from flask import Flask, render_template, request, redirect, url_for
from SIGBEpacks import DBInterface as DB
import os
from psycopg2 import Binary


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])



@app.route("/")
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    connection = DB.connect_to()
    cursor = connection.cursor()

    # Retrieve user from database
    cursor.execute('SELECT * FROM elevi WHERE username = %s', (username,))
    user = cursor.fetchone()
    print(user)
    if user is None or str(user[2]) != password:
        error_message = "Incorrect username or password."
        return render_template('index.html', error_message=error_message)
    else:
         return redirect(url_for('dashboard', pk = user[0]))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process registration form data and insert into the database
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        nume = request.form.get('nume')
        prenume = request.form.get('prenume')
        data_nasterii = request.form.get('data_nasterii')
        cnp = request.form.get('cnp')

        connection = DB.connect_to()
        cursor = connection.cursor()

        # Check if username already exists in the database
        cursor.execute('SELECT * FROM elevi WHERE username = %s', (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            error_message = "Username already exists."
            return render_template('register.html', error_message=error_message)

        # Insert new user into the database
        cursor.execute('INSERT INTO elevi (username, password, email, nume, prenume, data_nasterii, cnp) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                       (username, password, email, nume, prenume, data_nasterii, cnp,))
        connection.commit()

        success_message = "Registration successful! You can now log in."
        return render_template('index.html', success_message=success_message)

    return render_template('register.html')

@app.route('/dashboard/<int:pk>',methods=['GET','POST'])
def dashboard(pk):
    user = DB.return_user(pk)
    return render_template('dashboard.html', 
                               username = str(user[1]), nume = str(user[4]), prenume = str(user[5]), data_nasterii = str(user[6]), cnp = str(user[7]), pk=pk)


@app.route('/upload/<int:pk>', methods=['POST'])
def upload(pk):
    print(pk)
    file = request.files['file']
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    connection = DB.connect_to()
    cursor = connection.cursor()
    cursor.execute('INSERT INTO fisiere (filename, elev_id, filepath) VALUES (%s, %s, %s)', 
                   (os.path.basename(filename), pk, filename))
    connection.commit()
    return redirect(url_for('dashboard', pk=pk))




@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
