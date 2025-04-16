import json
import mysql.connector
import logging

# Logger configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Database connection function
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="knowledge_base"
        )
        logger.info("Connected to MySQL database successfully")
        return connection
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise

# Function to insert or update JSON data into MySQL
def insert_json_to_db(json_file_path):
    try:
        # Read the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        # Connect to the database
        conn = connect_to_db()
        cursor = conn.cursor()

        # Start a transaction
        cursor.execute("START TRANSACTION")

        # Process each record in the JSON array
        for record in data:
            # Check if the intent already exists
            cursor.execute("SELECT id FROM knowledge_base WHERE intent = %s", (record['intent'],))
            existing_record = cursor.fetchone()

            if existing_record:
                kb_id = existing_record[0]
                logger.debug(f"Intent '{record['intent']}' already exists with kb_id {kb_id}. Updating record.")

                # Update existing record in knowledge_base
                kb_query = """
                    UPDATE knowledge_base 
                    SET title = %s, category = %s, summary = %s, response_template = %s
                    WHERE intent = %s
                """
                kb_values = (
                    record['title'],
                    record['category'],
                    record['content']['summary'],
                    record['content']['response_template'],
                    record['intent']
                )
                cursor.execute(kb_query, kb_values)

                # Delete existing related data to avoid duplicates
                cursor.execute("DELETE FROM kb_keywords WHERE kb_id = %s", (kb_id,))
                cursor.execute("DELETE FROM kb_details WHERE kb_id = %s", (kb_id,))
                cursor.execute("DELETE FROM kb_metadata WHERE kb_id = %s", (kb_id,))
            else:
                # Insert new record into knowledge_base
                kb_query = """
                    INSERT INTO knowledge_base (title, intent, category, summary, response_template)
                    VALUES (%s, %s, %s, %s, %s)
                """
                kb_values = (
                    record['title'],
                    record['intent'],
                    record['category'],
                    record['content']['summary'],
                    record['content']['response_template']
                )
                cursor.execute(kb_query, kb_values)
                kb_id = cursor.lastrowid  # Get the new kb_id
                logger.debug(f"Inserted new record: {record['title']} with kb_id {kb_id}")

            # Insert keywords into kb_keywords
            for keyword in record['keywords']:
                keyword_query = """
                    INSERT INTO kb_keywords (kb_id, keyword)
                    VALUES (%s, %s)
                """
                cursor.execute(keyword_query, (kb_id, keyword))
            logger.debug(f"Inserted {len(record['keywords'])} keywords for kb_id {kb_id}")

            # Insert details into kb_details
            for step_order, instruction in enumerate(record['content']['details'], 1):
                detail_query = """
                    INSERT INTO kb_details (kb_id, step_order, instruction)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(detail_query, (kb_id, step_order, instruction))
            logger.debug(f"Inserted {len(record['content']['details'])} details for kb_id {kb_id}")

            # Insert metadata into kb_metadata
            for meta_key, meta_value in record['metadata'].items():
                metadata_query = """
                    INSERT INTO kb_metadata (kb_id, meta_key, meta_value)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(metadata_query, (kb_id, meta_key, meta_value))
            logger.debug(f"Inserted {len(record['metadata'])} metadata entries for kb_id {kb_id}")

        # Commit the transaction
        conn.commit()
        logger.info(f"Successfully processed {len(data)} records from JSON into MySQL")

    except Exception as e:
        logger.error(f"Error inserting JSON data: {str(e)}")
        conn.rollback()  # Roll back on error
        raise

    finally:
        cursor.close()
        conn.close()
        logger.info("Database connection closed")

# Example usage
if __name__ == "__main__":
    json_file_path = "kb_data.json"  # Replace with your JSON file path
    insert_json_to_db(json_file_path)