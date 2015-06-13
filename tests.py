import unittest
from app import app

from xml.etree import ElementTree

class PartyLineTest(unittest.TestCase):

    def setUp(self):

        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_party_line(self):
        """ Test that an incoming phone call works."""
        response = self.app.get('/')
        
        self.assertEquals(response.status, "200 OK")

        # Parse the result into an ElementTree object
        root = ElementTree.fromstring(response.data)

        # Assert the root element is a Response tag
        self.assertEquals(root.tag, 'Response',
                "Did not find  tag as root element " \
                "TwiML response.")

        # Assert menu has five options
        self.assertEquals(len(root.findall('Say')), 5,
                "Did not find five menu options, instead found: %i " %
                len(root.findall('Say')))


if __name__ == '__main__':
    unittest.main()