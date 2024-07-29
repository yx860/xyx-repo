from elasticsearch import Elasticsearch, helpers
import pandas as pd
import os

def main():
    # Path to CSV file
    csv_file_path = os.path.join(os.path.dirname(__file__), "cv-valid-dev-test.csv")
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)
    
    df = df.where(pd.notnull(df), None)
    print(df)
    # Convert DataFrame to a list of dictionaries
    records = df.to_dict('records')
    
    # Connect to the Elasticsearch cluster
    es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme' : "http"}])
    
    # Define the index name
    index_name = 'cv-transcriptions'
    
    # Check if the index exists and delete if it does
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    
    # Define the index mapping
    mapping = {
        "mappings": {
            "properties": {
                "generated_text": {"type": "float"},
                "duration": {"type": "float"},
                "age": {"type": "keyword"},
                "gender": {"type": "keyword"},
                "accent": {"type": "keyword"}
            }
        }
    }
    
    # Create the index with the mapping
    es.indices.create(index=index_name, body=mapping)
    
    # # Prepare the records for bulk indexing
    actions = [
        {
            "_index": index_name,
            "_source": record
        }
        for record in records
    ]
    
    # Bulk index the data
    helpers.bulk(es, actions)
    
    print(f"Indexed {len(records)} records into the '{index_name}' index.")

if __name__ == "__main__":
    main()

