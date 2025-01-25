# 20250124
#call API download data, create a database if not excist, load data into database
# we download data about starships
# the fields include
# Name: Name of the starship.
# Model: The specific model of the starship.
# Manufacturer: Who built it.
# Crew: Number of crew members needed.
# Passengers: Passenger capacity.
# Cargo Capacity: The amount of cargo it can carry.
# Cost in Credits: Cost of the starship.
# all columns 
# ['name', 'model', 'manufacturer', 'cost_in_credits', 'length', 
# 'max_atmosphering_speed', 'crew', 'passengers', 'cargo_capacity', 'consumables', 
# 'hyperdrive_rating', 'MGLT', 'starship_class', 'pilots', 'films', 'created', 'edited', 'url']

import requests
import psycopg2

# Database connection parameters
DB_HOST = "localhost"
DB_NAME = "test_db"
DB_USER = "admin"
DB_PASS = "admin"

# Function to fetch starship data from the API
def fetch_starship_data():
    url = "https://swapi.dev/api/starships/"
    starships = []
    while url:
        response = requests.get(url)
        data = response.json()
        starships.extend(data['results'])
        url = data['next']
    return starships

##### formating text
def to_sentence_case(text):
    return text.capitalize() if text else None

def to_title_case(text):
    return text.title() if text else None


# Function to process starship data, convert text data to rgith format
def process_starship_data(starships):
    processed_starships = []
    for ship in starships:
        processed_starships.append((
            to_title_case(ship.get('name')),  # Capitalize each word
            ship.get('model').lower() if ship.get('model') else None,  # Lowercase
            to_sentence_case(ship.get('manufacturer')),  # Sentence case
            int(ship['cost_in_credits']) if ship['cost_in_credits'] and ship['cost_in_credits'].isdigit() else None,
            float(ship['length'].replace(',', '')) if ship['length'] and ship['length'].replace(',', '').isdigit() else None,
            int(ship['max_atmosphering_speed']) if ship['max_atmosphering_speed'] and ship['max_atmosphering_speed'].isdigit() else None,
            int(ship['crew']) if ship['crew'] and ship['crew'].isdigit() else None,
            int(ship['passengers']) if ship['passengers'] and ship['passengers'].isdigit() else None,
            int(ship['cargo_capacity']) if ship['cargo_capacity'] and ship['cargo_capacity'].isdigit() else None,
            ship.get('consumables').lower() if ship.get('consumables') else None,  # Lowercase
            float(ship['hyperdrive_rating']) if ship.get('hyperdrive_rating') and ship['hyperdrive_rating'].replace('.', '', 1).isdigit() else None,
            int(ship['MGLT']) if ship.get('MGLT') and ship['MGLT'].isdigit() else None,
            to_title_case(ship.get('starship_class')) if ship.get('starship_class') else None,  # Capitalize each word
            ','.join(ship['pilots']).lower() if ship.get('pilots') else None,  # Lowercase
            ','.join(ship['films']).lower() if ship.get('films') else None,  # Lowercase
            ship.get('created'),
            ship.get('edited'),
            ship.get('url')
    )) 
    return processed_starships

# Function to save starship data to the PostgreSQL database 2 dimennnsion tables and 1 fact
def save_starship_data_to_db(starships):
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = connection.cursor()

    # Drop and recreate dimension and fact tables
    cursor.execute("""
    DROP TABLE IF EXISTS fact_starships CASCADE;
    DROP TABLE IF EXISTS dim_starships CASCADE;
    DROP TABLE IF EXISTS dim_manufacturers CASCADE;

    CREATE TABLE dim_manufacturers (
        id SERIAL PRIMARY KEY,
        manufacturer VARCHAR(255) UNIQUE
    );

    CREATE TABLE dim_starships (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        model VARCHAR(255),
        starship_class VARCHAR(255),
        manufacturer_id INT REFERENCES dim_manufacturers(id)
    );

    CREATE TABLE fact_starships (
        id INT PRIMARY KEY REFERENCES dim_starships(id),
        cost_in_credits BIGINT,
        length FLOAT,
        max_atmosphering_speed INT,
        crew INT,
        passengers INT,
        cargo_capacity BIGINT,
        hyperdrive_rating FLOAT,
        MGLT INT
    );
    """)

    # Insert data into dimension and fact tables
    manufacturer_cache = {}
    for ship in starships:
        # Insert into dim_manufacturers if not already inserted
        manufacturer = ship[2]
        if manufacturer not in manufacturer_cache:
            cursor.execute("""
            INSERT INTO dim_manufacturers (manufacturer)
            VALUES (%s) RETURNING id;
            """, (manufacturer,))
            manufacturer_id = cursor.fetchone()[0]
            manufacturer_cache[manufacturer] = manufacturer_id
        else:
            manufacturer_id = manufacturer_cache[manufacturer]

        # Insert into dim_starships
        cursor.execute("""
        INSERT INTO dim_starships (
            name, model, starship_class, manufacturer_id
        ) VALUES (%s, %s, %s, %s) RETURNING id;
        """, (ship[0], ship[1], ship[12], manufacturer_id))
        starship_id = cursor.fetchone()[0]

        # Insert into fact_starships
        cursor.execute("""
        INSERT INTO fact_starships (
            id, cost_in_credits, length, max_atmosphering_speed, crew, passengers, 
            cargo_capacity, hyperdrive_rating, MGLT
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            starship_id, ship[3], ship[4], ship[5], ship[6], ship[7],
            ship[8], ship[10], ship[11]
        ))

    connection.commit()
    cursor.close()
    connection.close()


# Main execution
if __name__ == "__main__":
    try:
        starships = fetch_starship_data()
        processed_starships = process_starship_data(starships)
        save_starship_data_to_db(processed_starships)
        print("Starship data successfully saved to the database.")
    except Exception as e:
        print(f"An error occurred: {e}")
