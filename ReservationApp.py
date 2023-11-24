import json
import os
import uuid
import requests
from Seat import Seat
import streamlit as st
class ReservationApp:
    def __init__(self, data_file):
        self.data_file = data_file # the file path to the JSON file storing reservation data
        self.seats = self.load_seats() # load reservation data from the JSON file and store it in the seats attribute.load_seats(self):



    def load_seats(self):
        if os.path.exists(self.data_file):#checks if the file specified by self.data_file exists.
            with open(self.data_file, "r") as file: # opens the file in read mode ("r") and uses the json.load function to load the data from the file.
                loaded_seats = json.load(file)
                return [Seat(**seat_data) if "request_id" in seat_data else Seat(str(uuid.uuid4()), **seat_data) for seat_data in loaded_seats]#The method returns a list of Seat objects, representing the reservations stored in the file.
        else:
            return [] #If the file does not exist, an empty list is returned since there is no reservation data to load.

    def save_seats(self):
        with open(self.data_file, "w") as file:
            json.dump([seat.__dict__ for seat in self.seats], file, indent=2) #to serialize the seat reservation data and write it to the opened file.
            #List comprehension that converts each Seat object in the self.seats list to a dictionary using the __dict__ attribute. The __dict__ attribute contains the object's attributes and their values.
            #file: The file object to which the JSON data will be written.
            #indent=2: This argument specifies the number of spaces to use for indentation in the JSON output. In this case, it uses 2 spaces for better human readability.

    def add_seat(self, description, name, department):
        if not description.isdigit():
            st.warning("Please enter a valid integer for the seat number.")
            return

        # Check if the seat is already booked
        if any(seat.description == int(description) for seat in self.seats):
            st.warning(f"The seat {int(description)} is already booked. Please choose another seat.")
            freelist = list(range(1, 10))
            booked_seats = [seat.description for seat in self.seats]
            available_seats = [seat for seat in freelist if seat not in booked_seats]
            st.warning(f"Booked seats: {', '.join(map(str, booked_seats))}")
            st.warning(f"Available seats: {', '.join(map(str, available_seats))}")
            return

        if len(self.seats) >= 9:
            st.warning("Maximum number of seats reached. Cannot add more.")
        else:
            st.balloons()
            request_id = str(uuid.uuid4())  # generate a unique request ID
            st.success(f"Place booked successfully! Your request ID is {request_id}")

            # Fetch a meme from the Meme API
            meme_api_url = "https://meme-api.com/gimme"
            meme_response = requests.get(meme_api_url)
            meme_data = meme_response.json()

            if meme_response.status_code == 200:
                meme_url = meme_data['url']
                st.image(meme_url, caption="Random Meme from Meme API")
            else:
                st.warning("Failed to fetch meme from the Meme API.")

            seat = Seat(request_id, int(description), name, department)
            self.seats.append(seat)
            self.save_seats()

    def view_seats(self):
        return self.seats

    def delete_seat(self, request_id):
        for i, seat in enumerate(self.seats):
            if seat.request_id == request_id:
                st.snow()
                del self.seats[i]
                self.save_seats()
                return True  # successfully deleted
        return False  # request ID not found