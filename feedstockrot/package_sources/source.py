import abc
from typing import Set
from packaging.version import Version, InvalidVersion


class Source(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def _fetch_package_versions(self, name: str) -> Set[str]:
        pass

    @classmethod
    def get_package_versions(cls, package_name: str) -> Set[Version]:
        versions = set()

        versions_raw = cls._fetch_package_versions(package_name)
        if versions_raw is None:
            return None

        for version_str in versions_raw:
            try:
                version = Version(version_str)
            except InvalidVersion:
                continue
            versions.add(version)
        return versions