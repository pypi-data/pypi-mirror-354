# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import copy
import os
from collections.abc import Iterator
from functools import cached_property
from pathlib import Path
from typing import Final, Optional, TypeVar, Union
from zoneinfo import ZoneInfo

from ddeutil.core import str2bool
from ddeutil.io import YamlFlResolve, search_env_replace
from ddeutil.io.paths import glob_files, is_ignored, read_ignore
from pydantic import SecretStr

from .__types import DictData
from .utils import obj_name

T = TypeVar("T")
PREFIX: Final[str] = "WORKFLOW"


def env(var: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment variable with uppercase and adding prefix string.

    :param var: (str) A env variable name.
    :param default: (Optional[str]) A default value if an env var does not set.

    :rtype: Optional[str]
    """
    return os.getenv(f"{PREFIX}_{var.upper().replace(' ', '_')}", default)


class Config:  # pragma: no cov
    """Config object for keeping core configurations on the current session
    without changing when if the application still running.

        The config value can change when you call that config property again.
    """

    @property
    def conf_path(self) -> Path:
        """Config path that keep all workflow template YAML files.

        :rtype: Path
        """
        return Path(env("CORE_CONF_PATH", "./conf"))

    @property
    def tz(self) -> ZoneInfo:
        """Timezone value that return with the `ZoneInfo` object and use for all
        datetime object in this workflow engine.

        :rtype: ZoneInfo
        """
        return ZoneInfo(env("CORE_TIMEZONE", "UTC"))

    @property
    def generate_id_simple_mode(self) -> bool:
        """Flag for generate running ID with simple mode. That does not use
        `md5` function after generate simple mode.

        :rtype: bool
        """
        return str2bool(env("CORE_GENERATE_ID_SIMPLE_MODE", "true"))

    @property
    def registry_caller(self) -> list[str]:
        """Register Caller that is a list of importable string for the call
        stage model can get.

        :rtype: list[str]
        """
        regis_call_str: str = env("CORE_REGISTRY_CALLER", ".")
        return [r.strip() for r in regis_call_str.split(",")]

    @property
    def registry_filter(self) -> list[str]:
        """Register Filter that is a list of importable string for the filter
        template.

        :rtype: list[str]
        """
        regis_filter_str: str = env(
            "CORE_REGISTRY_FILTER", "ddeutil.workflow.templates"
        )
        return [r.strip() for r in regis_filter_str.split(",")]

    @property
    def trace_path(self) -> Path:
        return Path(env("LOG_TRACE_PATH", "./logs"))

    @property
    def debug(self) -> bool:
        """Debug flag for echo log that use DEBUG mode.

        :rtype: bool
        """
        return str2bool(env("LOG_DEBUG_MODE", "true"))

    @property
    def log_format(self) -> str:
        return env(
            "LOG_FORMAT",
            (
                "%(asctime)s.%(msecs)03d (%(process)-5d, "
                "%(thread)-5d) [%(levelname)-7s] (%(cut_id)s) %(message)-120s "
                "(%(filename)s:%(lineno)s) (%(name)-10s)"
            ),
        )

    @property
    def log_format_file(self) -> str:
        return env(
            "LOG_FORMAT_FILE",
            (
                "{datetime} ({process:5d}, {thread:5d}) ({cut_id}) "
                "{message:120s} ({filename}:{lineno})"
            ),
        )

    @property
    def enable_write_log(self) -> bool:
        return str2bool(env("LOG_TRACE_ENABLE_WRITE", "false"))

    @property
    def audit_path(self) -> Path:
        return Path(env("LOG_AUDIT_PATH", "./audits"))

    @property
    def enable_write_audit(self) -> bool:
        return str2bool(env("LOG_AUDIT_ENABLE_WRITE", "false"))

    @property
    def log_datetime_format(self) -> str:
        return env("LOG_DATETIME_FORMAT", "%Y-%m-%d %H:%M:%S")

    @property
    def stage_default_id(self) -> bool:
        return str2bool(env("CORE_STAGE_DEFAULT_ID", "false"))


class APIConfig:
    """API Config object."""

    @property
    def version(self) -> str:
        return env("API_VERSION", "1")

    @property
    def prefix_path(self) -> str:
        return env("API_PREFIX_PATH", f"/api/v{self.version}")


class YamlParser:
    """Base Load object that use to search config data by given some identity
    value like name of `Workflow` or `Crontab` templates.

    :param name: (str) A name of key of config data that read with YAML
        Environment object.
    :param path: (Path) A config path object.
    :param externals: (DictData) An external config data that want to add to
        loaded config data.
    :param extras: (DictDdata) An extra parameters that use to override core
        config values.

    :raise ValueError: If the data does not find on the config path with the
        name parameter.

    Noted:
        The config data should have `type` key for modeling validation that
    make this loader know what is config should to do pass to.

        ... <identity-key>:
        ...     type: <importable-object>
        ...     <key-data-1>: <value-data-1>
        ...     <key-data-2>: <value-data-2>

        This object support multiple config paths if you pass the `conf_paths`
    key to the `extras` parameter.
    """

    def __init__(
        self,
        name: str,
        *,
        path: Optional[Union[str, Path]] = None,
        externals: DictData | None = None,
        extras: DictData | None = None,
        obj: Optional[Union[object, str]] = None,
    ) -> None:
        self.path: Path = Path(dynamic("conf_path", f=path, extras=extras))
        self.externals: DictData = externals or {}
        self.extras: DictData = extras or {}
        self.data: DictData = self.find(
            name,
            path=path,
            paths=self.extras.get("conf_paths"),
            extras=extras,
            obj=obj,
        )

        # VALIDATE: check the data that reading should not empty.
        if not self.data:
            raise ValueError(
                f"Config {name!r} does not found on the conf path: {self.path}."
            )

        self.data.update(self.externals)

    @classmethod
    def find(
        cls,
        name: str,
        *,
        path: Optional[Path] = None,
        paths: Optional[list[Path]] = None,
        obj: Optional[Union[object, str]] = None,
        extras: Optional[DictData] = None,
        ignore_filename: Optional[str] = None,
    ) -> DictData:
        """Find data with specific key and return the latest modify date data if
        this key exists multiple files.

        :param name: (str) A name of data that want to find.
        :param path: (Path) A config path object.
        :param paths: (list[Path]) A list of config path object.
        :param obj: (object | str) An object that want to validate matching
            before return.
        :param extras: (DictData)  An extra parameter that use to override core
            config values.
        :param ignore_filename: (str) An ignore filename. Default is
            ``.confignore`` filename.

        :rtype: DictData
        """
        path: Path = dynamic("conf_path", f=path, extras=extras)
        if not paths:
            paths: list[Path] = [path]
        elif not isinstance(paths, list):
            raise TypeError(
                f"Multi-config paths does not support for type: {type(paths)}"
            )
        else:
            paths: list[Path] = copy.deepcopy(paths)
            paths.append(path)

        all_data: list[tuple[float, DictData]] = []
        obj_type: Optional[str] = obj_name(obj)

        for path in paths:
            for file in glob_files(path):

                if cls.is_ignore(file, path, ignore_filename=ignore_filename):
                    continue

                if data := cls.filter_yaml(file, name=name):
                    if not obj_type:
                        all_data.append((file.lstat().st_mtime, data))
                    elif (t := data.get("type")) and t == obj_type:
                        all_data.append((file.lstat().st_mtime, data))
                    else:
                        continue

        return {} if not all_data else max(all_data, key=lambda x: x[0])[1]

    @classmethod
    def finds(
        cls,
        obj: Union[object, str],
        *,
        path: Optional[Path] = None,
        paths: Optional[list[Path]] = None,
        excluded: Optional[list[str]] = None,
        extras: Optional[DictData] = None,
        ignore_filename: Optional[str] = None,
    ) -> Iterator[tuple[str, DictData]]:
        """Find all data that match with object type in config path. This class
        method can use include and exclude list of identity name for filter and
        adds-on.

        :param obj: (object | str) An object that want to validate matching
            before return.
        :param path: (Path) A config path object.
        :param paths: (list[Path]) A list of config path object.
        :param excluded: An included list of data key that want to filter from
            data.
        :param extras: (DictData) An extra parameter that use to override core
            config values.
        :param ignore_filename: (str) An ignore filename. Default is
            ``.confignore`` filename.

        :rtype: Iterator[tuple[str, DictData]]
        """
        excluded: list[str] = excluded or []
        path: Path = dynamic("conf_path", f=path, extras=extras)
        paths: Optional[list[Path]] = paths or (extras or {}).get("conf_paths")
        if not paths:
            paths: list[Path] = [path]
        elif not isinstance(paths, list):
            raise TypeError(
                f"Multi-config paths does not support for type: {type(paths)}"
            )
        else:
            paths.append(path)

        all_data: dict[str, list[tuple[float, DictData]]] = {}
        obj_type: str = obj_name(obj)

        for path in paths:
            for file in glob_files(path):

                if cls.is_ignore(file, path, ignore_filename=ignore_filename):
                    continue

                for key, data in cls.filter_yaml(file).items():

                    if key in excluded:
                        continue

                    if (t := data.get("type")) and t == obj_type:
                        marking: tuple[float, DictData] = (
                            file.lstat().st_mtime,
                            data,
                        )
                        if key in all_data:
                            all_data[key].append(marking)
                        else:
                            all_data[key] = [marking]

        for key in all_data:
            yield key, max(all_data[key], key=lambda x: x[0])[1]

    @classmethod
    def is_ignore(
        cls,
        file: Path,
        path: Path,
        *,
        ignore_filename: Optional[str] = None,
    ) -> bool:
        """Check this file was ignored from the `.confignore` format.

        :param file: (Path) A file path that want to check.
        :param path: (Path) A config path that want to read the config
            ignore file.
        :param ignore_filename: (str) An ignore filename. Default is
            ``.confignore`` filename.

        :rtype: bool
        """
        ignore_filename: str = ignore_filename or ".confignore"
        return is_ignored(file, read_ignore(path / ignore_filename))

    @classmethod
    def filter_yaml(cls, file: Path, name: Optional[str] = None) -> DictData:
        """Read a YAML file context from an input file path and specific name.

        :param file: (Path) A file path that want to extract YAML context.
        :param name: (str) A key name that search on a YAML context.

        :rtype: DictData
        """
        if any(file.suffix.endswith(s) for s in (".yml", ".yaml")):
            values: DictData = YamlFlResolve(file).read()
            if values is not None:
                return values.get(name, {}) if name else values
        return {}

    @cached_property
    def type(self) -> str:
        """Return object of string type which implement on any registry. The
        object type.

        :rtype: str
        """
        if _typ := self.data.get("type"):
            return _typ
        raise ValueError(
            f"the 'type' value: {_typ} does not exists in config data."
        )


config: Config = Config()
api_config: APIConfig = APIConfig()


def dynamic(
    key: Optional[str] = None,
    *,
    f: Optional[T] = None,
    extras: Optional[DictData] = None,
) -> Optional[T]:
    """Dynamic get config if extra value was passed at run-time.

    :param key: (str) A config key that get from Config object.
    :param f: (T) An inner config function scope.
    :param extras: An extra values that pass at run-time.

    :rtype: T
    """
    extra: Optional[T] = (extras or {}).get(key, None)
    conf: Optional[T] = getattr(config, key, None) if f is None else f
    if extra is None:
        return conf
    if not isinstance(extra, type(conf)):
        raise TypeError(
            f"Type of config {key!r} from extras: {extra!r} does not valid "
            f"as config {type(conf)}."
        )
    return extra


def pass_env(value: T) -> T:  # pragma: no cov
    """Passing environment variable to an input value.

    :param value: (Any) A value that want to pass env var searching.

    :rtype: Any
    """
    if isinstance(value, dict):
        return {k: pass_env(value[k]) for k in value}
    elif isinstance(value, (list, tuple, set)):
        return type(value)([pass_env(i) for i in value])
    if not isinstance(value, str):
        return value

    rs: str = search_env_replace(value)
    return None if rs == "null" else rs


class CallerSecret(SecretStr):  # pragma: no cov
    """Workflow Secret String model."""

    def get_secret_value(self) -> str:
        """Override get_secret_value by adding pass_env before return the
        real-value.

        :rtype: str
        """
        return pass_env(super().get_secret_value())
