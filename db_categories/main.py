import json
import csv
import os
import mysql.connector
from datetime import datetime
import argparse

from mysql.connector import connect

#Arugument parser
parser = argparse.ArgumentParser(description = 'Read argument from command line')
parser.add_argument('-username', type = str, required = True, help = 'your username')
parser.add_argument('-password', type = str, required = True, help = 'your password')
parser.add_argument('-database', type = str, required = True, help = 'your database')
parser.add_argument('-action', type = str, required = True, help = 'your action')
args = parser.parse_args()

#Connect to MySql
mydb = mysql.connector.connect(
    host="localhost",
    user=args.username,
    password=args.password,
    database=args.database
)

#Perform action given by user
def perform_action(action):
    match action:
        case 'create':
            create_table()
        case 'delete':
            delete()
        case 'drop':
            drop()
        case 'select':
            select()

#CREATE TABLE
def create_table():
    cursor = mydb.cursor()
    cursor.execute("""
        CREATE TABLE categories(
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(255),
            parent_id INT NOT NULL,
            created_by INT,
            updated_by INT,
            created_at DATETIME,
            updated_at DATETIME,
            status ENUM('pending', 'active', 'inactive') DEFAULT 'pending'
        )
    """)
    mydb.commit()
    print('Created Table successfully')

#DELETE TABLE DATA
def delete():
    cursor = mydb.cursor()
    cursor.execute('TRUNCATE TABLE categories')
    mydb.commit()
    print('Table data deleted successfully')

#DROP TABLE
def drop():
    cursor = mydb.cursor()
    cursor.execute('DROP TABLE categories')
    mydb.commit()
    print('Table data dropped successfully')

#SELECT
def select():
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM categories')
    result = cursor.fetchall()
    for rows in result:
        print(rows)

#Insert data
def insert_data(file_data):
    cursor = mydb.cursor()
    for rows in file_data:
        name = rows['name']
        description = rows['description']
        current_time = datetime.now()

        cursor.execute(
            """INSERT INTO categories(name, description, parent_id, created_by, updated_by, created_at, updated_at, status)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""", (name, description, 0, 0, 0, current_time, current_time, 'active')
        )
        mydb.commit()
    print('Data inserted successfully')



#Identify file type
def file_type(directory_path, files):
    for file_name in files:
        extension = file_name.split('.')[-1]
        full_path = os.path.join(directory_path, file_name) # Path of file

        match extension:
            case 'json':
                file_data = read_file_json(full_path)
                insert_data(file_data)
            case 'csv':
                file_data = read_file_csv(full_path)
                insert_data(file_data)
            case _:
                pass


# Read json file
def read_file_json(file_name):
    with open(file_name, 'r') as file:
        document_name = json.load(file)
        return document_name

# Read csv file
def read_file_csv(file_name):
    with open(file_name, mode='r') as file:
        return list(csv.DictReader(file))

#Main
def main():
    action = args.action
    perform_action(action)

    if args.action == 'create':
        directory_path = '/Users/ayushsamor/workspace/python-programs/booksy/db_categories'
        files = os.listdir(directory_path)
        file_type(directory_path, files)

if __name__ == '__main__':
    main()
