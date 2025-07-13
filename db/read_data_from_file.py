import json
import csv
import mysql.connector
from datetime import datetime
import argparse
import os

#Argument parser
parser = argparse.ArgumentParser(description="Example program to read command line args")
parser.add_argument("-username", type=str, help="Your name")
parser.add_argument("-password", type=str, help="Your password")
parser.add_argument("-database", type=str, help="data")
args = parser.parse_args()  # read argument

# connect to MySql
mydb = mysql.connector.connect(
    host="localhost",
    user=args.username,
    password=args.password,
    database=args.database
)


# create table in MySql
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

#Insert data into MySql
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

#Read json file
def read_file_json(file_name):
    with open(file_name, 'r') as file:
        document_name = json.load(file)
        return document_name

#Read csv file
def read_file_csv(file_name):
    with open(file_name, mode='r') as file:
        return list(csv.DictReader(file))

#Identify file type
def file_type(directory_path, files):
    for file_name in files:
        extension = file_name.split(".")[-1]
        full_path = os.path.join(directory_path, file_name)  #Path of file

        match extension:
            case 'json':
                file_data = read_file_json(full_path)
                insert_data(file_data)
            case 'csv':
                file_data = read_file_csv(full_path)
                insert_data(file_data)
            case _:
                print(f"Unknown file extension: {extension}")


#Main code
def main():
    directory_path = '/Users/ayushsamor/workspace/python-programs/booksy/db'
    files = os.listdir(directory_path)
    create_table()
    file_type(directory_path, files)

if __name__ == '__main__':
    main()