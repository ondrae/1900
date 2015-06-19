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

        # Menu is listening
        self.assertEqual(root[0].tag, 'Gather')

        # Menu has five options
        self.assertEquals(len(root[0].findall('Say')), 5,
                "Did not find five menu options, instead found: %i " %
                len(root.findall('Say')))


    def test_menu_1(self):
        """ Test that pressing menu 1 plays an mp3"""
        response = self.app.post("/menu_press", data={"Digits" : 1})

        # Parse the result into an ElementTree object
        root = ElementTree.fromstring(response.data)

        # Assert the root element is a Response tag
        self.assertEquals(root.tag, 'Response',
                "Did not find  tag as root element " \
                "TwiML response.")

        # Mp3 plays
        self.assertEqual(root[0].tag, 'Play')
        self.assertTrue(root[0].text.endswith('.mp3'))


    def test_menu_2(self):
        """ Test that pressing menu 2 calls random other caller """
        response = self.app.post("/menu_press", data={"Digits" : 2})

        # Parse the result into an ElementTree object
        root = ElementTree.fromstring(response.data)

        # Assert the root element is a Response tag
        self.assertEquals(root.tag, 'Response',
                "Did not find  tag as root element " \
                "TwiML response.")

        # Call an outbound number
        self.assertEqual(root[1].tag, 'Dial')


if __name__ == '__main__':
    unittest.main()