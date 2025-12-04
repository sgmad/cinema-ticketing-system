from db.connection import create_connection
from datetime import timedelta

# =====================================================
# MOVIE MANAGEMENT (ADMIN)
# =====================================================

def add_movie(title, genre, duration, rating, description, poster_path):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = """
        INSERT INTO movies (title, genre, duration_minutes, rating, description, poster_path)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (title, genre, duration, rating, description, poster_path)
        try:
            cursor.execute(query, values)
            conn.commit()
            print("Movie added successfully!")
            return True
        except Exception as e:
            print(f"Error adding movie: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

def delete_movie(movie_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Delete associated showtimes first (Cleanup)
            cursor.execute("DELETE FROM showtimes WHERE movie_id = %s", (movie_id,))
            
            # Delete the movie
            cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting movie: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

def get_all_movies():
    """ Used by both Admin (list view) and Customer (home screen) """
    conn = create_connection()
    movies = []
    if conn:
        cursor = conn.cursor(dictionary=True) # Return results as dictionaries
        cursor.execute("SELECT * FROM movies ORDER BY id DESC")
        movies = cursor.fetchall()
        cursor.close()
        conn.close()
    return movies

def get_all_halls():
    conn = create_connection()
    halls = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM halls")
        halls = cursor.fetchall()
        cursor.close()
        conn.close()
    return halls

def get_movies_by_date(target_date_str):
    """
    target_date_str format: 'YYYY-MM-DD'
    Returns list of movies playing on that specific date.
    """
    conn = create_connection()
    movies = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        # distinct: ensures we don't get the same movie twice if it plays 5 times that day
        query = """
        SELECT DISTINCT m.* FROM movies m
        JOIN showtimes s ON m.id = s.movie_id
        WHERE DATE(s.start_time) = %s
        ORDER BY m.title
        """
        cursor.execute(query, (target_date_str,))
        movies = cursor.fetchall()
        cursor.close()
        conn.close()
    return movies

# =====================================================
# SHOWTIME MANAGEMENT (ADMIN)
# =====================================================

def add_showtime(movie_id, hall_id, start_datetime_str, price):
    # Convert string to datetime object for math
    from datetime import datetime
    start_dt = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S')

    # CHECK CONFLICT
    is_conflict, msg = is_hall_occupied(hall_id, start_dt, movie_id)
    if is_conflict:
        return False, msg # Return the error message

    # Proceed if safe
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "INSERT INTO showtimes (movie_id, hall_id, start_time, price_standard) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (movie_id, hall_id, start_datetime_str, price))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Success"
    return False, "DB Error"

def get_showtimes_for_movie(movie_id):
    conn = create_connection()
    results = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        # CHANGED: Added h.total_rows and h.total_cols to the SELECT
        query = """
        SELECT s.id, s.start_time, s.price_standard, 
               h.name as hall_name, h.total_rows, h.total_cols
        FROM showtimes s
        JOIN halls h ON s.hall_id = h.id
        WHERE s.movie_id = %s AND s.start_time >= NOW()
        ORDER BY s.start_time ASC
        """
        cursor.execute(query, (movie_id,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
    return results

def get_taken_seats(showtime_id):
    """ Returns a set of tuples representing taken seats, e.g., {('A', 1), ('A', 2)} """
    conn = create_connection()
    taken_seats = set() # Using a set for fast lookups
    if conn:
        cursor = conn.cursor()
        query = "SELECT seat_row_label, seat_number FROM tickets WHERE showtime_id = %s"
        cursor.execute(query, (showtime_id,))
        rows = cursor.fetchall()
        for r in rows:
            # r[0] is 'A', r[1] is 1
            taken_seats.add((r[0], r[1]))
        cursor.close()
        conn.close()
    return taken_seats

def save_booking(showtime_id, customer_name, seat_list, total_price):
    """
    Saves a booking and its associated tickets in one atomic transaction.
    seat_list is a list of tuples: [('A', 1), ('A', 2)]
    Returns the new booking_id if successful, or None if failed.
    """
    conn = create_connection()
    booking_id = None
    
    if conn:
        cursor = conn.cursor()
        try:
            # 1. Start Transaction
            conn.start_transaction()

            # 2. Create the Booking Record (The Receipt Header)
            query_booking = "INSERT INTO bookings (customer_name, total_amount) VALUES (%s, %s)"
            cursor.execute(query_booking, (customer_name, total_price))
            booking_id = cursor.lastrowid # Get the ID generated (e.g., Booking #101)

            # 3. Create the Ticket Records (The Individual Seats)
            query_ticket = """
            INSERT INTO tickets (booking_id, showtime_id, seat_row_label, seat_number, price)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            # Calculate price per ticket (total / count)
            price_per_ticket = total_price / len(seat_list)

            for row, number in seat_list:
                cursor.execute(query_ticket, (booking_id, showtime_id, row, number, price_per_ticket))

            # 4. Commit (Save everything permanently)
            conn.commit()
            print(f"Transaction successful! Booking ID: {booking_id}")
            
        except Exception as e:
            # If ANYTHING goes wrong, undo everything
            conn.rollback()
            print(f"Transaction failed: {e}")
            booking_id = None
        finally:
            cursor.close()
            conn.close()
            
    return booking_id

# =====================================================
# SCHEDULE MANAGEMENT (CRUD)
# =====================================================

def get_all_showtimes_full():
    """ Fetches all showtimes with Movie and Hall names for the Admin List """
    conn = create_connection()
    results = []
    if conn:
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
        cursor.close()
        conn.close()
    return results

def delete_showtime(showtime_id):
    conn = create_connection()
    success = False
    if conn:
        cursor = conn.cursor()
        try:
            # Note: This will fail if tickets exist for this showtime (Foreign Key Constraint)
            # You might need to delete tickets first if that's desired behavior.
            cursor.execute("DELETE FROM showtimes WHERE id = %s", (showtime_id,))
            conn.commit()
            success = True
        except Exception as e:
            print(f"Error deleting showtime: {e}")
        finally:
            cursor.close()
            conn.close()
    return success

def update_showtime(showtime_id, movie_id, hall_id, start_datetime_str, price):
    from datetime import datetime
    start_dt = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S')

    # CHECK CONFLICT (Pass the ID so we don't conflict with ourselves)
    is_conflict, msg = is_hall_occupied(hall_id, start_dt, movie_id, ignore_showtime_id=showtime_id)
    if is_conflict:
        return False, msg

    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        query = "UPDATE showtimes SET movie_id=%s, hall_id=%s, start_time=%s, price_standard=%s WHERE id=%s"
        cursor.execute(query, (movie_id, hall_id, start_datetime_str, price, showtime_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "Success"
    return False, "DB Error"

# =====================================================
# HALL MANAGEMENT
# =====================================================

def add_hall(name, rows, cols):
    conn = create_connection()
    if conn:
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
            cursor.close()
            conn.close()

def delete_hall(hall_id):
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # 1. Delete associated showtimes first? 
            # Ideally, you shouldn't delete a hall if it has active bookings.
            # For this simple project, we will just try to delete the hall.
            cursor.execute("DELETE FROM halls WHERE id = %s", (hall_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Cannot delete hall (probably has showtimes linked): {e}")
            return False
        finally:
            cursor.close()
            conn.close()

def update_hall(hall_id, name, rows, cols):
    conn = create_connection()
    success = False
    if conn:
        cursor = conn.cursor()
        try:
            # Simple update
            query = "UPDATE halls SET name=%s, total_rows=%s, total_cols=%s WHERE id=%s"
            cursor.execute(query, (name, rows, cols, hall_id))
            conn.commit()
            success = True
        except Exception as e:
            print(f"Error updating hall: {e}")
        finally:
            cursor.close()
            conn.close()
    return success

def is_hall_occupied(hall_id, new_start_dt, movie_id, ignore_showtime_id=None):
    """
    Checks if a new showtime overlaps with existing ones.
    Returns: (True, "Conflict Reason") or (False, None)
    """
    conn = create_connection()
    if not conn: return True, "DB Error"

    cursor = conn.cursor(dictionary=True)
    
    # 1. Get Duration of the NEW movie to calculate its End Time
    cursor.execute("SELECT duration_minutes FROM movies WHERE id = %s", (movie_id,))
    res = cursor.fetchone()
    if not res: return True, "Invalid Movie ID"
    
    new_duration = res['duration_minutes']
    # Add 20 mins for cleaning/trailers buffer
    new_end_dt = new_start_dt + timedelta(minutes=new_duration + 20) 

    # 2. Get all other showtimes for this hall on the same day
    # We fetch their start time AND their specific movie duration
    query = """
    SELECT s.id, s.start_time, m.title, m.duration_minutes 
    FROM showtimes s
    JOIN movies m ON s.movie_id = m.id
    WHERE s.hall_id = %s 
    AND DATE(s.start_time) = %s
    """
    cursor.execute(query, (hall_id, new_start_dt.date()))
    existing_shows = cursor.fetchall()
    
    for show in existing_shows:
        # If we are Editing, skip checking against ourself
        if ignore_showtime_id and show['id'] == ignore_showtime_id:
            continue

        existing_start = show['start_time']
        existing_end = existing_start + timedelta(minutes=show['duration_minutes'] + 20)

        # 3. The Overlap Formula
        # (StartA < EndB) and (EndA > StartB)
        if (new_start_dt < existing_end) and (new_end_dt > existing_start):
            conflict_msg = f"Conflict with '{show['title']}'\n({existing_start.strftime('%H:%M')} - {existing_end.strftime('%H:%M')})"
            return True, conflict_msg

    cursor.close()
    conn.close()
    return False, None

# =====================================================
# BOOKING MANAGEMENT (ADMIN)
# =====================================================

def get_all_bookings():
    """ Fetches all bookings with summary details """
    conn = create_connection()
    results = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        # We join to get the Count of tickets for each booking
        query = """
        SELECT b.id, b.customer_name, b.booking_date, b.total_amount, 
               COUNT(t.id) as ticket_count, m.title
        FROM bookings b
        LEFT JOIN tickets t ON b.id = t.booking_id
        LEFT JOIN showtimes s ON t.showtime_id = s.id
        LEFT JOIN movies m ON s.movie_id = m.id
        GROUP BY b.id
        ORDER BY b.booking_date DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
    return results

def delete_booking(booking_id):
    """ Deletes a booking AND its associated tickets (Cascade delete) """
    conn = create_connection()
    success = False
    if conn:
        cursor = conn.cursor()
        try:
            # 1. Delete Tickets first (Child records)
            cursor.execute("DELETE FROM tickets WHERE booking_id = %s", (booking_id,))
            
            # 2. Delete Booking (Parent record)
            cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
            
            conn.commit()
            success = True
        except Exception as e:
            print(f"Error deleting booking: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
    return success

# =====================================================
# AUTHENTICATION
# =====================================================

def check_admin_login(username, password):
    conn = create_connection()
    user = None
    if conn:
        cursor = conn.cursor(dictionary=True)
        # In a real app, use hashing (bcrypt) for passwords!
        query = "SELECT * FROM admins WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
    return user