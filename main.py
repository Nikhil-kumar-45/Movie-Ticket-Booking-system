from collections import deque


class MovieTicketSystem:

    def _init_(self):
        # Movie details and seat arrays
        self.movies = {
            "1": {
                "name": "Interstellar",
                "price": 200,
                "seats": ["O"] * 10
            },
            "2": {
                "name": "Inception",
                "price": 180,
                "seats": ["O"] * 10
            },
            "3": {
                "name": "The Dark Knight",
                "price": 150,
                "seats": ["O"] * 10
            }
        }

        # Queue for customers waiting for each movie
        self.waiting_queues = {
            movie["name"]: deque()
            for movie in self.movies.values()
        }

        # Dictionary to store active bookings
        self.bookings = {}

        # Booking ID counter
        self.booking_counter = 1

    # Display all movies
    def display_movies(self):
        print("\n========== AVAILABLE MOVIES ==========")

        for key, movie in self.movies.items():
            print(
                key + ". " + movie["name"]
                + " | Ticket Price: Rs."
                + str(movie["price"])
            )

    # Select a movie
    def select_movie(self):
        self.display_movies()

        choice = input("\nEnter movie number: ").strip()

        if choice in self.movies:
            return self.movies[choice]

        print("Invalid movie selection!")
        return None

    # Display seats for a movie
    def display_seats(self):
        movie = self.select_movie()

        if movie is None:
            return

        print("\nSeats for", movie["name"])
        print("O = Available, X = Booked")

        for i, seat in enumerate(movie["seats"], start=1):
            print(str(i) + ":" + seat, end="   ")

        print()

    # Create a booking
    def create_booking(self, customer, movie, seat_number):
        booking_id = "B" + str(self.booking_counter).zfill(3)
        self.booking_counter += 1

        booking = {
            "customer": customer,
            "movie": movie["name"],
            "seat": seat_number,
            "price": movie["price"]
        }

        self.bookings[booking_id] = booking

        # Mark the seat as booked
        movie["seats"][seat_number - 1] = "X"

        print("\nTicket booked successfully!")
        print("Booking ID:", booking_id)
        print("Customer:", customer)
        print("Movie:", movie["name"])
        print("Seat Number:", seat_number)
        print("Ticket Price: Rs.", movie["price"])

    # Book a ticket
    def book_ticket(self):
        movie = self.select_movie()

        if movie is None:
            return

        customer = input("Enter customer name: ").strip()

        if not customer:
            print("Customer name cannot be empty!")
            return

        seats = movie["seats"]

        # Check whether all seats are booked
        if "O" not in seats:
            print("\nSorry, all seats are booked!")

            choice = input(
                "Would you like to join the waiting queue? (yes/no): "
            ).strip().lower()

            if choice == "yes":
                queue = self.waiting_queues[movie["name"]]

                queue.append(customer)

                print(customer, "added to the waiting queue.")
                print("Your queue position is:", len(queue))
            else:
                print("No booking made.")

            return

        # Display available seats
        print("\nAvailable seats:")

        for i, seat in enumerate(seats, start=1):
            if seat == "O":
                print(i, end="  ")

        print()

        try:
            seat_number = int(input("Enter seat number (1-10): "))
        except ValueError:
            print("Please enter a valid number!")
            return

        if seat_number < 1 or seat_number > len(seats):
            print("Invalid seat number!")
            return

        if seats[seat_number - 1] == "X":
            print("This seat is already booked!")
            return

        self.create_booking(customer, movie, seat_number)

    # Display all active bookings
    def display_bookings(self):
        print("\n========== ACTIVE BOOKINGS ==========")

        if not self.bookings:
            print("No active bookings.")
            return

        for booking_id, booking in self.bookings.items():
            print(
                "Booking ID:", booking_id,
                "| Customer:", booking["customer"],
                "| Movie:", booking["movie"],
                "| Seat:", booking["seat"],
                "| Price: Rs.", booking["price"]
            )

    # Search for a booking
    def search_booking(self):
        booking_id = input("Enter booking ID: ").strip().upper()

        if booking_id in self.bookings:
            booking = self.bookings[booking_id]

            print("\nBooking Found!")
            print("Booking ID:", booking_id)
            print("Customer:", booking["customer"])
            print("Movie:", booking["movie"])
            print("Seat:", booking["seat"])
            print("Price: Rs.", booking["price"])
        else:
            print("Booking not found!")

    # Cancel a booking
    def cancel_ticket(self):
        booking_id = input("Enter booking ID to cancel: ").strip().upper()

        if booking_id not in self.bookings:
            print("Invalid booking ID!")
            return

        # Remove the booking record
        booking = self.bookings.pop(booking_id)

        movie_name = booking["movie"]
        seat_number = booking["seat"]

        # Find the corresponding movie
        movie = None

        for item in self.movies.values():
            if item["name"] == movie_name:
                movie = item
                break

        # Release the cancelled seat
        movie["seats"][seat_number - 1] = "O"

        print("\nTicket cancelled successfully!")
        print("Released seat:", seat_number)
        print("Movie:", movie_name)

        # Give the released seat to the first waiting customer
        queue = self.waiting_queues[movie_name]

        if queue:
            next_customer = queue.popleft()

            print("\nA waiting customer will receive the released seat.")

            self.create_booking(
                next_customer,
                movie,
                seat_number
            )

    # Display waiting queue
    def display_waiting_queue(self):
        movie = self.select_movie()

        if movie is None:
            return

        queue = self.waiting_queues[movie["name"]]

        print("\nWaiting Queue for", movie["name"])

        if not queue:
            print("No customers in the waiting queue.")
            return

        for position, customer in enumerate(queue, start=1):
            print(str(position) + ".", customer)

    # Display sales summary
    def sales_summary(self):
        print("\n========== SALES SUMMARY ==========")

        total_tickets = len(self.bookings)
        total_sales = sum(
            booking["price"]
            for booking in self.bookings.values()
        )

        print("Active Tickets:", total_tickets)
        print("Total Active Booking Value: Rs.", total_sales)

        print("\nMovie-wise seat status:")

        for movie in self.movies.values():
            booked = movie["seats"].count("X")
            available = movie["seats"].count("O")

            print("\nMovie:", movie["name"])
            print("Booked Seats:", booked)
            print("Available Seats:", available)

    # Main menu
    def run(self):
        while True:
            print("\n========== MOVIE TICKET BOOKING SYSTEM ==========")
            print("1. Display Movies")
            print("2. Display Seats")
            print("3. Book Ticket")
            print("4. View All Bookings")
            print("5. Search Booking")
            print("6. Cancel Ticket")
            print("7. View Waiting Queue")
            print("8. Sales Summary")
            print("9. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.display_movies()

            elif choice == "2":
                self.display_seats()

            elif choice == "3":
                self.book_ticket()

            elif choice == "4":
                self.display_bookings()

            elif choice == "5":
                self.search_booking()

            elif choice == "6":
                self.cancel_ticket()

            elif choice == "7":
                self.display_waiting_queue()

            elif choice == "8":
                self.sales_summary()

            elif choice == "9":
                print("Thank you for using the Movie Ticket Booking System!")
                break

            else:
                print("Invalid choice! Please select 1-9.")


# Create an object and run the system
system = MovieTicketSystem()
system.run()