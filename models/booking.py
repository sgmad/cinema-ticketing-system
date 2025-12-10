class Booking:
    def __init__(self, id, booking_date, customer_name, movie_title, ticket_count, total_amount):
        self.id = id
        self.booking_date = booking_date
        self.customer_name = customer_name
        self.movie_title = movie_title
        self.ticket_count = ticket_count
        self.total_amount = total_amount

    def get_formatted_date(self):
        return self.booking_date.strftime("%Y-%m-%d  %H:%M")

    def get_formatted_total(self):
        return f"₱{self.total_amount:,.2f}"