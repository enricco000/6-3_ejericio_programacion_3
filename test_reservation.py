# test_reservation.py
"""Unit tests for reservation.py"""

import unittest
import os
from reservation import Reservation
from hotel import Hotel
from customer import Customer

class TestReservation(unittest.TestCase):
    """Test reservations"""
    @classmethod
    def setUpClass(cls):
        if os.path.exists(Reservation.reservations_file):
            os.remove(Reservation.reservations_file)
        # Setup for related Hotel and Customer instances
        Hotel("H001", "Test Hotel", "Test Location", {}).save()
        Customer("C001", "John Doe", "johndoe@example.com").save()

    def setUp(self):
        """Create a test reservation instance."""
        self.reservation = Reservation("R001", "C001", "H001", "101", "2024-01-01", "2024-01-10")

    def test_reservation_creation(self):
        """Test initializing a reservation instance."""
        self.assertEqual(self.reservation.reservation_id, "R001")
        self.assertEqual(self.reservation.customer_id, "C001")
        self.assertEqual(self.reservation.hotel_id, "H001")
        self.assertEqual(self.reservation.room_number, "101")
        self.assertEqual(self.reservation.start_date, "2024-01-01")
        self.assertEqual(self.reservation.end_date, "2024-01-10")

    def test_save_and_load_reservation(self):
        """Test saving a reservation to file and loading it."""
        self.reservation.save()
        loaded_reservations = Reservation.get_all_reservations()
        self.assertIn("R001", loaded_reservations)

    def test_cancel_reservation(self):
        """Test canceling a reservation."""
        self.reservation.save()
        Reservation.cancel("R001")
        reservations_after_cancellation = Reservation.get_all_reservations()
        self.assertNotIn("R001", reservations_after_cancellation)

    @classmethod
    def tearDownClass(cls):
        # Clean up created files during tests
        if os.path.exists(Reservation.reservations_file):
            os.remove(Reservation.reservations_file)
        if os.path.exists(Hotel.hotels_file):
            os.remove(Hotel.hotels_file)
        if os.path.exists(Customer.customers_file):
            os.remove(Customer.customers_file)

if __name__ == '__main__':
    unittest.main(verbosity=2)
