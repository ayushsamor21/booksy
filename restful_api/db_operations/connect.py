import mysql.connector

class DatabaseConnector:
    def __init__(self, host, port, database, username, password):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password

    def connect(self):
        db_instance = mysql.connector.connect(
            host=self.host,
            port=self.port,
            database = self.database,
            user=self.username,
            password=self.password
        )
        return db_instance
