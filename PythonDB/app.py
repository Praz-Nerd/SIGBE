from flask import Flask, render_template, request, redirect, url_for
from SIGBEpacks import DBInterface as DB
import os
from psycopg2 import Binary

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'PythonDB/static/uploads'

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
    # Retrieve user from database
    validation = DB.login_validation(username, password)
    if validation[0] == False:
        return render_template('index.html', error_message=validation[1])
    else:
        return redirect(url_for('dashboard', pk = validation[2][0]))

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
        photo = request.files['file']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
        photo.save(filepath)

        validation = DB.register_validation(username, password, nume, prenume, data_nasterii, cnp, photo.filename)
        
        if validation[0] == False:
            return render_template('register.html', error_message=validation[1])
        else:
            validation = DB.create_user(username, password, email, 
                                            nume, prenume, data_nasterii, cnp, filepath)
            if validation[0] == True:
                return render_template('index.html', success_message=validation[1])
            else:
                err = validation[1]+validation[2]
                return err
    return render_template('register.html')
    
@app.route('/dashboard/<int:pk>',methods=['GET','POST'])
def dashboard(pk):
    user = DB.return_user(pk)
    file_list = DB.check_files(pk)
    filename= os.path.basename(user[8])        
    return render_template('dashboard.html', filepath = url_for('static', filename='uploads/' + filename),
                               username = str(user[1]), nume = str(user[4]), prenume = str(user[5]), 
                               data_nasterii = str(user[6]), cnp = str(user[7]), pk=pk, file_list=file_list)

@app.route('/upload/<int:pk>', methods=['POST'])
def upload(pk):
    try:
        file = request.files['file']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        validation = DB.upload_file(file.filename, filepath, pk)

        if validation[0] == False:
            err = validation[1]+validation[2]
            return err
        else:
            print(validation[1])
            return redirect(url_for('dashboard', pk=pk))
    except:
       return "No file selected..."

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
