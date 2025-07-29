from __future__ import annotations

import dataclasses
import os
import re
import shutil
import string
import subprocess
from email.generator import Generator
from email.message import Message
from pathlib import Path
from typing import Any

from manifestoo_core.metadata import EXTERNAL_DEPENDENCIES_MAP
from packaging.requirements import Requirement

from .compat import tomllib
from .exceptions import NoScmFound
from .version import version as lib_version


def _get_mapping_metadata():
    return {"-".join(t.capitalize() for t in k.split("-")): v for k, v in EXTERNAL_DEPENDENCIES_MAP.items()}


EXTRA_NAME_RE = re.compile("^[a-z0-9]+(-[a-z0-9]+)*$")

CORE_METADATA_PROJECT_FIELDS = {
    "Author": ("authors",),
    "Author-email": ("authors",),
    "Classifier": ("classifiers",),
    "Description": ("readme",),
    "Description-Content-Type": ("readme",),
    "Dynamic": ("dynamic",),
    "Keywords": ("keywords",),
    "License": ("license",),
    "License-Expression": ("license",),
    "License-Files": ("license-files",),
    "Maintainer": ("maintainers",),
    "Maintainer-email": ("maintainers",),
    "Name": ("name",),
    "Provides-Extra": ("dependencies", "optional-dependencies"),
    "Requires-Dist": ("dependencies",),
    "Requires-Python": ("requires-python",),
    "Summary": ("description",),
    "Project-URL": ("urls",),
    "Version": ("version",),
}
PROJECT_CORE_METADATA_FIELDS = {
    "authors": ("Author", "Author-email"),
    "classifiers": ("Classifier",),
    "dependencies": ("Requires-Dist",),
    "dynamic": ("Dynamic",),
    "keywords": ("Keywords",),
    "license": ("License", "License-Expression"),
    "license-files": ("License-Files",),
    "maintainers": ("Maintainer", "Maintainer-email"),
    "name": ("Name",),
    "optional-dependencies": ("Requires-Dist", "Provides-Extra"),
    "readme": ("Description", "Description-Content-Type"),
    "requires-python": ("Requires-Python",),
    "description": ("Summary",),
    "urls": ("Project-URL",),
    "version": ("Version",),
}
WHEEL_TAG = "py3-none-any"

"""
Mapping with SDPX licence from https://spdx.org/licenses/
"""
odoo_licence_to_SDPX = {
    "GPL-2": "GPL-2.0",
    "GPL-2 or any later version": "GPL-2.0-or-later",
    "GPL-3": "GPL-3.0-only",
    "GPL-3 or any later version": "GPL-3.0-or-later",
    "AGPL-3": "AGPL-3.0-or-later",
    "LGPL-3": "LGPL-3.0-or-later",
    "Other OSI approved licence": "any-OSI",
    "OEEL-1": "LicenseRef-OEEL-1",
    "OPL-1": "LicenseRef-OPL-1",
    "Other proprietary": "",
}


def base_wheel_metadata() -> Message:
    """
    Create and return the base metadata for the wheel.

    This metadata includes the wheel version, the generator information,
    whether the root is purelib, and the tag. It is used in the creation
    of the wheel file for the Odoo addon.

    Returns:
        Message: An email.message.Message object containing the base wheel metadata.
    """
    msg = Message()
    msg["Wheel-Version"] = "1.0"  # of the spec
    msg["Generator"] = "Mangono Wheel Builder" + lib_version
    msg["Root-Is-Purelib"] = "true"
    msg["Tag"] = WHEEL_TAG
    return msg


def write_metadata(msg: Message, dest: Path) -> None:
    with open(dest, "w", encoding="utf-8") as f:
        Generator(f, mangle_from_=False, maxheaderlen=0).flatten(msg)


def load_pyproject_toml(addon_dir: Path) -> PyProjectConfig:
    pyproject_toml_path = addon_dir / "pyproject.toml"
    if pyproject_toml_path.exists():
        with open(pyproject_toml_path, "rb") as f:
            return PyProjectConfig.from_config(tomllib.load(f))
    return PyProjectConfig.from_config({})


WellKnownLabels = [
    "homepage",
    "source",
    "download",
    "changelog",
    "releasenotes",
    "documentation",
    "issues",
    "funding",
]


def normalize_label(label: str) -> tuple[bool, str]:
    chars_to_remove = string.punctuation + string.whitespace
    removal_map = str.maketrans("", "", chars_to_remove)
    n_label = label.translate(removal_map).lower()
    return n_label in WellKnownLabels, n_label.capitalize()


@dataclasses.dataclass
class PyProjectConfig:
    project_config: dict
    name: str
    version: str
    dynamic: list[str]
    description: str
    readme: str
    readme_content_type: str
    license: str
    license_expression: str
    license_files: list[str]
    keywords: list[str]
    classifiers: list[str]
    requires_python: str
    requires_dist: list[str]
    dependencies: list[Requirement]
    optional_dependencies: dict[str, list[Requirement]]
    author: str
    author_email: str
    maintainer: str
    maintainer_email: str
    tool_mangono: ToolConfig

    @classmethod
    def from_file(cls, pyproject_toml_path: Path) -> PyProjectConfig:
        if not pyproject_toml_path.exists():
            raise FileNotFoundError(pyproject_toml_path)
        with open(pyproject_toml_path, "rb") as f:
            return cls.from_config(tomllib.load(f))

    def get(self, key: str, default=None):
        return self.project_config.get(key, default)

    @classmethod
    def from_config(cls, config: dict[str, Any]):
        project_config = config.get("project", {})
        r = cls(
            project_config=project_config,
            name=project_config.get("name") or "",
            version=project_config.get("version") or "",
            dynamic=project_config.get("dynamic") or [],
            description=project_config.get("description") or "",
            readme=project_config.get("readme") or "",
            readme_content_type=project_config.get("readme_content_type") or "",
            license=project_config.get("license") or "",
            license_expression=project_config.get("license_expression") or "",
            license_files=project_config.get("license_files") or [],
            keywords=project_config.get("keywords") or [],
            classifiers=project_config.get("classifiers") or [],
            requires_python=project_config.get("requires_python") or "",
            requires_dist=project_config.get("requires_dist") or [],
            dependencies=[Requirement(dep) for dep in project_config.get("dependencies") or []],
            optional_dependencies={
                option: [Requirement(dep) for dep in deps]
                for option, deps in project_config.get("optional-dependencies", {}).items()
            },
            author=project_config.get("author") or "",
            author_email=project_config.get("author_email") or "",
            maintainer=project_config.get("maintainer") or "",
            maintainer_email=project_config.get("maintainer_email") or "",
            tool_mangono=ToolConfig.from_config(config.get("tool", {}).get("mangono_odoo_wheeler", {})),
        )
        return r


@dataclasses.dataclass
class ToolConfig:
    support_only_community: bool
    post_version_strategy_override: bool
    ignore_depends: list[str]
    depends_override: dict[str, str]
    external_dependencies_only: bool
    external_dependencies_override: dict[str, str]
    auto_oca_depends: bool
    odoo_version_override: str | None

    @classmethod
    def from_config(cls, config: dict[str, Any]):
        if os.getenv("WHEEL_POST_VERSION_STRATEGY_OVERRIDE", "None").upper() not in ("FALSE", "NONE"):
            post_version_strategy_override = os.getenv("WHEEL_POST_VERSION_STRATEGY_OVERRIDE")
        else:
            post_version_strategy_override = config.get("post_version_strategy_override")
        return cls(
            odoo_version_override=config.get("odoo_version_override"),
            post_version_strategy_override=post_version_strategy_override,
            support_only_community=config.get("support_only_community") or True,
            ignore_depends=config.get("ignore_depends") or [],
            depends_override=config.get("depends_override") or {},
            external_dependencies_only=config.get("external_dependencies_only") or False,
            external_dependencies_override=dict(
                **EXTERNAL_DEPENDENCIES_MAP, **config.get("external_dependencies_override") or {}
            ),
            auto_oca_depends=config.get("auto_oca_depends") or True,
        )


def _scm_ls_files(addon_dir: Path) -> list[str]:
    try:
        return subprocess.check_output(["git", "ls-files"], universal_newlines=True, cwd=addon_dir).strip().split("\n")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise NoScmFound() from e


def copy_to(addon_dir: Path, dst: Path) -> None:
    if (Path(addon_dir) / "PKG-INFO").exists():
        # if PKG-INFO is present, assume we are in an sdist, copy everything
        shutil.copytree(addon_dir, dst)
        return
    # copy scm controlled files
    try:
        scm_files = _scm_ls_files(addon_dir)
    except NoScmFound:
        # NOTE This requires pip>=21.3 which builds in-tree. Previous pip versions
        # copied to a temporary directory with a different name than the addon, which
        # caused the resulting distribution name to be wrong.
        shutil.copytree(addon_dir, dst)
    else:
        dst.mkdir()
        for f in scm_files:
            d = Path(f).parent
            dstd = dst / d
            if not dstd.is_dir():
                dstd.mkdir(parents=True)
            shutil.copy(addon_dir / f, dstd)


def ensure_absent(paths: list[Path]) -> None:
    for path in paths:
        if path.exists():
            path.unlink()
