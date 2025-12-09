import mysql.connector

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.config = {
                'host': 'localhost',
                'database': 'cinema_db',
                'user': 'root',
                'password': ''
            }
        return cls._instance

    def get_connection(self):
        return mysql.connector.connect(**self._instance.config)

    # =========================================================
    # AUTH
    # =========================================================
    def check_admin_login(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s AND password = %s AND role = 'admin'"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn.close()
        return user

    # =========================================================
    # MOVIE CRUD
    # =========================================================
    def fetch_all_movies(self):
        from models.movie import Movie
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movies ORDER BY id DESC")
        results = cursor.fetchall()
        conn.close()
        
        movies = []
        for r in results:
            m = Movie(
                id=r['id'],
                title=r['title'],
                genre=r['genre'],
                duration=r['duration_minutes'],
                rating=r['rating'],
                imdb_rating=r['imdb_rating'],
                description=r['description'],
                poster_path=r['poster_path'],
                tagline=r['review'],
                cast=r['cast'],
                director=r['director']
            )
            movies.append(m)
        return movies

    def get_movie_by_id(self, movie_id):
        from models.movie import Movie
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
        r = cursor.fetchone()
        conn.close()
        
        if r:
            return Movie(
                id=r['id'],
                title=r['title'],
                genre=r['genre'],
                duration=r['duration_minutes'],
                rating=r['rating'],
                imdb_rating=r['imdb_rating'],
                description=r['description'],
                poster_path=r['poster_path'],
                tagline=r['review'],
                cast=r['cast'],
                director=r['director']
            )
        return None

    def add_movie(self, title, genre, duration, rating, imdb, tagline, desc, poster_path):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = """INSERT INTO movies (title, genre, duration_minutes, rating, description, poster_path, review, imdb_rating) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            vals = (title, genre, duration, rating, desc, poster_path, tagline, imdb)
            cursor.execute(query, vals)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding movie: {e}")
            return False
        finally:
            conn.close()

    def update_movie(self, m_id, title, genre, duration, rating, imdb, tagline, desc, poster_path=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            if poster_path:
                query = """UPDATE movies SET title=%s, genre=%s, duration_minutes=%s, rating=%s, description=%s, poster_path=%s, review=%s, imdb_rating=%s WHERE id=%s"""
                vals = (title, genre, duration, rating, desc, poster_path, tagline, imdb, m_id)
            else:
                query = """UPDATE movies SET title=%s, genre=%s, duration_minutes=%s, rating=%s, description=%s, review=%s, imdb_rating=%s WHERE id=%s"""
                vals = (title, genre, duration, rating, desc, tagline, imdb, m_id)
            
            cursor.execute(query, vals)
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating movie: {e}")
            return False
        finally:
            conn.close()

    def delete_movie(self, movie_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    def fetch_movies_by_date(self, date_str):
        from models.movie import Movie
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT DISTINCT m.* FROM movies m
        JOIN showtimes s ON m.id = s.movie_id
        WHERE DATE(s.start_time) = %s
        """
        cursor.execute(query, (date_str,))
        results = cursor.fetchall()
        conn.close()

        movies = []
        for r in results:
            m = Movie(
                id=r['id'],
                title=r['title'],
                genre=r['genre'],
                duration=r['duration_minutes'],
                rating=r['rating'],
                imdb_rating=r['imdb_rating'],
                description=r['description'],
                poster_path=r['poster_path'],
                tagline=r['review'],
                cast=r['cast'],
                director=r['director']
            )
            movies.append(m)
        return movies

    # =========================================================
    # HALL MANAGEMENT
    # =========================================================
    def fetch_all_halls(self):
        from models.hall import hall_factory 
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM halls")
        rows = cursor.fetchall()
        conn.close()

        hall_objects = []
        for r in rows:
            obj = hall_factory(r['id'], r['name'], r['total_rows'], r['total_cols'])
            hall_objects.append(obj)
        
        return hall_objects
    
    def add_hall(self, name, rows, cols):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO halls (name, total_rows, total_cols) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, rows, cols))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding hall: {e}")
            return False
        finally:
            conn.close()

    def update_hall(self, hall_id, name, rows, cols):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = "UPDATE halls SET name=%s, total_rows=%s, total_cols=%s WHERE id=%s"
            cursor.execute(query, (name, rows, cols, hall_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating hall: {e}")
            return False
        finally:
            conn.close()

    def delete_hall(self, hall_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM halls WHERE id = %s", (hall_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting hall: {e}")
            return False
        finally:
            conn.close()

    # =========================================================
    # SHOWTIME MANAGEMENT
    # =========================================================
    def fetch_all_showtimes_full(self):
        from models.showtime import Showtime
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT s.id, s.start_time, s.price_standard, 
               m.title as movie_title, h.name as hall_name
        FROM showtimes s
        JOIN movies m ON s.movie_id = m.id
        JOIN halls h ON s.hall_id = h.id
        ORDER BY s.start_time DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        
        cleaned = []
        for r in results:
            s = Showtime(r['id'], None, None, r['hall_name'], r['start_time'], r['price_standard'])
            s.movie_title = r['movie_title'] 
            cleaned.append(s)
        return cleaned

    def fetch_showtimes_by_movie(self, movie_id):
        from models.showtime import Showtime
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT s.id, s.movie_id, s.hall_id, s.start_time, s.price_standard, 
               h.name as hall_name, h.total_rows, h.total_cols
        FROM showtimes s
        JOIN halls h ON s.hall_id = h.id
        WHERE s.movie_id = %s
        AND s.start_time >= NOW()
        ORDER BY s.start_time ASC
        """
        cursor.execute(query, (movie_id,))
        results = cursor.fetchall()
        conn.close()

        showtimes = []
        for r in results:
            s = Showtime(
                id=r['id'],
                movie_id=r['movie_id'],
                hall_id=r['hall_id'],
                hall_name=r['hall_name'],
                start_time=r['start_time'],
                price=r['price_standard'],
                total_rows=r['total_rows'],
                total_cols=r['total_cols']
            )
            showtimes.append(s)
        return showtimes

    def delete_showtime(self, showtime_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM showtimes WHERE id = %s", (showtime_id,))
            conn.commit()
            return True
        except:
            return False
        finally:
            conn.close()

    def check_conflict(self, hall_id, start_dt, movie_id, ignore_id=None):
        from datetime import timedelta
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT duration_minutes FROM movies WHERE id = %s", (movie_id,))
        res = cursor.fetchone()
        if not res: return True, "Invalid Movie"
        
        duration = res['duration_minutes']
        end_dt = start_dt + timedelta(minutes=duration + 20)

        query = """
        SELECT s.id, s.start_time, m.title, m.duration_minutes 
        FROM showtimes s
        JOIN movies m ON s.movie_id = m.id
        WHERE s.hall_id = %s 
        AND DATE(s.start_time) = %s
        """
        cursor.execute(query, (hall_id, start_dt.date()))
        existing = cursor.fetchall()
        conn.close()

        for show in existing:
            if ignore_id and show['id'] == ignore_id: continue
            s_start = show['start_time']
            s_end = s_start + timedelta(minutes=show['duration_minutes'] + 20)
            if (start_dt < s_end) and (end_dt > s_start):
                return True, "Conflict Detected"
        
        return False, None

    def add_showtime(self, movie_id, hall_id, start_dt, price):
        is_conflict, msg = self.check_conflict(hall_id, start_dt, movie_id)
        if is_conflict: return False, msg

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO showtimes (movie_id, hall_id, start_time, price_standard) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (movie_id, hall_id, start_dt, price))
            conn.commit()
            return True, "Success"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    def update_showtime(self, showtime_id, movie_id, hall_id, start_dt, price):
        is_conflict, msg = self.check_conflict(hall_id, start_dt, movie_id, ignore_id=showtime_id)
        if is_conflict: return False, msg

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = "UPDATE showtimes SET movie_id=%s, hall_id=%s, start_time=%s, price_standard=%s WHERE id=%s"
            cursor.execute(query, (movie_id, hall_id, start_dt, price, showtime_id))
            conn.commit()
            return True, "Success"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    # =========================================================
    # BOOKING & TICKETS (STRICTLY MATCHING 3NF SCHEMA)
    # =========================================================
    
    def get_taken_seats(self, showtime_id):
        # Queries the TICKETS table directly
        # Uses 'row_letter' and 'seat_num' (matches nuke_and_rebuild.py)
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT row_letter, seat_num FROM tickets WHERE showtime_id = %s"
        
        cursor.execute(query, (showtime_id,))
        taken = cursor.fetchall()
        conn.close()
        return taken

    def create_booking(self, showtime_id, customer_name, seat_list, total_price):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # 1. CREATE BOOKING HEADER
            # (No showtime_id in bookings table)
            insert_booking = "INSERT INTO bookings (customer_name, ticket_count, total_amount) VALUES (%s, %s, %s)"
            cursor.execute(insert_booking, (customer_name, len(seat_list), total_price))
            booking_id = cursor.lastrowid

            # 2. CREATE TICKET LINE ITEMS
            # Uses 'row_letter' and 'seat_num'
            unit_price = total_price / len(seat_list) if seat_list else 0
            insert_ticket = "INSERT INTO tickets (booking_id, showtime_id, row_letter, seat_num, price_at_purchase) VALUES (%s, %s, %s, %s, %s)"
            
            for row, num in seat_list:
                cursor.execute(insert_ticket, (booking_id, showtime_id, row, num, unit_price))
            
            conn.commit()
            return booking_id
        except Exception as e:
            print(f"Booking Error: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    def fetch_all_bookings(self):
        from models.booking import Booking
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # 3NF JOIN: Bookings -> Tickets -> Showtimes -> Movies
        # We join to get the Movie Title via the tickets
        query = """
        SELECT 
            b.id, 
            b.booking_date, 
            b.customer_name, 
            b.ticket_count, 
            b.total_amount,
            m.title as movie_title
        FROM bookings b
        JOIN tickets t ON t.booking_id = b.id
        JOIN showtimes s ON t.showtime_id = s.id
        JOIN movies m ON s.movie_id = m.id
        GROUP BY b.id
        ORDER BY b.booking_date DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        bookings = []
        for r in results:
            b = Booking(
                r['id'], r['booking_date'], r['customer_name'],
                r['movie_title'], r['ticket_count'], r['total_amount']
            )
            bookings.append(b)
        return bookings

    def delete_booking(self, booking_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            # CASCADE DELETE is on, but explicit delete is safer for logic
            cursor.execute("DELETE FROM tickets WHERE booking_id = %s", (booking_id,))
            cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
            conn.commit()
            return True
        except: return False
        finally: conn.close()