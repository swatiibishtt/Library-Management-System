import mysql.connector

def connect_database():
    connection = mysql.connector.connect(
        host="127.0.0.1",                  
        user="root",
        password="swatidatabase",    
        database="library_db",
        use_pure=True,                     
        connection_timeout=3              
    )
    return connection