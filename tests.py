import unittest
from app import app

from xml.etree import ElementTree

class PartyLineTest(unittest.TestCase):

    def setUp(self):

        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_incoming_call(self):
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

        # Menu mp3
        self.assertEqual(root[0][0].tag, 'Play')
        self.assertTrue(root[0][0].text.endswith('.mp3'))


    def test_bad_menu_press(self):
        """ Test that non menu choices start the menu over """
        response = self.app.post("/menu_press", data={"Digits" : 9})

        self.assertEquals(response.status, "200 OK")

        # Parse the result into an ElementTree object
        root = ElementTree.fromstring(response.data)

        # Assert that we are about to redirect
        self.assertTrue(root[0].tag,"Redirect")
        self.assertTrue(root[0].text,"/")


    def test_cry(self):
        """ Test crying mp3"""
        response = self.app.post("/menu_press", data={"Digits" : 3})

        # Parse the result into an ElementTree object
        root = ElementTree.fromstring(response.data)

        # Assert the root element is a Response tag
        self.assertEquals(root.tag, 'Response',
                "Did not find  tag as root element " \
                "TwiML response.")

        # Listen for 0
        self.assertEqual(root[0].tag, 'Gather')

        # Play a message
        self.assertEqual(root[0][0].tag, 'Play')
        self.assertTrue(root[0][0].text.endswith('.mp3'))


    def test_privatepartyline(self):
        """ Test private party lines """
        response = self.app.post("/menu_press", data={"Digits" : 1})

        # Parse the result into an ElementTree object
        root = ElementTree.fromstring(response.data)

        self.assertEquals(response.status, "200 OK")

        # Assert the root element is a Response tag
        self.assertEquals(root.tag, 'Response',
                "Did not find  tag as root element " \
                "TwiML response.")

        # Dial into a conference
        self.assertEqual(root[0].tag, 'Dial')
        self.assertEqual(root[0][0].tag, 'Conference')
        self.assertEqual(root[0][0].text,'partyline1')


    def test_grouppartyline(self):
        """ Test group party lines """
        response = self.app.post("/menu_press", data={"Digits" : 2})

        # Parse the result into an ElementTree object
        root = ElementTree.fromstring(response.data)

        self.assertEquals(response.status, "200 OK")

        # Assert the root element is a Response tag
        self.assertEquals(root.tag, 'Response',
                "Did not find  tag as root element " \
                "TwiML response.")

        # Dial into a conference
        self.assertEqual(root[0].tag, 'Say')
        self.assertEqual(root[1].tag, 'Say')
        self.assertEqual(root[2].tag, 'Dial')
        self.assertEqual(root[2][0].tag, 'Conference')
        self.assertEqual(root[2][0].text,'grouppartyline')


if __name__ == '__main__':
    unittest.main()