# customer.py
"""This code handles customers"""

import json
import os
import argparse


class Customer:
    """Customer class for the system"""
    customers_file = 'customers.json'

    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def save(self):
        """Save the customer to the JSON file."""
        if not os.path.isfile(Customer.customers_file):
            with open(Customer.customers_file, 'w', encoding='utf-8') as file:
                json.dump({}, file)

        with open(Customer.customers_file, 'r+', encoding='utf-8') as file:
            customers = json.load(file)
            customers[self.customer_id] = {
                "name": self.name,
                "email": self.email
            }
            file.seek(0)
            json.dump(customers, file, indent=4)

    @staticmethod
    def delete(customer_id):
        """Delete a customer by ID from the JSON file."""
        if not os.path.isfile(Customer.customers_file):
            print("Customers file not found.")
            return

        with open(Customer.customers_file, 'r+', encoding='utf-8') as file:
            customers = json.load(file)
            if customer_id in customers:
                del customers[customer_id]
                file.seek(0)
                file.truncate()
                json.dump(customers, file, indent=4)
            else:
                print("Customer not found.")

    @staticmethod
    def get_all_customers():
        """Return all customers from the JSON file."""
        if not os.path.isfile(Customer.customers_file):
            return {}
        with open(Customer.customers_file, 'r', encoding='utf-8') as file:
            customers = json.load(file)
        return customers

    @staticmethod
    def display_info(customer_id):
        """Display information for a specific customer."""
        customers = Customer.get_all_customers()
        if customer_id in customers:
            customer = customers[customer_id]
            print(
                f"""Customer ID: {customer_id},
                Name: {customer['name']},
                Email: {customer['email']}"""
                )
        else:
            print("Customer not found.")


def main():
    """Main when called from terminal"""
    parser = argparse.ArgumentParser(description="Customer Management CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Create customer command
    create_parser = subparsers.add_parser(
        'create', help='Create a new customer'
        )
    create_parser.add_argument('customer_id', type=str, help='Customer ID')
    create_parser.add_argument('name', type=str, help='Name of the customer')
    create_parser.add_argument('email', type=str, help='Email of the customer')

    # Delete customer command
    delete_parser = subparsers.add_parser('delete', help='Delete a customer')
    delete_parser.add_argument('customer_id', type=str, help='Customer ID')

    # Display customer info command
    display_parser = subparsers.add_parser(
        'display', help='Display customer information'
        )
    display_parser.add_argument('customer_id', type=str, help='Customer ID')

    args = parser.parse_args()

    if args.command == 'create':
        customer = Customer(args.customer_id, args.name, args.email)
        customer.save()
        print(f"Customer {args.name} created successfully.")

    elif args.command == 'delete':
        Customer.delete(args.customer_id)
        print(f"Customer {args.customer_id} deleted successfully.")

    elif args.command == 'display':
        Customer.display_info(args.customer_id)


if __name__ == '__main__':
    main()
