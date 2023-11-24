# test_main.py

from ReservationApp import ReservationApp
def test_book_a_seat():
    data_file = "test_seats.json"
    reservation_app = ReservationApp(data_file)

    # Test adding a seat: after reserve one seat, the seat list should be 1 
    reservation_app.add_seat("3", "Dou", "Finance")
    seats = reservation_app.view_seats()
    try:
        assert len(seats) == 1
        print("Testing the booking of a seat: PASS")
    except AssertionError:
         print(f"Test failed: Expected 'not 1', but got '{ len(seats)}'")

test_book_a_seat() 

def test_delete_a_seat():
    data_file = "test_seats.json"
    reservation_app = ReservationApp(data_file)

    # Test deleting a seat: first add one seat to empty list, then eliminate it , then the it should be  0 
    reservation_app.add_seat("3", "Dou", "Finance")
    seats = reservation_app.view_seats()  # Retrieve seats after adding
    request_id = seats[0].request_id
    reservation_app.delete_seat(request_id)
    seats = reservation_app.view_seats()  # Retrieve seats after deleting
    try:
         assert len(seats) == 0
         print("Testing the deletion of a seat: PASS")
    except AssertionError:
         print(f"Test failed: Expected 'not 0', but got '{len(seats)}'")

test_delete_a_seat()

