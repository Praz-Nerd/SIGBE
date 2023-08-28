import psycopg2
from datetime import datetime
#functii diverse pentru interactiunea cu baza de date

def has_number(input_string):
    return any(char.isdigit() for char in input_string)

def has_special_char(input_string):
    return any(char in "!@#$%^&*()<>,./?;:" for char in input_string)

def connect_to():
    return psycopg2.connect(
        dbname = "SIGBE_DB",
        user = "postgres",
        password = "1234",
        host = "localhost",
        port = "5432"
    )

def login_validation(username, password):
    connection = connect_to()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM elevi WHERE username = %s AND password = %s', (username,password,))
    user = cursor.fetchone()
    print(user)
    cursor.close()
    connection.close()
    #list format: validation success, validation message, user
    if user is None:
        return [False, "Incorrect username or password", user]
    else:
        return [True, "Login successful", user]

def register_validation(username, password, nume, prenume, data_nasterii, cnp):
    connection = connect_to()
    cursor = connection.cursor()
    #username validation
    cursor.execute('SELECT * FROM elevi WHERE username = %s', (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        return [False, "Username already taken"]
    #password validation
    cursor.execute('SELECT * FROM elevi WHERE password = %s', (password,))
    existing_user = cursor.fetchone()
    if existing_user:
        return [False, "Password already used"]
    if len(password) < 8:
        return [False, "Password is too short"]
    #email validation is done in html
    #nume validation
    if has_number(nume) or has_special_char(nume):
        return [False, "Invalid nume"]
    if nume[0].isupper() == False:
        return [False, "Nume should start with an uppercase letter"]
    #prenume validation
    if has_number(prenume) or has_special_char(prenume):
        return [False, "Invalid prenume"]
    if nume[0].isupper() == False:
        return [False, "Prenume should start with an uppercase letter"]
    #data_nasterii validation
    if datetime.fromisoformat(data_nasterii).date() > datetime.today().date():
        return [False, "Invalid birth date"]
    #cnp validation
    if len(cnp) != 13:
        return [False, "Invalid CNP"]    
    cursor.close()
    connection.close()
    return [True, "User can be created"]
    
def create_user(username, password, email, nume, prenume, data_nasterii, cnp):
    try:
        connection = connect_to()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO elevi (username, password, email, nume, prenume, data_nasterii, cnp) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                       (username, password, email, nume, prenume, data_nasterii, cnp,))
        connection.commit()
        cursor.close()
        connection.close()
        return [True, "Registration successful! You can now log in."]
    except psycopg2.Error as e:
        return [False, "An error has occured", e]

def return_user(pk):
    connection = connect_to()
    cursor = connection.cursor()
    # Retrieve user from database
    cursor.execute('SELECT * FROM elevi WHERE id = %s', (pk,))
    user = cursor.fetchone()
    cursor.close()
    connection.close()
    return user

def upload_file(filename, filepath, pk):
    try:
        connection = connect_to()
        cursor = connection.cursor()
        cursor.execute('INSERT INTO fisiere (filename, elev_id, filepath) VALUES (%s, %s, %s)', 
                    (filename, pk, filepath,))
        connection.commit()
        cursor.close()
        connection.close()
        return [True, "File sucessfully saved in database"]
    except psycopg2.Error as e:
        return [False, "An error has occured", e]

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