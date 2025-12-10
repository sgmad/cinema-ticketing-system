class Showtime:
    def __init__(self, id, movie_id, hall_id, hall_name, start_time, price, total_rows=10, total_cols=14):
        self.id = id
        self.movie_id = movie_id
        self.hall_id = hall_id
        self.hall_name = hall_name
        self.start_time = start_time
        self.price = price
        # Attributes for Seat Map
        self.total_rows = total_rows
        self.total_cols = total_cols

    def get_formatted_time(self):
        return self.start_time.strftime("%I:%M %p")

    def get_formatted_date(self):
        return self.start_time.strftime("%A, %d %B")
        
    def get_formatted_price(self):
        return f"₱{self.price}"