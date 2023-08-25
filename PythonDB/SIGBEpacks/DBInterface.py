import psycopg2
#inserare in baza de date

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
