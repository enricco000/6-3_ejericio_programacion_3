# populate_data.py
"""To have initial data in our system"""

import json
import argparse

# Default initial data
default_hotels_data = {
    "H001": {
        "name": "Seaside Resort",
        "location": "Ocean View, 123 Beach Lane",
        "rooms": {
            "101": {"available": True, "customer_id": None},
            "102": {"available": True, "customer_id": None},
            "103": {"available": False, "customer_id": "C001"}
        }
    },
    "H002": {
        "name": "Mountain Lodge",
        "location": "Peaktop, 456 Hill Road",
        "rooms": {
            "201": {"available": True, "customer_id": None},
            "202": {"available": False, "customer_id": "C002"},
            "203": {"available": True, "customer_id": None}
        }
    }
}

default_customers_data = {
    "C001": {
        "name": "John Doe",
        "email": "johndoe@example.com"
    },
    "C002": {
        "name": "Jane Smith",
        "email": "janesmith@example.com"
    }
}

default_reservations_data = {
    "R001": {
        "customer_id": "C001",
        "hotel_id": "H001",
        "room_number": "103",
        "start_date": "2024-01-01",
        "end_date": "2024-01-10"
    },
    "R002": {
        "customer_id": "C002",
        "hotel_id": "H002",
        "room_number": "202",
        "start_date": "2024-02-15",
        "end_date": "2024-02-20"
    },
    "R003": {
        "customer_id": "C001",
        "hotel_id": "H002",
        "room_number": "203",
        "start_date": "2024-03-01",
        "end_date": "2024-03-05"
    }
}

def create_or_update_file(file_name, data):
    """Create or update"""
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def main(hotels, customers, reservations):
    """Main entry point"""
    if hotels:
        hotels_data = json.loads(hotels)
    else:
        hotels_data = default_hotels_data

    if customers:
        customers_data = json.loads(customers)
    else:
        customers_data = default_customers_data

    if reservations:
        reservations_data = json.loads(reservations)
    else:
        reservations_data = default_reservations_data

    create_or_update_file('hotels.json', hotels_data)
    create_or_update_file('customers.json', customers_data)
    create_or_update_file('reservations.json', reservations_data)

    print("Data files have been created/updated.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Populate initial data for the hotel management system."
        )
    parser.add_argument('--hotels', type=str, help='JSON string of hotels data')
    parser.add_argument('--customers', type=str, help='JSON string of customers data')
    parser.add_argument('--reservations', type=str, help='JSON string of reservations data')

    args = parser.parse_args()
    main(args.hotels, args.customers, args.reservations)
