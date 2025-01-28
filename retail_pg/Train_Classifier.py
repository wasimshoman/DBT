#created: 2025 26 01

# cluster the starship models into 3 groups based on their attributes. 
# results are saved to anew table (starship_clusters)

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import psycopg2
from psycopg2 import sql
import numpy as np



# Configure database connection
conn_params = {
    'dbname': 'test_db',
    'user': 'admin',
    'password': 'admin',
    'host': 'localhost',
    'port': 5432
}

try:
    # Connect to the database
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()

    # Load valid data from the OBT_starships table
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

    # Get relevant features
    features = ['cost_in_credits', 'crew', 'passengers', 'max_atmosphering_speed', 'length']
    X = df[features].fillna(0)

    # Create and train model
    scaler = StandardScaler()
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['cluster'] = kmeans.fit_predict(scaler.fit_transform(X))

    
    # save results to database
    
    # Drop if it exists and create a new table
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
    print(f"Success! Saved {len(df)} clusters to database")

except Exception as e:
    print(f"Error: {e}")
    if 'conn' in locals():
        conn.rollback()  
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()



