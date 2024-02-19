# hotel.py
"""This code handles hotels"""

import json
import os
import argparse

class Hotel:
    hotels_file = 'hotels.json'

    def __init__(self, hotel_id, name, location, rooms):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        # Assume rooms is a dict: {room_number: {"available": True, "customer_id": None}}
        self.rooms = rooms

    def save(self):
        """Save the hotel to the JSON file."""
        if not os.path.isfile(Hotel.hotels_file):
            with open(Hotel.hotels_file, 'w', encoding='utf-8') as file:
                json.dump({}, file)

        with open(Hotel.hotels_file, 'r+', encoding='utf-8') as file:
            hotels = json.load(file)
            hotels[self.hotel_id] = {
                "name": self.name,
                "location": self.location,
                "rooms": self.rooms
            }
            file.seek(0)
            json.dump(hotels, file, indent=4)

    @staticmethod
    def delete(hotel_id):
        """Delete a hotel by ID from the JSON file."""
        if not os.path.isfile(Hotel.hotels_file):
            print("Hotels file not found.")
            return

        with open(Hotel.hotels_file, 'r+', encoding='utf-8') as file:
            hotels = json.load(file)
            if hotel_id in hotels:
                del hotels[hotel_id]
                file.seek(0)
                file.truncate()
                json.dump(hotels, file, indent=4)
            else:
                print("Hotel not found.")

    @staticmethod
    def get_all_hotels():
        """Return all hotels from the JSON file."""
        if not os.path.isfile(Hotel.hotels_file):
            return {}
        with open(Hotel.hotels_file, 'r', encoding='utf-8') as file:
            hotels = json.load(file)
        return hotels

    @staticmethod
    def display_info(hotel_id):
        """Display information for a specific hotel."""
        hotels = Hotel.get_all_hotels()
        if hotel_id in hotels:
            hotel = hotels[hotel_id]
            print(f"Hotel ID: {hotel_id}, Name: {hotel['name']}, Location: {hotel['location']}, Rooms: {hotel['rooms']}")
        else:
            print("Hotel not found.")


def main():
    """Main when called from terminal"""
    parser = argparse.ArgumentParser(description="Hotel Management CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Create hotel command
    create_parser = subparsers.add_parser('create', help='Create a new hotel')
    create_parser.add_argument('hotel_id', type=str, help='Hotel ID')
    create_parser.add_argument('name', type=str, help='Name of the hotel')
    create_parser.add_argument('location', type=str, help='Location of the hotel')
    create_parser.add_argument('--rooms', type=json.loads, default='{}', help='JSON string of rooms')

    # Delete hotel command
    delete_parser = subparsers.add_parser('delete', help='Delete a hotel')
    delete_parser.add_argument('hotel_id', type=str, help='Hotel ID')

    # Display hotel info command
    display_parser = subparsers.add_parser('display', help='Display hotel information')
    display_parser.add_argument('hotel_id', type=str, help='Hotel ID')

    args = parser.parse_args()

    if args.command == 'create':
        hotel = Hotel(args.hotel_id, args.name, args.location, args.rooms)
        hotel.save()
        print(f"Hotel {args.name} created successfully.")

    elif args.command == 'delete':
        Hotel.delete(args.hotel_id)
        print(f"Hotel {args.hotel_id} deleted successfully.")

    elif args.command == 'display':
        Hotel.display_info(args.hotel_id)

if __name__ == '__main__':
    main()