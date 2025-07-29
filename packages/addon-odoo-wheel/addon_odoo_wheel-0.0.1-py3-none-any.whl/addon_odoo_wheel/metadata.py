import email
import logging
from email.message import Message
from email.utils import formataddr
from pathlib import Path
from typing import Optional

from manifestoo_core.addon import Addon
from manifestoo_core.exceptions import UnsupportedManifestVersion
from manifestoo_core.manifest import Manifest
from manifestoo_core.metadata import OdooSeriesInfo
from manifestoo_core.odoo_series import MIN_VERSION_PARTS, OdooSeries

from . import compat
from .utils import (
    EXTRA_NAME_RE,
    WHEEL_TAG,
    PyProjectConfig,
    load_pyproject_toml,
    normalize_label,
    odoo_licence_to_SDPX,
)
from .well_know import WellKnowAddonContributor

_logger = logging.getLogger(__name__)


class AddonMetadata:
    addon: Addon
    metadata: Message
    """The metadata extracted from manifest"""
    odoo_series: OdooSeries
    odoo_series_info: OdooSeriesInfo
    """The Odoo version found from the module version or the key `odoo_version_override` in pyproject.toml"""
    git_postversion: str

    @classmethod
    def from_addon_dir(
        cls, addon_dir: Path, allow_not_installable: bool = True, force_addon_name: str = None
    ) -> "AddonMetadata":
        _addon = Addon.from_addon_dir(addon_dir, allow_not_installable)
        if force_addon_name:
            _addon.name = force_addon_name
        pyproject_options = load_pyproject_toml(addon_dir)
        return cls(pyproject_options, _addon)

    def __init__(self, pyproject_options: PyProjectConfig, addon: Addon) -> None:
        self.addon = addon
        self.pyproject_options = pyproject_options
        self._set_odoo_series()
        self.git_postversion = (
            self.pyproject_options.tool_mangono.post_version_strategy_override
            or self.odoo_series_info.git_postversion_strategy
        )

    @property
    def metadata(self) -> Message:
        return self._generate_metadata()

    @property
    def addon_path(self):
        return self.addon.path

    @property
    def odoo_series_info(self):
        return OdooSeriesInfo.from_odoo_series(self.odoo_series)

    @property
    def wheel_name(self) -> str:
        return f"{self.sdist_name}-{WHEEL_TAG}"

    @property
    def sdist_name(self) -> str:
        return "{}-{}".format(self.metadata["Name"].replace("-", "_").replace(".", "_"), self.metadata["Version"])

    @property
    def addon_name(self):
        return self.addon.name

    @property
    def manifest(self) -> Manifest:
        return self.addon.manifest

    def _set_odoo_series(self):
        if self.pyproject_options.tool_mangono.odoo_version_override:
            self.odoo_series = OdooSeries.from_str(self.pyproject_options.tool_mangono.odoo_version_override)
        else:
            version_parts = self.addon.manifest.version.split(".")
            if len(version_parts) < MIN_VERSION_PARTS:
                msg = (
                    f"Version in manifest must have at least "
                    f"{MIN_VERSION_PARTS} components and start with "
                    f"the Odoo series number (in {self.addon.path})"
                )
                raise UnsupportedManifestVersion(msg)
            self.odoo_series = OdooSeries.from_str(".".join(version_parts[:2]))

    def _generate_metadata(self) -> Message:
        """Return Python Package Metadata 2.1 for an Odoo addon directory as an
        ``email.message.Message``.

        The Description field is absent and is stored in the message payload. All values are
        guaranteed to not contain newline characters, except for the payload.

        ``precomputed_metadata_path`` may point to a file containing pre-computed metadata
        that will be used to obtain the Name and Version, instead of looking at the addon
        directory name or manifest version + VCS, respectively. This is useful to process a
        manifest from a sdist tarball with PKG-INFO, for example, when the original
        directory name or VCS is not available to compute the package name and version.

        This function may raise :class:`manifestoo_core.exceptions.ManifestooException` if
        ``addon_dir`` does not contain a valid installable Odoo addon for a supported Odoo
        version.
        """
        if (self.addon.path / "PKG-INFO").exists():
            # if PKG-INFO is present, assume we are in an sdist, copy everything
            with (self.addon.path / "PKG-INFO").open("r") as f:
                return email.parser.HeaderParser().parse(f)
        return self.construct_metadata_file_2_4()

    def construct_metadata_file_2_4(self) -> Message:
        """
        https://peps.python.org/pep-0639/
        """
        msg = Message()

        msg["Metadata-Version"] = "2.4"
        self._set_name_and_version(msg)
        self._set_urls(msg)
        self._set_authors(msg)
        self._set_license(msg)
        self._set_classifier(msg)
        self._set_require_python(msg)
        self._set_dependencies(msg)
        self._set_description(msg)
        return msg

    def _set_name_and_version(self, msg):
        pkg_name = self.pyproject_options.name
        if not pkg_name or pkg_name == "auto:addon":
            prefix = WellKnowAddonContributor.from_author(self.manifest.author).get_package_prefix(self.odoo_series)
            if prefix:
                pkg_name = f"{prefix}-{self.addon_name}"
            else:
                pkg_name = self.addon_name
        msg["Name"] = pkg_name

        _version = self.manifest.version
        if "version" not in self.pyproject_options.dynamic and self.pyproject_options.version:
            _logger.debug("Force set version from pyproject.toml: %s -> %s", _version, self.pyproject_options.version)
            _version = self.pyproject_options.version
        msg["Version"] = str(_version)

    def _set_description(self, msg):
        if self.pyproject_options.get("summary"):
            msg["Summary"] = self.pyproject_options.get("summary").splitlines()[0]
        to_try = [("README.md", "text/markdown"), ("README.rst", "text/x-rst")]
        if self.pyproject_options.get("readme"):
            content_type = "text/plain"
            if Path(self.pyproject_options.get("readme")).suffix == ".md":
                content_type = "text/markdown"
            if Path(self.pyproject_options.get("readme")).suffix == ".rst":
                content_type = "text/x-rst"
            to_try.insert(0, (self.pyproject_options.get("readme"), content_type))

        for read_to_try in to_try:
            if not read_to_try[0]:
                continue
            readme_path = self.addon.path / read_to_try[0]
            if readme_path.exists() and readme_path.is_file():
                msg["Description-Content-Type"] = read_to_try[1]
                msg.set_payload(readme_path.read_text(encoding="utf-8"))
                break
        else:
            if self.manifest.description:
                msg["Description-Content-Type"] = "text/plain"
                msg["Description"] = self.manifest.description

    def _set_dependencies(self, msg):
        for dependency in self.pyproject_options.dependencies:
            msg["Requires-Dist"] = str(dependency)
        for extra, dependencies in self.pyproject_options.get("optional-dependencies", {}).items():
            if not EXTRA_NAME_RE.match(extra):
                raise ValueError(
                    f"Invalid extra name: {extra!r} See: https://packaging.python.org/en/latest/specifications/core-metadata/#provides-extra-multiple-use"
                )
            msg["Provides-Extra"] = extra
            for dependency in dependencies:
                msg["Requires-Dist"] = f"{dependency}; extra == {extra!r}"

    def _set_require_python(self, msg):
        if self.pyproject_options.requires_python or self.odoo_series:
            msg["Requires-Python"] = self.pyproject_options.requires_python or self.odoo_series_info.python_requires

    def _set_classifier(self, msg):
        classifiers = set(self.pyproject_options.classifiers)
        if self.odoo_series:
            _manifest_copy = Manifest.from_dict(self.manifest.manifest_dict)
            if not self.manifest.development_status:
                version_parts = self.manifest.version.split(".")
                if len(version_parts) == MIN_VERSION_PARTS:
                    version_parts = version_parts[2:]
                development_status = "stable" if int(version_parts[0]) > 0 else "alpha"
                _manifest_copy = Manifest.from_dict(
                    dict(self.manifest.manifest_dict, development_status=development_status)
                )
            classifiers |= set(compat.make_classifiers(self.odoo_series, _manifest_copy))
        for classifier in classifiers:
            msg["Classifier"] = classifier

    def _set_license(self, msg):
        license_map = odoo_licence_to_SDPX.get(self.manifest.license)
        if self.addon.manifest.license == "Other proprietary" and not self.pyproject_options.license:
            raise ValueError("field `project.license` must be static when using 'Other proprietary' value in manifest")
        msg["License-Expression"] = license_map or self.pyproject_options.license or "AGPL-3.0-or-later"
        for license_file in self.pyproject_options.license_files:
            msg["License-File"] = license_file

    def _set_urls(self, msg):
        urls = self.pyproject_options.get("urls", {})
        urls["Homepage"] = self.manifest.website
        for label, url in urls.items():
            is_well_know, label_n = normalize_label(label)
            msg["Project-URL"] = f"{label_n}, {url}"

    def _set_authors(self, msg: Message):
        odoo_authors = []
        if self.manifest.author:
            odoo_authors = self.manifest.author.split(",")
        author_values = []
        author_no_mail = []
        for author in self.pyproject_options.get("authors", []):
            if author["name"] in odoo_authors:
                odoo_authors.remove(author["name"])
            author_values.append(formataddr((author["name"], author["email"])))

        for odoo_author in odoo_authors:
            email = WellKnowAddonContributor.from_author(self.manifest.author).get_mail(self.odoo_series)
            if email:
                author_values.append(formataddr((odoo_author, email)))
            else:
                author_no_mail.append(odoo_author)
        if author_values:
            msg["Author-Email"] = ", ".join(author_values)
        if author_no_mail:
            msg["Author"] = ", ".join(author_no_mail)


def _no_nl(s: Optional[str]) -> Optional[str]:
    if not s:
        return s
    return " ".join(s.split())


def _author_email(author_name: Optional[str]) -> Optional[str]:
    if author_name == "Odoo Community Association (OCA)":
        return "support@odoo-community.org"
    if author_name.upper() == "Mangono":
        return "opensource+wheel@mangono.fr"
    return None
