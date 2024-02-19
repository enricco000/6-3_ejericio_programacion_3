# reservation.py
"""This code handles reservations"""

import json
import os
import argparse
from hotel import Hotel

class Reservation:
    """Reservation class for the system"""
    reservations_file = 'reservations.json'

    def __init__(self, reservation_id, customer_id, hotel_id, room_number, start_date, end_date):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.room_number = room_number
        self.start_date = start_date
        self.end_date = end_date

    def save(self):
        """Save the reservation to the JSON file and update hotel room status."""
        if not os.path.isfile(Reservation.reservations_file):
            with open(Reservation.reservations_file, 'w', encoding='utf-8') as file:
                json.dump({}, file)

        with open(Reservation.reservations_file, 'r+', encoding='utf-8') as file:
            reservations = json.load(file)
            reservations[self.reservation_id] = {
                "customer_id": self.customer_id,
                "hotel_id": self.hotel_id,
                "room_number": self.room_number,
                "start_date": self.start_date,
                "end_date": self.end_date
            }
            file.seek(0)
            json.dump(reservations, file, indent=4)

        with open(Hotel.hotels_file, 'r+', encoding='utf-8') as file:
            hotels = json.load(file)
            if self.hotel_id in hotels and self.room_number in hotels[self.hotel_id]['rooms']:
                hotels[self.hotel_id]['rooms'][self.room_number]['available'] = False
                hotels[self.hotel_id]['rooms'][self.room_number]['customer_id'] = self.customer_id
                file.seek(0)
                file.truncate()
                json.dump(hotels, file, indent=4)

    @staticmethod
    def cancel(reservation_id):
        """Cancel a reservation and update hotel room status."""
        if not os.path.isfile(Reservation.reservations_file):
            print("Reservations file not found.")
            return False

        with open(Reservation.reservations_file, 'r+', encoding='utf-8') as file:
            reservations = json.load(file)
            if reservation_id in reservations:
                reservation = reservations.pop(reservation_id)
                file.seek(0)
                file.truncate()
                json.dump(reservations, file, indent=4)

                with open(Hotel.hotels_file, 'r+', encoding='utf-8') as file:
                    hotels = json.load(file)
                    hotel_id = reservation['hotel_id']
                    room_number = reservation['room_number']
                    if hotel_id in hotels and room_number in hotels[hotel_id]['rooms']:
                        hotels[hotel_id]['rooms'][room_number]['available'] = True
                        hotels[hotel_id]['rooms'][room_number]['customer_id'] = None
                        file.seek(0)
                        file.truncate()
                        json.dump(hotels, file, indent=4)
                return True
            else:
                print("Reservation not found.")
                return False

    @staticmethod
    def get_all_reservations():
        """Return all reservations from the JSON file."""
        if not os.path.isfile(Reservation.reservations_file):
            return {}
        with open(Reservation.reservations_file, 'r', encoding='utf-8') as file:
            reservations = json.load(file)
        return reservations

def main():
    """Main function when called from terminal"""
    parser = argparse.ArgumentParser(description="Reservation Management CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Create reservation command
    create_parser = subparsers.add_parser('create', help='Create a new reservation')
    create_parser.add_argument('reservation_id', type=str, help='Reservation ID')
    create_parser.add_argument('customer_id', type=str, help='Customer ID')
    create_parser.add_argument('hotel_id', type=str, help='Hotel ID')
    create_parser.add_argument('room_number', type=str, help='Room Number')
    create_parser.add_argument('start_date', type=str, help='Start Date (YYYY-MM-DD)')
    create_parser.add_argument('end_date', type=str, help='End Date (YYYY-MM-DD)')

    # Cancel reservation command
    cancel_parser = subparsers.add_parser('cancel', help='Cancel a reservation')
    cancel_parser.add_argument('reservation_id', type=str, help='Reservation ID')

    args = parser.parse_args()

    if args.command == 'create':
        reservation = Reservation(
            args.reservation_id,
            args.customer_id,
            args.hotel_id,
            args.room_number,
            args.start_date,
            args.end_date
            )
        reservation.save()
        print(f"Reservation {args.reservation_id} created successfully.")

    elif args.command == 'cancel':
        success = Reservation.cancel(args.reservation_id)
        if success:
            print(f"Reservation {args.reservation_id} canceled successfully.")
        else:
            print("Failed to cancel reservation.")

if __name__ == '__main__':
    main()
