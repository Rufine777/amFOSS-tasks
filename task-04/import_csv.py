import csv
from connector import MySQLConnector

def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            series_title VARCHAR(255),
            released_year INT,
            genre VARCHAR(255),
            imdb_rating FLOAT,
            director VARCHAR(255),
            star1 VARCHAR(255),
            star2 VARCHAR(255),
            star3 VARCHAR(255)
        )
    """)

def import_csv_to_mysql(csv_file):
    db = MySQLConnector()
    if not db.connect():
        print("Failed to connect to database.")
        return

    cursor = db.connection.cursor()
    create_table(cursor)

    batch_data = []

    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            batch_data.append((
                row.get("Series_Title"),
                int(row.get("Released_Year")) if row.get("Released_Year") and row.get("Released_Year").isdigit() else None,
                row.get("Genre"),
                float(row.get("IMDB_Rating")) if row.get("IMDB_Rating") else None,
                row.get("Director"),
                row.get("Star1"),
                row.get("Star2"),
                row.get("Star3")
            ))

    insert_sql = """
        INSERT INTO movies (series_title, released_year, genre, imdb_rating, director, star1, star2, star3)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    db.batch_insert(insert_sql, batch_data)

    cursor.close()
    db.disconnect()

    print(f"Imported {len(batch_data)} rows from {csv_file} into the database successfully!")

if __name__ == "__main__":
    import_csv_to_mysql("movies.csv")

