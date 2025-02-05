# Created: 2025-01-26

# cluster the starship models into 3 groups based on their attributes. 
# results are saved to anew table (starship_clusters)

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import psycopg2
from psycopg2 import sql, extras
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
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cursor:
            # Load data and calculate each class averages because it has many ships
            query = """
                SELECT
                    starship_class,  -- Group by starship class
                    AVG(cost_in_credits) AS avg_cost_in_credits,
                    AVG(crew) AS avg_crew,
                    AVG(passengers) AS avg_passengers,
                    AVG(max_atmosphering_speed) AS avg_max_atmosphering_speed,
                    AVG(length) AS avg_length
                FROM
                    public."OBT_starships"
                WHERE cost_in_credits <> 0
                GROUP BY starship_class
            """
            df = pd.read_sql(query, conn)

            # Features for clustering
            features = ['avg_cost_in_credits', 'avg_crew', 'avg_passengers', 'avg_max_atmosphering_speed', 'avg_length']
            X = df[features].fillna(0)  # Handle missing values (if any after averaging)

            # Create and train KMeans model
            scaler = StandardScaler()
            kmeans = KMeans(n_clusters=3, random_state=42)
            df['cluster'] = kmeans.fit_predict(scaler.fit_transform(X))

            # Save results to the database (using bulk insert)
            create_table_query = """
                DROP TABLE IF EXISTS starship_clusters;
                CREATE TABLE starship_clusters (
                    starship_class VARCHAR(255) PRIMARY KEY,  -- Use starship_class as primary key
                    cluster INT
                );
            """
            cursor.execute(create_table_query)

            insert_query = sql.SQL("""
                INSERT INTO starship_clusters (starship_class, cluster)
                VALUES %s
                ON CONFLICT (starship_class) DO UPDATE SET cluster = EXCLUDED.cluster;
            """)

            values_to_insert = list(df[['starship_class', 'cluster']].itertuples(index=False, name=None))
            extras.execute_values(cursor, insert_query.as_string(conn), values_to_insert)


            conn.commit()
            logging.info(f"Success! Saved {len(df)} starship class clusters to database")

except Exception as e:
    logging.error(f"Error: {e}")
    if 'conn' in locals():
        conn.rollback()
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()