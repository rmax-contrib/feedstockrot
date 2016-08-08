from unittest import TestCase
from feedstockrot.package_sources.condaforge import Condaforge
from feedstockrot.package import Package
from packaging.version import Version
from ..helpers.mock.mock import Mocker
from ..helpers.mock.condaforge import CondaforgeRepoMock
from ..helpers.mock.condaforge import CondaforgeRecipeMock
from ..helpers.mock.pypi import PypiMock


class TestCondaforge(TestCase):

    def test_possible_names(self):
        self.assertListEqual(
            ['testing-feedstock', 'testing'],
            list(Condaforge._possible_names('testing-feedstock'))
        )

    def test_get_repodata(self):
        with Mocker(CondaforgeRepoMock('package_a')):
            result = Condaforge._get_repodata()

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn('packages', result)
        self.assertIn('package_a-1.0', result['packages'])

    def test_fetch_versions(self):
        with Mocker(CondaforgeRepoMock('package_a')):
            result_a = Condaforge._fetch_versions("package_a")
        expected_a = {'1.0', '1.2', '2.0'}
        self.assertSetEqual(result_a, expected_a)

        with Mocker(CondaforgeRepoMock('package_b')):
            result_b = Condaforge._fetch_versions("package_b")
        self.assertSetEqual(result_b, {'1.0'})

    def test_versions(self):
        with Mocker(CondaforgeRepoMock('package_a'), PypiMock('package_a')):
            src_a = Condaforge(Package('package_a'))

        self.assertSetEqual(
            {Version('1.0'), Version('1.2'), Version('2.0')},
            src_a.versions
        )

        with Mocker(CondaforgeRepoMock('package_b'), PypiMock('package_b')):
            src_b = Condaforge(Package('package_b'))

        self.assertSetEqual(
            {Version('1.0')},
            src_b.versions
        )

    def test__get_recipe_a(self):
        with Mocker(CondaforgeRepoMock('package_a'), PypiMock('package_a')):
            src_a = Condaforge(Package('package_a'))
        with Mocker(CondaforgeRecipeMock('package_a')):
            result = src_a._get_recipe()
        self.assertIsInstance(result, dict)
        self.assertIn('package', result)

    def test__get_recipe_b(self):
        with Mocker(CondaforgeRepoMock('package_b'), PypiMock('package_b')):
            src_a = Condaforge(Package('package_b'))
        with Mocker(CondaforgeRecipeMock('package_b')):
            result = src_a._get_recipe()
        self.assertIsInstance(result, dict)
        self.assertIn('package', result)
        self.assertIn('about', result)
        self.assertIn('home', result['about'])

    def test_get_recipe_urls_a(self):
        with Mocker(CondaforgeRepoMock('package_a'), PypiMock('package_a')):
            src_a = Condaforge(Package('package_a'))
        with Mocker(CondaforgeRecipeMock('package_a')):
            result = src_a.get_recipe_urls()
        self.assertEqual(0, len(result))

    def test_get_recipe_urls_b(self):
        with Mocker(CondaforgeRepoMock('package_b'), PypiMock('package_b')):
            src_a = Condaforge(Package('package_b'))
        with Mocker(CondaforgeRecipeMock('package_b')):
            result = src_a.get_recipe_urls()
        self.assertEqual(1, len(result))
