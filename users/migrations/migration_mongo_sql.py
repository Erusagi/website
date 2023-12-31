import pymongo
import psycopg2
import sys

def migrate_mongo_to_postgres(mongo_uri, mongo_db, postgres_uri):

    mongo_client = pymongo.MongoClient(mongo_uri)
    db = mongo_client[mongo_db]


    try:
        pg_conn = psycopg2.connect(postgres_uri)
        pg_cursor = pg_conn.cursor()
    except Exception as e:
        print(f"Не вдалося підключитися до PostgreSQL: {e}")
        sys.exit(1)


    try:

        authors = db.authors.find()
        quotes = db.quotes.find()


        for author in authors:
            pg_cursor.execute("INSERT INTO author (name, bio) VALUES (%s, %s) RETURNING id;",
                              (author['name'], author.get('bio', '')))
            author_id = pg_cursor.fetchone()[0]


            for quote in quotes:
                if quote['author_id'] == author['_id']:
                    pg_cursor.execute("INSERT INTO quote (text, author_id) VALUES (%s, %s);",
                                      (quote['text'], author_id))


        pg_conn.commit()
    except Exception as e:
        print(f"Помилка під час міграції: {e}")
        pg_conn.rollback()
        sys.exit(1)
    finally:

        pg_cursor.close()
        pg_conn.close()
        mongo_client.close()


mongo_uri = "mongodb://localhost:27017/"
mongo_db = "my_mongo_db"
postgres_uri = "postgresql://user:password@localhost:5432/my_postgres_db"

migrate_mongo_to_postgres(mongo_uri, mongo_db, postgres_uri)
