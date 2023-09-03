from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="userinfo"
)

mycursor = mydb.cursor()


# Function to get divisions from the database
def get_divisions():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM division")  # Corrected table name
    divisions = mycursor.fetchall()
    mycursor.close()
    return divisions

@app.route('/')
def index():
    divisions = get_divisions()
    return render_template('division.html', divisions=divisions)

@app.route('/add', methods=['POST'])
def add_division():
    division_name = request.form['division']
    mycursor = mydb.cursor()
    query = "INSERT INTO division (Division) VALUES (%s)"  # Corrected table name
    values = (division_name,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:division_id>', methods=['GET', 'POST'])
def edit_division(division_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM division WHERE id = %s"  # Corrected table name
        values = (division_id,)
        mycursor.execute(query, values)
        division = mycursor.fetchone()
        mycursor.close()
        return render_template('division_edit.html', division=division)  # Updated template name
    elif request.method == 'POST':
        new_name = request.form['new_name']
        new_name1=request.form['new_name1']
        mycursor = mydb.cursor()
        query = "UPDATE division SET Division = %s, id=%s WHERE id = %s"  # Corrected table name
        values = (new_name,new_name1, division_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('index'))

@app.route('/delete/<int:division_id>', methods=['POST'])
def delete_division(division_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM division WHERE id = %s"  # Corrected table name
    values = (division_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search_division():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM division WHERE Division LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    divisions = mycursor.fetchall()
    mycursor.close()
    return render_template('division.html', divisions=divisions)

@app.route('/clear')
def clear():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
