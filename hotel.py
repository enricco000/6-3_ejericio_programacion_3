# hotel.py
"""This code handles hotels"""

import json
import os
import argparse

class Hotel:
    """Hotel class for the system"""
    hotels_file = 'hotels.json'

    def __init__(self, hotel_id, name, location, rooms):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        # Assume rooms is a dict: {room_number: {"available": True, "customer_id": None}}
        self.rooms = rooms

    def save(self):
        """Save the hotel to the JSON file."""
        hotels = {}
        if os.path.isfile(Hotel.hotels_file):
            with open(Hotel.hotels_file, 'r', encoding='utf-8') as file:
                try:
                    hotels = json.load(file)
                except json.JSONDecodeError:
                    print("Warning: Existing hotels file is corrupted and will be overwritten.")
        hotels[self.hotel_id] = {
            "name": self.name,
            "location": self.location,
            "rooms": self.rooms
        }
        with open(Hotel.hotels_file, 'w', encoding='utf-8') as file:
            json.dump(hotels, file, indent=4)

    @staticmethod
    def delete(hotel_id):
        """Delete a hotel by ID from the JSON file."""
        if not os.path.isfile(Hotel.hotels_file):
            print("Hotels file not found.")
            return
        with open(Hotel.hotels_file, 'r+', encoding='utf-8') as file:
            try:
                hotels = json.load(file)
            except json.JSONDecodeError:
                print("Error: hotels file is corrupted.")
                return
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
            try:
                hotels = json.load(file)
            except json.JSONDecodeError:
                print("Error: hotels file is corrupted.")
                return {}
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

    def add_room(self, room_number, available=True, customer_id=None):
        """Add a new room to the hotel."""
        self.rooms[room_number] = {"available": available, "customer_id": customer_id}
        self.save()

    def remove_room(self, room_number):
        """Remove a room from the hotel."""
        if room_number in self.rooms:
            del self.rooms[room_number]
            self.save()
        else:
            print(f"Room {room_number} not found in hotel {self.hotel_id}.")

def main():
    """Main function when called from terminal"""
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
