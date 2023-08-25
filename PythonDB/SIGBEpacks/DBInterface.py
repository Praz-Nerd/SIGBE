import psycopg2
#functii diverse pentru interactiunea cu baza de date

def connect_to():
    return psycopg2.connect(
        dbname = "SIGBE_DB",
        user = "postgres",
        password = "1234",
        host = "localhost",
        port = "5432"
    )
       
def return_user(pk):
    connection = connect_to()
    cursor = connection.cursor()
    # Retrieve user from database
    cursor.execute('SELECT * FROM elevi WHERE id = %s', (pk,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user

def check_files(pk):
    connection = connect_to()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM fisiere WHERE elev_id = %s', (pk,))
    file_list = cursor.fetchall()
    for file in file_list:
        print(file[3])
    cursor.close()
    connection.close()
    return file_list