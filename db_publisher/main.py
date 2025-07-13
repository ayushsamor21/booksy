import csv
import mysql.connector
from datetime import datetime
import argparse

#Argument parse
parser = argparse.ArgumentParser(description="MySql connector to read csv file")
parser.add_argument("-username", type=str, required=True, help="Your MySql username")
parser.add_argument("-password", type=str, required=True, help="Your MySql password")
parser.add_argument("-database", type=str, required=True, help="Your MySql database")
args = parser.parse_args()

#connect to MySql
mydb = mysql.connector.connect(
    host = "localhost",
    user = args.username,
    password = args.password,
    database = args.database
)

#create table:publisher in MySql
def create_table():
    cursor = mydb.cursor()
    cursor.execute("""
        CREATE TABLE publishers(
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            address VARCHAR(255),
            description VARCHAR(255),
            created_by INT DEFAULT 0, 
            updated_by INT DEFAULT 0,
            created_at DATETIME,
            updated_at DATETIME,
            status ENUM('pending', 'active', 'inactive') DEFAULT 'pending'
        )"""
    )
    mydb.commit()
    print("The table created successfully")

#insert data in MySql
def insert_data(publishers):
    cursor = mydb.cursor()
    for row in publishers:
        name = row["name"]
        address = row["address"]
        description = row["description"]
        current_datetime = datetime.now()

        cursor.execute("""
                INSERT INTO publishers (name, address, description, created_by, updated_by, created_at, updated_at, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, address, description, 0, 0, current_datetime, current_datetime, 'active'))
    mydb.commit()

    print("Data inserted successfully.")

#read csv file
def read_file(file_name):
    with open(file_name, mode='r') as file:    #with open(file_name, mode='r', encoding='utf-8')
        return list(csv.DictReader(file))

#main function
def main():
    create_table()
    file_name = 'publisher_data.csv'
    publishers = read_file(file_name)
    insert_data(publishers)

if __name__ == '__main__':
    main()
