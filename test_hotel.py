# test_hotel.py
"""Unit tests for hotel.py"""

import unittest
import os
import sys
from io import StringIO
from hotel import Hotel


class TestHotel(unittest.TestCase):
    """Test hotel"""
    @classmethod
    def setUpClass(cls):
        if os.path.exists(Hotel.hotels_file):
            os.remove(Hotel.hotels_file)

    def setUp(self):
        """Set up for testing"""
        self.hotel = Hotel("H100", "Test Hotel", "Test Location", {})
        self.hotel.save()
        self.original_stdout = sys.stdout
        sys.stdout = StringIO()

    def test_hotel_creation(self):
        """Hotel creation"""
        self.assertEqual(self.hotel.hotel_id, "H100")
        self.assertEqual(self.hotel.name, "Test Hotel")

    def test_add_room(self):
        """Room adding"""
        self.hotel.add_room("101", available=True)
        self.assertIn("101", self.hotel.rooms)
        self.assertTrue(self.hotel.rooms["101"]["available"])

    def test_remove_room(self):
        """Room remotion"""
        self.hotel.add_room("102", available=True)
        self.hotel.remove_room("102")
        self.assertNotIn("102", self.hotel.rooms)

    def test_save_and_load_hotel(self):
        """Save hotel"""
        self.hotel.save()
        loaded_hotels = Hotel.get_all_hotels()
        self.assertIn("H100", loaded_hotels)

    def test_delete_hotel(self):
        """Delete hotel"""
        self.hotel.save()
        Hotel.delete("H100")
        hotels_after_deletion = Hotel.get_all_hotels()
        self.assertNotIn("H100", hotels_after_deletion)

    def test_display_info(self):
        """Check that the info is correctly displayed"""
        expected_output = "Hotel ID: H100, Name: Test Hotel, Location: Test Location, Rooms: {}\n"
        self.hotel.display_info(self.hotel.hotel_id)
        output = sys.stdout.getvalue()
        self.assertEqual(output, expected_output)

    def tearDown(self):
        sys.stdout = self.original_stdout

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(Hotel.hotels_file):
            os.remove(Hotel.hotels_file)

if __name__ == '__main__':
    unittest.main(verbosity=2)
