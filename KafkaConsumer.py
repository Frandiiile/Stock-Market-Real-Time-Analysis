from kafka import KafkaConsumer
from time import sleep
from json import loads
from google.cloud import bigquery
import ast

from google.oauth2 import service_account

# Create BigQuery credentials object
credentials = service_account.Credentials.from_service_account_file('SWARET.json')

# Construct a BigQuery client object.
bq_client = bigquery.Client(credentials=credentials)

# Specify BigQuery table to stream to
table_id = 'stock-market-realtime-analysis.HadikDataset.hadakTableau'

# Create a Kafka consumer
c = KafkaConsumer('Stock_Topic', bootstrap_servers='localhost:9092')

def main():
    try:
        for msg in c:
            data = msg.value.decode('utf-8')
            res = ast.literal_eval(data)  # Convert string response to dictionary
            print(res)

            # Stream data into the BigQuery table
            rows_to_insert = [res]
            errors = bq_client.insert_rows_json(table_id, rows_to_insert)  # Make API request

            if errors == []:
                print("New rows added.")
            else:
                print("Encountered errors while inserting rows: {}".format(errors))
    finally:
        c.close()  # Close the Kafka consumer

if __name__ == "__main__":
    main()
