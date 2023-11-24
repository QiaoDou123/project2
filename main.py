
import streamlit as st
from ReservationApp import ReservationApp
from datetime import datetime
from datetime import datetime, timedelta


def main():
    # Set Streamlit theme
    
    st.set_page_config(page_title="Seat Booking System", page_icon="✨")
        

    st.title("🪑 Seat Booking System")

    data_file = "seats.json"
    reservation_app = ReservationApp(data_file)
    current_datetime = datetime.now()
    current_day = current_datetime.strftime("%A, %Y-%m-%d")
    next_day_datetime = current_datetime + timedelta(days=1)
    next_day = next_day_datetime.strftime("%A, %Y-%m-%d ")


    st.sidebar.header(f" Ahoy there!😄 \n Today is {current_day}.")
    st.sidebar.header(" Any plan for tommorow?")
    menu = st.sidebar.radio("Choose an option", ["View booked seats", "Book a seat", "Cancel reservation", "My Bookings"])

    if menu == "Book a seat":
        st.sidebar.image("gif/work.gif", use_column_width=True, caption="")
        st.subheader(f"Reserve Your Seat for tommorow {next_day}")
        number = st.text_input("Enter the seat number you want to reserve:")
        name = st.text_input("Your Name:")
        department = st.text_input("Your Department:")

        if st.button("Reserve"):
            if not (number and name and department):
                st.warning("Please fill in all the fields.", icon="⚠️")
            else:
                reservation_app.add_seat(number, name, department)

    elif menu == "View booked seats":
        seats = reservation_app.view_seats()
        st.sidebar.image("gif/how.gif", use_column_width=True, caption="")
        if seats:
            freelist = list(range(1, 10))
            st.subheader(f" Tommorow is {next_day}")
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🔒 Seats Reserved:")
                for i, seat in enumerate(seats):
                    if i == 8:
                        st.warning("Sorry, all seats are booked.", icon="⚠️")
                    else:
                        st.write(f" Request{i + 1}: Table {seat.description} booked by {seat.name} from {seat.department} department)")
                        if seat.description in freelist:
                            freelist.remove(seat.description)
                st.info(f"🟢 Free seats: {', '.join(map(str, freelist))}")

            with col2:
                
                
                st.subheader("Current Seat Reservation :")
                for i in range(3):
                    row = ""
                    for j in range(3):
                        seat_number = i * 3 + j + 1
                        if seat_number in freelist:
                            row += f"<div style='background-color:#ADD8E6; border-radius: 10px; padding: 20px; margin: 10px; display: inline-block; text-align: center;'>{seat_number}</div>"
                        else:
                            row += f"<div style='background-color: #FFFF99; border-radius: 10px; padding: 20px; margin: 10px; display: inline-block; text-align: center;'>{seat_number}</div>"
                    st.markdown(row, unsafe_allow_html=True)

        else:
            st.info("No seat has been booked.")

    elif menu == "Cancel reservation":
        st.subheader(f"Cancel Reservation for tommorow {next_day}:")
        st.text("Before canceling your reservation, find your Request ID in the 'My Bookings' section.")
        seats = reservation_app.view_seats()
        st.sidebar.image("gif/g.jpeg", use_column_width=True, caption="")


        if seats:
            selected_request_id = st.text_input("Enter your Request ID for cancellation:")
            if st.button("Cancel Reservation"):
                if reservation_app.delete_seat(selected_request_id):
                    st.success("Reservation canceled successfully!", icon="🗑️")
                else:
                    st.warning("Invalid Request ID. Please enter a valid one.", icon="⚠️")
        else:
            st.info("No seats have been booked.", icon="⚠️")

    elif menu == "My Bookings":
        st.subheader(f"My Bookings for tommorow {next_day}:")
        my_bookings = reservation_app.view_seats()
        st.sidebar.image("gif/m.gif", use_column_width=True, caption="")
        if my_bookings:
            for i, seat in enumerate(my_bookings):
                st.success(f"Table {seat.description} booked by {seat.name} from {seat.department} (Request ID: {seat.request_id})", icon="🎉")
        else:
            st.info("You haven't booked any seats yet.")

if __name__ == "__main__":
    main()