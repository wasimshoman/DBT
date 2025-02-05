# 20250124
# call API download data, create a database if not excist, load data into database
# we download data about starships
# All columns 
# ['name', 'model', 'manufacturer', 'cost_in_credits', 'length', 
# 'max_atmosphering_speed', 'crew', 'passengers', 'cargo_capacity', 'consumables', 
# 'hyperdrive_rating', 'MGLT', 'starship_class', 'pilots', 'films', 
# 'created', 'edited', 'url']
# metadata for the columns https://swapi.dev/documentation#starships


import requests
import psycopg2
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# postgres database connection parameters
conn_params = {
    'dbname': 'test_db',
    'user': 'admin',
    'password': 'admin',
    'host': 'localhost',
    'port': 5432
}
# fetch starship data from the API
def fetch_starship_data():
    url = "https://swapi.dev/api/starships/"
    starships = []
    while url:
        response = requests.get(url)
        data = response.json()
        starships.extend(data['results'])
        url = data['next']
    return starships

# formatting texts
def to_sentence_case(text):
    return text.capitalize() if text else None

def to_title_case(text):
    return text.title() if text else None

def to_int(value):
    if not value:
        return None
    try:
        return int(value.replace(',', '').replace(' ', ''))  # remove commas and spaces
    except ValueError:
        return None  

def to_float(value):
    if not value:
        return None
    try:
        return float(value.replace(',', '').replace(' ', '')) # remove commas and spaces
    except ValueError:
        return None
    

# data cleaning and structuring
# split manufacturer into two columns if multiple manufacturers exist
# search for company suffex and add it to the first name
def split_manufacturers(manufacturer):
    if not manufacturer:
        return None, None
    split_pattern = r",(?=\s(?!Inc(?:\.)?))"
    manufacturers = [m.strip() for m in re.split(split_pattern, manufacturer)]
    return manufacturers[0], manufacturers[1] if len(manufacturers) > 1 else None

# process starship data
# format data to the right structure
def process_starship_data(starships):
    processed_starships = []
    for ship in starships:
        manufacturer1, manufacturer2 = split_manufacturers(ship.get('manufacturer'))
        processed_starships.append({
            "name": to_title_case(ship.get('name')),  # capitalize each word
            "model": ship.get('model').lower() if ship.get('model') else None,
            "manufacturer1": to_sentence_case(manufacturer1),
            "manufacturer2": to_sentence_case(manufacturer2),
            "cost_in_credits": to_int(ship.get('cost_in_credits')),
            "length": to_float(ship.get('length')),
            "max_atmosphering_speed": to_int(ship.get('max_atmosphering_speed')),
            "crew": to_int(ship.get('crew')),
            "passengers": to_int(ship.get('passengers')),
            "cargo_capacity": to_int(ship.get('cargo_capacity')),
            "consumables": ship.get('consumables').lower() if ship.get('consumables') else None,
            "hyperdrive_rating": to_float(ship.get('hyperdrive_rating')),
            "MGLT": to_int(ship.get('MGLT')),
            "starship_class": to_title_case(ship.get('starship_class')) if ship.get('starship_class') else None, # capitalize each word
        })
    return processed_starships

# save data to the database
def save_starship_data_to_db(starships):
    try:
        with psycopg2.connect(**conn_params) as connection:
            with connection.cursor() as cursor:
                # drop and recreate dimension and fact tables + metadata table
                # 2 dimenstion tables (manufacturer and starship) 1 fact table, 1 metadata
                cursor.execute("""
                DROP TABLE IF EXISTS fact_starships CASCADE;
                DROP TABLE IF EXISTS dim_starships CASCADE;
                DROP TABLE IF EXISTS dim_manufacturers CASCADE;
                DROP TABLE IF EXISTS metadata CASCADE;

                CREATE TABLE dim_manufacturers (
                    id SERIAL PRIMARY KEY,
                    manufacturer1 VARCHAR(255),
                    manufacturer2 VARCHAR(255)
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
                CREATE TABLE metadata (
                    column_name VARCHAR(255) PRIMARY KEY,
                    data_type VARCHAR(255),
                    description TEXT,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP

                );
            """)

                 # insert data into dimension and fact tables + metadata
                manufacturer_cache = {} # to avoid repeating manufacturarers 
                for ship in starships:
                    # insert into dim_manufacturers if not already inserted
                    manufacturer_key = (ship["manufacturer1"], ship["manufacturer2"])
                    if manufacturer_key not in manufacturer_cache:
                        cursor.execute("""
                            INSERT INTO dim_manufacturers (manufacturer1, manufacturer2)
                            VALUES (%s, %s) RETURNING id;
                        """, manufacturer_key)
                        manufacturer_id = cursor.fetchone()[0] # get the id of the newly inserted manufacturer
                        manufacturer_cache[manufacturer_key] = manufacturer_id # create a copy of that manu. in the cache 
                    else:
                        manufacturer_id = manufacturer_cache[manufacturer_key]

                    # insert into dim_starships
                    cursor.execute("""
                        INSERT INTO dim_starships (
                            name, model, starship_class, manufacturer_id
                        ) VALUES (%s, %s, %s, %s) RETURNING id;
                    """, (ship["name"], ship["model"], ship["starship_class"], manufacturer_id)) 
                    starship_id = cursor.fetchone()[0] # get the id of the newly inserted starship

                    # insert into fact_starships
                    cursor.execute("""
                    INSERT INTO fact_starships (
                        id, cost_in_credits, length, max_atmosphering_speed, crew, passengers, 
                        cargo_capacity, hyperdrive_rating, MGLT
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                    """, (
                        starship_id, ship["cost_in_credits"], ship["length"], ship["max_atmosphering_speed"], 
                        ship["crew"], ship["passengers"], ship["cargo_capacity"], 
                        ship["hyperdrive_rating"], ship["MGLT"]
                    ))

                # insert metadata into the table
                # data copied from the website
                metadata = [
                    ("name", "string", "The name of this starship. The common name, such as 'Death Star'."),
                    ("model", "string", "The model or official name of this starship. Such as 'T-65 X-wing' or 'DS-1 Orbital Battle Station'."),
                    ("starship_class", "string", "The class of this starship, such as 'Starfighter' or 'Deep Space Mobile Battlestation'."),
                    ("manufacturer", "string", "The manufacturer of this starship. Comma separated if more than one."),
                    ("cost_in_credits", "string", "The cost of this starship new, in galactic credits."),
                    ("length", "string", "The length of this starship in meters."),
                    ("crew", "string", "The number of personnel needed to run or pilot this starship."),
                    ("passengers", "string", "The number of non-essential people this starship can transport."),
                    ("max_atmosphering_speed", "string", "The maximum speed of this starship in the atmosphere. 'N/A' if this starship is incapable of atmospheric flight."),
                    ("hyperdrive_rating", "string", "The class of this starship's hyperdrive."),
                    ("MGLT", "string", "The Maximum number of Megalights this starship can travel in a standard hour. A 'Megalight' is a standard unit of distance and has never been defined before within the Star Wars universe. This figure is only really useful for measuring the difference in speed of starships. We can assume it is similar to AU, the distance between our Sun (Sol) and Earth."),
                    ("cargo_capacity", "string", "The maximum number of kilograms that this starship can transport.")
                ]

                cursor.executemany("""
                INSERT INTO metadata (column_name, data_type, description)
                VALUES (%s, %s, %s);
                """, metadata)

                connection.commit()
                logging.info("Starship data successfully saved to the database.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Main execution
if __name__ == "__main__":
    try:
        starships = fetch_starship_data()
        processed_starships = process_starship_data(starships)
        save_starship_data_to_db(processed_starships)
    except Exception as e:
        logging.error(f"An error occurred: {e}")