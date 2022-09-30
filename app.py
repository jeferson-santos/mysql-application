from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = '35.198.55.42'
app.config['MYSQL_USER'] = 'netbr'
app.config['MYSQL_PASSWORD'] = 'netbr'
app.config['MYSQL_DB'] = 'RH'

mysql = MySQL(app)

@app.route('/')
def Index():
    error = None
    if request.method == 'POST':
        # Get users
        cur = mysql.connection.cursor()
        cur.execute("SELECT email, pass, profile FROM users")
        data = cur.fetchall()
        cur.close()
        
        # Users looping
        for user in data:
            email = user[0]
            password  = user[1]
            profile = user[2]
    
            # Verify email
            if request.form['email'] == email:
                print("Encontrou o email")

                # Verify password
                if request.form['password'] == password:
                    print("Senha está correta!")

                    # Verify profile ADMIN
                    if profile == 1:
                        return redirect(url_for('admin'))
        
                    return redirect(url_for('Index'))

        error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

@app.route('/admin')
def admin():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM users")
    data = cur.fetchall()
    cur.close()

    return render_template('admin.html', users=data )


@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Inserted Successfully")
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        profile = request.form['profile']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (firstname, lastname, phone, email, pass, profile) VALUES (%s, %s, %s, %s, %s, %s)", (firstname, lastname, phone, email, password, profile))
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    print(id_data)
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE email=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))



@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        email = request.form['id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phone = request.form['phone']
        password = request.form['password']
        profile =  request.form['profile']

        print("EMAILLLL")
        print(email)

        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE users
               SET firstname=%s, lastname=%s, email=%s, phone=%s, pass=%s, profile=%s
               WHERE email=%s
            """, (firstname, lastname, email, phone, password, profile, email))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('admin'))


# Route for handling the login page logic
@app.route('/home', methods=['GET', 'POST'])
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM users")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', users=data )


if __name__ == "__main__":
    app.run(debug=True)
