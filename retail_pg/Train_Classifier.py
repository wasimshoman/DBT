# Created: 2025-01-26

# cluster the starship models into 3 groups based on their attributes. 
# results are saved to anew table (starship_clusters)

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import psycopg2
from psycopg2 import sql
import logging

# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# database connection
conn_params = {
    'dbname': 'test_db',
    'user': 'admin',
    'password': 'admin',
    'host': 'localhost',
    'port': 5432
}
try:
    # connect to the OBT_starships database
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cursor:
            # Load data from the table
            query = """
                SELECT
                    starship_id,
                    starship_name,
                    cost_in_credits,
                    crew,
                    passengers,
                    max_atmosphering_speed,
                    length,
                    starship_group as starship_group_manually
                FROM
                    public."OBT_starships"
                WHERE cost_in_credits <> 0
            """
            df = pd.read_sql(query, conn)

            # Get only relevant features
            features = ['cost_in_credits', 'crew', 'passengers', 'max_atmosphering_speed', 'length']
            X = df[features].fillna(0)  # important for the classifier to work; otherwise, it will throw an error

            # Create and train model
            scaler = StandardScaler()  # ensures all features are on a similar scale.
            kmeans = KMeans(n_clusters=3, random_state=42)  # models will be grouped into 3 clusters (0, 1, 2). 
            df['cluster'] = kmeans.fit_predict(scaler.fit_transform(X))

            # Save results to database
            # Drop the existing table if it exists
            # Create a new table
            create_table_query = """
            DROP TABLE IF EXISTS starship_clusters;
                CREATE TABLE starship_clusters (
                    starship_id INT PRIMARY KEY,
                    cluster INT
                );
            """
            cursor.execute(create_table_query)

            # Insert data into the new table
            insert_query = sql.SQL("""
                INSERT INTO starship_clusters (starship_id, cluster)
                VALUES (%s, %s);
            """)
            for _, row in df[['starship_id', 'cluster']].iterrows():
                starship_id = int(row['starship_id'])
                cluster = int(row['cluster'])
                cursor.execute(insert_query, (starship_id, cluster))

            conn.commit()
            logging.info(f"Success! Saved {len(df)} clusters to database")

except Exception as e:
    print(f"Error: {e}")
    if 'conn' in locals():
        conn.rollback()
finally:
    # Close the database connection
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
