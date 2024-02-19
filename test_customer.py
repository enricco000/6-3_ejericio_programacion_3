# test_customer.py
"""Unit tests for customer.py"""

import unittest
import os
from customer import Customer

class TestCustomer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if os.path.exists(Customer.customers_file):
            os.remove(Customer.customers_file)

    def setUp(self):
        """Create a test customer instance."""
        self.customer = Customer("C001", "John Doe", "johndoe@example.com")

    def test_customer_creation(self):
        """Test initializing a customer instance."""
        self.assertEqual(self.customer.customer_id, "C001")
        self.assertEqual(self.customer.name, "John Doe")
        self.assertEqual(self.customer.email, "johndoe@example.com")

    def test_save_and_load_customer(self):
        """Test saving a customer to file and loading it."""
        self.customer.save()
        loaded_customers = Customer.get_all_customers()
        self.assertIn("C001", loaded_customers)

    def test_delete_customer(self):
        """Test deleting a customer from file."""
        self.customer.save()
        Customer.delete("C001")
        customers_after_deletion = Customer.get_all_customers()
        self.assertNotIn("C001", customers_after_deletion)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(Customer.customers_file):
            os.remove(Customer.customers_file)

if __name__ == '__main__':
    unittest.main()
