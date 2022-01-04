from registration import Registration
import unittest


class TestRegistration(unittest.TestCase):

    def test_get_sex(self):
        self.assertEqual(Registration.get_sex(Registration,1), 1)

    def test_get_city(self):
        self.assertEqual(Registration.get_city(Registration,1), 2)

    def test_get_age(self):
        self.assertEqual(Registration.get_age(Registration,1), 37)