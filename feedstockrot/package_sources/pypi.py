from .source import Source
import requests
from typing import Dict, Set, List
import logging


class Pypi(Source):

    DEFAULT_PACKAGE_URL = "https://pypi.python.org/pypi/{}/json"

    @classmethod
    def _possible_names(cls, name: str) -> List[str]:
        names = list(super()._possible_names(name))

        if name.startswith('python-'):
            names.append(name[len('python-'):])
        elif name.startswith('py-'):
            names.append(name[len('py-'):])

        if name.endswith('-python'):
            names.append(name[:-len('-python')])
        elif name.endswith('-py'):
            names.append(name[:-len('-py')])

        if len(names) > 1:
            logging.debug('Possible names for {}: {}'.format(name, names))

        return names

    @classmethod
    def __fetch(cls, name) -> Dict:
        resp = requests.get(cls.DEFAULT_PACKAGE_URL.format(name))
        if resp.status_code != 200:
            return None
        return resp.json()

    @classmethod
    def _fetch_versions(cls, name: str) -> Set[str]:
        resp = cls.__fetch(name)
        if resp is None:
            return None
        return resp['releases'].keys()
