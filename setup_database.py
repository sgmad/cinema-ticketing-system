import requests
import mysql.connector
import os
import shutil
from datetime import datetime, timedelta

# ==========================================
# CONFIGURATION
# ==========================================
API_KEY = 'e8170a03e66e01642b20d0ad8a609adc'
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
DB_CONFIG = { 'host': 'localhost', 'database': 'cinema_db', 'user': 'root', 'password': '' }

def create_connection():
    return mysql.connector.connect(**DB_CONFIG)

def download_image(poster_path):
    if not poster_path: return "assets/sample_posters/default.png"
    filename = poster_path.lstrip('/')
    local_path = f"assets/sample_posters/{filename}"
    if not os.path.exists("assets/sample_posters"):
        os.makedirs("assets/sample_posters")
    
    if os.path.exists(local_path): return local_path
    try:
        response = requests.get(f"{IMAGE_BASE_URL}{poster_path}", stream=True)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            return local_path
    except: pass
    return "assets/sample_posters/default.png"

# ==========================================
# 1. CATALOG MANAGEMENT
# ==========================================
def update_movies():
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT title, id FROM movies")
    existing_map = {row[0]: row[1] for row in cursor.fetchall()}
    
    # We need exactly 22 movies: 2 Anchors + 20 for Rotation (5 batches of 4)
    TARGET_COUNT = 22
    print(f"Fetching Top {TARGET_COUNT} Movies from TMDB...")
    
    added_count = 0
    updated_count = 0
    
    # Track titles handled in this specific execution to handle API duplicates across pages
    processed_in_batch = set()

    def process_page(page_num):
        url = f"https://api.themoviedb.org/3/movie/now_playing?api_key={API_KEY}&language=en-US&page={page_num}"
        return requests.get(url).json().get('results', [])

    # Fetch 2 pages to ensure we hit our target
    results = process_page(1) + process_page(2)
    
    for item in results:
        # strict limit to prevent over-fetching
        if added_count + len(existing_map) >= TARGET_COUNT and item['title'] not in existing_map:
             if added_count >= TARGET_COUNT: break 

        title = item['title']
        
        # Prevent processing the same movie twice if it appears on multiple pages
        if title in processed_in_batch:
            continue
        processed_in_batch.add(title)

        overview = item['overview']
        poster_path = download_image(item['poster_path'])
        score = item.get('vote_average', 0)
        imdb_label = f"★ {score:.1f}/10"

        details_url = f"https://api.themoviedb.org/3/movie/{item['id']}?api_key={API_KEY}&append_to_response=release_dates,credits"
        details = requests.get(details_url).json()
        
        duration = details.get('runtime', 120) or 120
        tagline = details.get('tagline', '') 
        
        mpaa_rating = "NR"
        for release in details.get('release_dates', {}).get('results', []):
            if release['iso_3166_1'] == 'US':
                for r in release['release_dates']:
                    if r['certification']:
                        mpaa_rating = r['certification']
                        break
        
        director = "Unknown"
        for crew in details.get('credits', {}).get('crew', []):
            if crew['job'] == 'Director':
                director = crew['name']
                break
        
        cast_str = ", ".join([c['name'] for c in details.get('credits', {}).get('cast', [])[:3]])
        genre = details['genres'][0]['name'] if details.get('genres') else "General"
        review_content = f"\"{tagline}\"" if tagline else ""

        if title in existing_map:
            movie_id = existing_map[title]
            sql = """UPDATE movies SET 
                     genre=%s, duration_minutes=%s, rating=%s, description=%s, 
                     poster_path=%s, director=%s, cast=%s, review=%s, imdb_rating=%s 
                     WHERE id=%s"""
            val = (genre, duration, mpaa_rating, overview, poster_path, director, cast_str, review_content, imdb_label, movie_id)
            cursor.execute(sql, val)
            updated_count += 1
        else:
            sql = """INSERT INTO movies 
                     (title, genre, duration_minutes, rating, description, poster_path, director, cast, review, imdb_rating) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            val = (title, genre, duration, mpaa_rating, overview, poster_path, director, cast_str, review_content, imdb_label)
            cursor.execute(sql, val)
            added_count += 1
            print(f"   + Added: {title}")

    conn.commit()
    conn.close()
    print(f"Movies Synced. Added: {added_count}, Updated: {updated_count}")

# ==========================================
# 2. SCHEDULE GENERATION
# ==========================================
def extend_schedule():
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM movies")
    movie_ids = [r[0] for r in cursor.fetchall()]
    
    if len(movie_ids) < 22:
        print(f"Warning: Only found {len(movie_ids)} movies. Ideal is 22. Schedule might loop early.")

    cursor.execute("SELECT id, name FROM halls ORDER BY id ASC")
    all_halls = cursor.fetchall()
    if not all_halls:
        print("No halls found.")
        return

    print("Generating 14-Day Schedule...")
    
    cursor.execute("DELETE FROM showtimes WHERE start_time > NOW()")
    
    today = datetime.now().date()
    slots = ["12:00:00", "15:00:00", "18:00:00", "21:00:00"]
    
    total_slots_needed = len(all_halls) * len(slots)

    # 1. Anchors: The top 2 movies play EVERY day.
    anchors = movie_ids[:2]
    
    # 2. Rotation Pool: The next 20 movies.
    rotation_pool = movie_ids[2:22]
    # Safety: if we didn't fetch enough, just cycle what we have
    if not rotation_pool: rotation_pool = anchors 

    for i in range(14): 
        current_date = today + timedelta(days=i)
        
        # SLIDING WINDOW LOGIC
        # We rotate the batch every 3 days.
        # Days 0-2: Batch 0 | Days 3-5: Batch 1 ... Days 12-13: Batch 4
        batch_index = i // 3
        
        # Ensure we don't go out of bounds if the loop extends
        batch_index = batch_index % 5 
        
        start_idx = batch_index * 4
        
        # Grab the 4 unique movies for this 3-day block
        # Using modulo ensures safety if the pool is smaller than expected
        todays_rotation = []
        for k in range(4):
            movie = rotation_pool[(start_idx + k) % len(rotation_pool)]
            todays_rotation.append(movie)
            
        # DAILY MENU: 2 Anchors + 4 Unique Rotating Movies
        daily_menu = anchors + todays_rotation
        
        # CARD DEALER PATTERN
        # We deal these 6 movies into the available hall slots.
        # Anchors appear twice in the pattern to represent high demand.
        pattern = [
            daily_menu[0], daily_menu[0], # Anchor 1 (Heavy Rotation)
            daily_menu[1], daily_menu[1], # Anchor 2 (Heavy Rotation)
            daily_menu[2], # Batch Movie 1
            daily_menu[3], # Batch Movie 2
            daily_menu[4], # Batch Movie 3
            daily_menu[5]  # Batch Movie 4
        ]
        
        deck = []
        while len(deck) < total_slots_needed:
            deck.extend(pattern)
            
        deck = deck[:total_slots_needed]
        
        # Shift the deck daily to ensure variety in start times/halls
        shift_amount = i * 3
        deck = deck[shift_amount % len(deck):] + deck[:shift_amount % len(deck)]

        # Deal to halls
        card_index = 0
        
        for hall_id, hall_name in all_halls:
            name_upper = hall_name.upper()
            if "IMAX" in name_upper: price = 750.00   
            elif "VIP" in name_upper or "LUXE" in name_upper: price = 550.00 
            else: price = 350.00              

            for time_str in slots:
                if card_index < len(deck):
                    selected_movie_id = deck[card_index]
                    card_index += 1
                    
                    start_time = f"{current_date} {time_str}"
                    
                    sql = "INSERT INTO showtimes (movie_id, hall_id, start_time, price_standard) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (selected_movie_id, hall_id, start_time, price))

    conn.commit()
    conn.close()
    print("Schedule Generated.")

if __name__ == "__main__":
    update_movies()
    extend_schedule()