import json
import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
    host = "localhost",
    user = "*****",
    password = "*****",
    database="******"
)

def create_table():
    cursor = mydb.cursor()
    cursor.execute("""
        CREATE TABLE authors(
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            email VARCHAR(255) NOT NULL,
            created_by INT,
            updated_by INT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            status ENUM('pending', 'active', 'inactive') DEFAULT 'pending'
        )
    """)
    mydb.commit()
    print("successful executed")


def insert_data(authors):
    cursor = mydb.cursor()
    for row in authors:
        name = row["name"]
        description = row["description"]
        email = row["email"]
        current_datetime = datetime.now()

        cursor.execute("""
            INSERT INTO authors (name, description, email, created_by, updated_by, created_at, updated_at, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, description, email, 0, 0, current_datetime, current_datetime, 'active'))

    mydb.commit()
    print("Data inserted successfully.")


def read_file(file_name):
    with open(file_name, 'r') as file:
        authors = json.load(file)
        return authors

def main():
    create_table()
    file_name = '../db_authors_json/data.json'
    authors = read_file(file_name)
    insert_data(authors)


if __name__ == '__main__':
    main()