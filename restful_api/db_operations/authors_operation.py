from restful_api.db.connect import DatabaseConnector
from datetime import datetime

class AuthorOperation(DatabaseConnector):

    def __init__(self, host, port, database, username, password):
        super().__init__(host, port, database, username, password)

    def read_authors(self):
        db_instance = self.connect()
        cursor = db_instance.cursor(dictionary=True)
        cursor.execute('SELECT * FROM authors')
        authors = cursor.fetchall()
        cursor.close()
        db_instance.close()
        return authors

    def insert_authors(self, name, description, email):
        db_instance = self.connect()
        cursor = db_instance.cursor()
        cursor.execute("""
                       INSERT INTO authors (name, description, email, created_by, updated_by, created_at, updated_at status)
                       VALUES (%s, %s, %s, %s, %s, %s)
                   """, (name, description, email, 0, 0, datetime.now(), datetime.now(), 'active'))
        db_instance.commit()
        author_id = cursor.lastrowid()
        cursor.close()
        db_instance.close()
        return author_id

    def update_authors(self, author_id, name, description, email):

        db_instance = self.connect()
        cursor = db_instance.cursor()
        cursor.execute("""
                      UPDATE authors
                      SET name=%s, description=%s, email=%s, updated_by=%s, updated_at=%s
                      WHERE id=%s
                  """,(name, description, email, 0, datetime.now(), author_id))
        db_instance.commit()
        cursor.close()
        db_instance.close()

    def delete_authors(self, author_id):
        db_instance = self.connect()
        cursor = db_instance.cursor()
        cursor.execute("DELETE FROM authors WHERE id = %s", (author_id,))
        db_instance.commit()
        cursor.close()
        db_instance.close()

