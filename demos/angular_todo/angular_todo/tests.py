import unittest
from pyramid import testing


class ViewTests(unittest.TestCase):
    def setUp(self):
        testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home_view(self):
        from .views import DemoViews

        request = testing.DummyRequest()
        dv = DemoViews({}, request)
        response = dv.home_view()
        self.assertEqual(response, {})
