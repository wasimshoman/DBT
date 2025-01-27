# cluster the starship models into 3 groups based on their attributes. 
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine

# Configure database connection
engine = create_engine('postgresql://admin:admin@localhost:5432/test_db')

try:
    # Load data from the ml_preprocessing table
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM public.ml_preprocessing", conn)

    # Get relevant features
    features = ['cost_in_credits', 'crew', 'passengers', 'max_atmosphering_speed', 'length']
    X = df[features].fillna(0)

    # Create and train model
    scaler = StandardScaler()
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['cluster'] = kmeans.fit_predict(scaler.fit_transform(X))

    # Save results to database
    df[['starship_id', 'cluster']].to_sql(
        name='starship_clusters',
        con=engine,
        if_exists='replace',  # Overwrite existing table
        index=False
    )
    print(f"Success! Saved {len(df)} clusters to database")

    # Show quick summary
    '''
    print("\nCluster distribution:")
    print(df['cluster'].value_counts())
    '''

except Exception as e:
    print(f"Error: {e}")