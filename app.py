from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import re
import tabula
import os
import csv
import pandas as pd
from pandas.errors import ParserError
from flask import send_file
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'Prakhar@123'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="userinfo"
)

mycursor = mydb.cursor()


@app.route('/')

@app.route('/login', methods=['GET', 'POST'])

def login():
    message = ''
    
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        
        mycursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email, password,))
        user = mycursor.fetchone()
        
        if user:
            session['loggedin'] = True
            session['userid'] = 7
            session['name'] = user[1]
            session['email'] = user[2]
            message = 'Logged in successfully!'
            return redirect(url_for('dashboarda'))
        else:
            mycursor.execute('SELECT * FROM userlogin WHERE email = %s AND password = %s', (email, password,))
            user = mycursor.fetchone()
            
            if user:
                session['loggedin'] = True
                session['userid'] = user[0]
                session['name'] = user[1]
                session['email'] = user[2]
                message = 'Logged in successfully!'
                return redirect(url_for('dashboard'))
            else:
                message = 'Please enter correct email/password!'
    
    return render_template('login.html', message=message)

@app.route('/logout')
# def logout():
#     return render_template('login.html')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/plantation')
def plantation():
    return render_template('plantation.html')


@app.route('/addplant')
def addplant():
    return render_template('addplant.html')

@app.route('/dashboarda')
def dashboarda():
    if 'name' in session and session['name'] == 'HQ user/ Admin':
        #Total form accepted
        mycursor.execute('SELECT COUNT(*) FROM user2')
        row_count = mycursor.fetchone()[0]

       
        #Form received from Users
        mycursor.execute('SELECT COUNT(*) FROM user1_form_details')
        form1_count = mycursor.fetchone()[0]

        mycursor.execute('SELECT COUNT(*) FROM user2_form_details')
        form2_count = mycursor.fetchone()[0]

        mycursor.execute('SELECT COUNT(*) FROM user3_form_details')
        form3_count = mycursor.fetchone()[0]

        mycursor.execute('SELECT COUNT(*) FROM user4_form_details')
        form4_count = mycursor.fetchone()[0]

        mycursor.execute('SELECT COUNT(*) FROM user5_form_details')
        form5_count = mycursor.fetchone()[0]

        mycursor.execute('SELECT COUNT(*) FROM user6_form_details')
        form6_count = mycursor.fetchone()[0]

        treceived_form=form1_count+form2_count+form3_count+form4_count+form5_count+form6_count

        #Unsubmitted form logic   
        mycursor.execute('SELECT COUNT(*) FROM user1_form')
        request1_count = mycursor.fetchone()[0]

        mycursor.execute('SELECT COUNT(*) FROM user2_form')
        request2_count = mycursor.fetchone()[0]

        mycursor.execute('SELECT COUNT(*) FROM user3_form')
        request3_count = mycursor.fetchone()[0]

        mycursor.execute('SELECT COUNT(*) FROM user4_form')
        request4_count = mycursor.fetchone()[0]

        mycursor.execute('SELECT COUNT(*) FROM user5_form')
        request5_count = mycursor.fetchone()[0]

        mycursor.execute('SELECT COUNT(*) FROM user6_form')
        request6_count = mycursor.fetchone()[0]

        tunsubmit_form=request1_count+request2_count+request3_count+request4_count+request5_count+request6_count

        #Form accepted from each user count
        mycursor.execute("SELECT COUNT(*) FROM user2 WHERE Division = 'Ambala'")
        form1_submit = mycursor.fetchone()[0]

        mycursor.execute("SELECT COUNT(*) FROM user2 WHERE Division = 'Faridabad'")
        form2_submit = mycursor.fetchone()[0]

        mycursor.execute("SELECT COUNT(*) FROM user2 WHERE Division = 'Gurugram'")
        form3_submit = mycursor.fetchone()[0]

        mycursor.execute("SELECT COUNT(*) FROM user2 WHERE Division = 'Hisar'")
        form4_submit = mycursor.fetchone()[0]

        mycursor.execute("SELECT COUNT(*) FROM user2 WHERE Division = 'Rohtak'")
        form5_submit = mycursor.fetchone()[0]

        mycursor.execute("SELECT COUNT(*) FROM user2 WHERE Division = 'Karnal'")
        form6_submit = mycursor.fetchone()[0]
        
       
    
        return render_template('dashboarda.html', row_count=row_count, 
                               form1_count=form1_count,form2_count=form2_count,form3_count=form3_count,form4_count=form4_count,
                               form5_count=form5_count,form6_count=form6_count,
                               request1_count=request1_count, request2_count=request2_count, request3_count=request3_count,
                                request4_count=request4_count, request5_count=request5_count, request6_count=request6_count,
                                treceived_form=treceived_form,tunsubmit_form=tunsubmit_form,form1_submit=form1_submit,
                                form2_submit=form2_submit,form3_submit=form3_submit,form4_submit=form4_submit,
                                form5_submit=form5_submit,form6_submit=form6_submit
                             )
    
@app.route('/dashboard')
def dashboard():
    if 'name' in session and session['name'] == 'HQ user/ Admin':
       return redirect(url_for('dashboarda'))
    
    elif 'name' in session and session['name'] == 'user1' :
        
        mycursor.execute("SELECT COUNT(*) FROM user2 WHERE Division = 'Ambala'")
        row_count = mycursor.fetchone()[0]
    
        
        mycursor.execute('SELECT COUNT(*) FROM user1_form_details')
        request_count = mycursor.fetchone()[0]

        mycursor.execute('SELECT COUNT(*) FROM user1_form')
        unsubmit_form=mycursor.fetchone()[0]
        
    
        return render_template('dashboard.html', row_count=row_count, request_count=request_count,
                               unsubmit_form=unsubmit_form
                               )
    
    elif 'name' in session and session['name'] == 'user2':
        mycursor.execute("SELECT COUNT(*) FROM user2 WHERE Division = 'Faridabad'")
        row_count = mycursor.fetchone()[0]
    
        
        mycursor.execute('SELECT COUNT(*) FROM user2_form_details')
        request_count = mycursor.fetchone()[0]

        mycursor.execute('SELECT COUNT(*) FROM user2_form')
        unsubmit_form=mycursor.fetchone()[0]
        
    
        return render_template('dashboard.html', row_count=row_count, request_count=request_count,
                               unsubmit_form=unsubmit_form
                               )
    
    elif 'name' in session and session['name'] == 'user3':
        mycursor.execute("SELECT COUNT(*) FROM user2 WHERE Division = 'Gurugram'")
        row_count = mycursor.fetchone()[0]
    
        
        mycursor.execute('SELECT COUNT(*) FROM user3_form_details')
        request_count = mycursor.fetchone()[0]

        mycursor.execute('SELECT COUNT(*) FROM user3_form')
        unsubmit_form=mycursor.fetchone()[0]
        
    
        return render_template('dashboard.html', row_count=row_count, request_count=request_count,
                               unsubmit_form=unsubmit_form
                               )

    
    elif 'name' in session and session['name'] == 'user4':
        mycursor.execute("SELECT COUNT(*) FROM user2 WHERE Division = 'Hisar'")
        row_count = mycursor.fetchone()[0]
    
        
        mycursor.execute('SELECT COUNT(*) FROM user4_form_details')
        request_count = mycursor.fetchone()[0]

        mycursor.execute('SELECT COUNT(*) FROM user4_form')
        unsubmit_form=mycursor.fetchone()[0]
        
    
        return render_template('dashboard.html', row_count=row_count, request_count=request_count,
                               unsubmit_form=unsubmit_form
                               )

    
    elif 'name' in session and session['name'] == 'user5':
        mycursor.execute("SELECT COUNT(*) FROM user2 WHERE Division = 'Rohtak'")
        row_count = mycursor.fetchone()[0]
    
        
        mycursor.execute('SELECT COUNT(*) FROM user5_form_details')
        request_count = mycursor.fetchone()[0]

        mycursor.execute('SELECT COUNT(*) FROM user5_form')
        unsubmit_form=mycursor.fetchone()[0]
        
    
        return render_template('dashboard.html', row_count=row_count, request_count=request_count,
                               unsubmit_form=unsubmit_form
                               )

    elif 'name' in session and session['name'] == 'user6':
        mycursor.execute("SELECT COUNT(*) FROM user2 WHERE Division = 'Karnal'")
        row_count = mycursor.fetchone()[0]
    
        
        mycursor.execute('SELECT COUNT(*) FROM user6_form_details')
        request_count = mycursor.fetchone()[0]

        mycursor.execute('SELECT COUNT(*) FROM user6_form')
        unsubmit_form=mycursor.fetchone()[0]
        
    
        return render_template('dashboard.html', row_count=row_count, request_count=request_count,
                               unsubmit_form=unsubmit_form
                               )


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        mycursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = mycursor.fetchone()
        if account:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not userName or not password or not email:
            message = 'Please fill out the form!'
        else:
            mycursor.execute('INSERT INTO userlogin (name, email, password) VALUES (%s, %s, %s)', (userName, email, password,))
            mydb.commit()
            message = 'You have successfully registered!'
    elif request.method == 'POST':
        message = 'Please fill out the form!'
    return render_template('register.html', message=message)

# @app.route("/plantation", methods=['POST'])
# def uploadFiles():
#     error_message=''
#     uploaded_file = request.files['file']
#     if uploaded_file.filename != '':
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
#         uploaded_file.save(file_path)
#         if file_path.endswith('.csv'):
#            error_message= parseCSV(file_path)
#         elif file_path.endswith('.pdf'):
#             csv_file_path = convertPDFtoCSV(file_path)
#             parseCSV(csv_file_path)
#             os.remove(csv_file_path)  # Remove the temporary CSV file

    
#     return redirect(url_for('alert', message=error_message))

# def convertPDFtoCSV(pdf_path):
#     csv_path = pdf_path.replace('.pdf', '.csv')
#     tabula.convert_into(pdf_path, csv_path, output_format="csv", pages='all')
#     return csv_path

# def parseCSV(csv_path):
#         mycursor.execute('SELECT COUNT(*) FROM user2')
#         row_count = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM save_details')
#         save_count = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user1_form_details')
#         form1_count = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user2_form_details')
#         form2_count = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user3_form_details')
#         form3_count = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user4_form_details')
#         form4_count = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user5_form_details')
#         form5_count = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user6_form_details')
#         form6_count = mycursor.fetchone()[0]

#         tform_count=row_count+form1_count+form2_count+form3_count+form4_count+form5_count+form6_count
            
#         mycursor.execute('SELECT COUNT(*) FROM user1_uploaded_details')
#         request1_count = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user2_uploaded_details')
#         request2_count = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user3_uploaded_details')
#         request3_count = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user4_uploaded_details')
#         request4_count = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user5_uploaded_details')
#         request5_count = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user6_uploaded_details')
#         request6_count = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user1_save_details')
#         save_details_row_count1 = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user2_save_details')
#         save_details_row_count2 = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user3_save_details')
#         save_details_row_count3 = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user4_save_details')
#         save_details_row_count4 = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user5_save_details')
#         save_details_row_count5 = mycursor.fetchone()[0]

#         mycursor.execute('SELECT COUNT(*) FROM user6_save_details')
#         save_details_row_count6 = mycursor.fetchone()[0]

#         tunsubmit_count1=save_details_row_count1+request1_count-form1_count
#         tunsubmit_count2=save_details_row_count2+request2_count-form2_count
#         tunsubmit_count3=save_details_row_count3+request3_count-form3_count
#         tunsubmit_count4=save_details_row_count4+request4_count-form4_count
#         tunsubmit_count5=save_details_row_count5+request5_count-form5_count
#         tunsubmit_count6=save_details_row_count6+request6_count-form6_count
#         col_names = ['id','Division', 'District', 'Range','Block','Beat','Village','Wing','LandCategory','Land','Scheme','PlantationMonth','Unit','Value','Spaceing','Sitename','KhasraNo','Latitude','Longitude','PlantCategory','Species','NoofPlant']
#         # csvData = pd.read_csv(csv_path, names=col_names, header=0,encoding='utf-8')
#          # Replace 'PlantationMonth' with the actual column name

#         # Define a custom date parsing function
        
        
#         df=pd.read_csv(csv_path,header=0, encoding='utf-8')
#         num_of_columns = df.shape[1]
#         if(num_of_columns<22):
#            error_message = "Please enter all coloumn. You have not filled " + str(22-num_of_columns) + " coloumns"
#            return error_message
#         elif(num_of_columns>22):
#            error_message = "Please remove extra coloumn. You have filled " + str(num_of_columns-22) + " extra coloumns"
#            return error_message
#         else:
#             try:
#                     csvData = pd.read_csv(csv_path, names=col_names, header=0, encoding='utf-8')
                    
#                     if len(csvData.columns) != len(col_names):
#                         error_message = "The number of columns in the CSV file "
#                         return error_message
                        
#                     else:
#                         if 'name' in session and session['name'] == 'HQ user/ Admin':
#                             for _, row in csvData.iterrows():
#                                 if all(row.values):
#                                     sql = "INSERT INTO user2 (id, Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
#                                     values = (row['id'], row['Division'], row['District'], row['Range'], row['Block'], row['Beat'], row['Village'], row['Wing'], row['LandCategory'], row['Land'], row['Scheme'], row['PlantationMonth'], row['Unit'], row['Value'], row['Spaceing'], row['Sitename'], row['KhasraNo'], row['Latitude'], row['Longitude'], row['PlantCategory'], row['Species'], row['NoofPlant'])
#                                     mycursor.execute(sql, values)
#                                     mydb.commit()
#                                     sql = "INSERT INTO misreport (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s,%s)"
#                                     values = (row['Division'], row['District'], row['Range'], row['Block'],row['Beat'],row['Village'],row['Wing'],row['LandCategory'],row['Land'],row['Scheme'],row['PlantationMonth'],row['Unit'], row['Value'],row['Spaceing'],row['Sitename'],row['KhasraNo'],row['Latitude'],row['Longitude'],row['PlantCategory'],row['Species'],row['NoofPlant'])
#                                     mycursor.execute(sql, values)
#                                     mydb.commit() 

                                   
#                                 else:
#                                     print("Please fill all details before inserting into the database.")


#                         elif 'name' in session and session['name'] == 'user1':
#                             if tunsubmit_count1==0:
#                                 error_message = "You have Submitted all Requested Form"
#                                 return error_message
#                             if request1_count==tunsubmit_count1:
#                                 error_message = "Please First Download Requested Form"
#                                 return error_message
#                             else:
#                                 for _, row in csvData.iterrows():
#                                     sql = "INSERT INTO user1_form_details (id,Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s,%s)"
#                                     values = (row['id'],row['Division'], row['District'], row['Range'], row['Block'],row['Beat'],row['Village'],row['Wing'],row['LandCategory'],row['Land'],row['Scheme'],row['PlantationMonth'],row['Unit'], row['Value'],row['Spaceing'],row['Sitename'],row['KhasraNo'],row['Latitude'],row['Longitude'],row['PlantCategory'],row['Species'],row['NoofPlant'])
#                                     mycursor.execute(sql, values)
#                                     mydb.commit()
#                                     sql = "INSERT INTO misreport (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s,%s)"
#                                     values = (row['Division'], row['District'], row['Range'], row['Block'],row['Beat'],row['Village'],row['Wing'],row['LandCategory'],row['Land'],row['Scheme'],row['PlantationMonth'],row['Unit'], row['Value'],row['Spaceing'],row['Sitename'],row['KhasraNo'],row['Latitude'],row['Longitude'],row['PlantCategory'],row['Species'],row['NoofPlant'])
#                                     mycursor.execute(sql, values)
#                                     mydb.commit()   
#                                     if request1_count>tunsubmit_count1:
#                                         delete_query = "DELETE FROM user1_uploaded_details ORDER BY id ASC LIMIT 1"
#                                         mycursor.execute(delete_query)
#                                         mydb.commit() 

#                         elif 'name' in session and session['name'] == 'user2':
#                             if tunsubmit_count2==0:
#                                 error_message = "You have Submitted all Requested Form"
#                                 return error_message
#                             elif request2_count==tunsubmit_count2:
#                                 error_message = "Please First Download Requested Form"
#                                 return error_message
#                             else:
#                                 for _, row in csvData.iterrows():
#                                     sql = "INSERT INTO user2_form_details (id,Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s,%s)"
#                                     values = (row['id'],row['Division'], row['District'], row['Range'], row['Block'],row['Beat'],row['Village'],row['Wing'],row['LandCategory'],row['Land'],row['Scheme'],row['PlantationMonth'],row['Unit'], row['Value'],row['Spaceing'],row['Sitename'],row['KhasraNo'],row['Latitude'],row['Longitude'],row['PlantCategory'],row['Species'],row['NoofPlant'])
#                                     mycursor.execute(sql, values)
#                                     mydb.commit()
#                                     sql = "INSERT INTO misreport (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s,%s)"
#                                     values = (row['Division'], row['District'], row['Range'], row['Block'],row['Beat'],row['Village'],row['Wing'],row['LandCategory'],row['Land'],row['Scheme'],row['PlantationMonth'],row['Unit'], row['Value'],row['Spaceing'],row['Sitename'],row['KhasraNo'],row['Latitude'],row['Longitude'],row['PlantCategory'],row['Species'],row['NoofPlant'])
#                                     mycursor.execute(sql, values)
#                                     mydb.commit()    
#                                     if request2_count>tunsubmit_count2:
#                                         delete_query = "DELETE FROM user2_uploaded_details ORDER BY id ASC LIMIT 1"
#                                         mycursor.execute(delete_query)
#                                         mydb.commit() 

#                         elif 'name' in session and session['name'] == 'user3':
#                             if tunsubmit_count3==0:
#                                 error_message = "You have Submitted all Requested Form"
#                                 return error_message
#                             elif request3_count==tunsubmit_count3:
#                                 error_message = "Please First Download Requested Form"
#                                 return error_message
#                             else:
#                                 for _, row in csvData.iterrows():
#                                     sql = "INSERT INTO user3_form_details (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s,%s)"
#                                     values = (row['id'],row['Division'], row['District'], row['Range'], row['Block'],row['Beat'],row['Village'],row['Wing'],row['LandCategory'],row['Land'],row['Scheme'],row['PlantationMonth'],row['Unit'], row['Value'],row['Spaceing'],row['Sitename'],row['KhasraNo'],row['Latitude'],row['Longitude'],row['PlantCategory'],row['Species'],row['NoofPlant'])
#                                     mycursor.execute(sql, values)
#                                     mydb.commit()
#                                     sql = "INSERT INTO misreport (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s,%s)"
#                                     values = (row['Division'], row['District'], row['Range'], row['Block'],row['Beat'],row['Village'],row['Wing'],row['LandCategory'],row['Land'],row['Scheme'],row['PlantationMonth'],row['Unit'], row['Value'],row['Spaceing'],row['Sitename'],row['KhasraNo'],row['Latitude'],row['Longitude'],row['PlantCategory'],row['Species'],row['NoofPlant'])
#                                     mycursor.execute(sql, values)
#                                     mydb.commit()    
#                                     if request3_count>tunsubmit_count3:
#                                         delete_query = "DELETE FROM user3_uploaded_details ORDER BY id ASC LIMIT 1"
#                                         mycursor.execute(delete_query)
#                                         mydb.commit()

#                         elif 'name' in session and session['name'] == 'user4':
#                             if tunsubmit_count4==0:
#                                 error_message = "You have Submitted all Requested Form"
#                                 return error_message
#                             elif request4_count==tunsubmit_count4:
#                                 error_message = "Please First Download Requested Form"
#                                 return error_message
#                             else:
#                                 for _, row in csvData.iterrows():
#                                     sql = "INSERT INTO user4_form_details (id,Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s,%s)"
#                                     values = (row['id'],row['Division'], row['District'], row['Range'], row['Block'],row['Beat'],row['Village'],row['Wing'],row['LandCategory'],row['Land'],row['Scheme'],row['PlantationMonth'],row['Unit'], row['Value'],row['Spaceing'],row['Sitename'],row['KhasraNo'],row['Latitude'],row['Longitude'],row['PlantCategory'],row['Species'],row['NoofPlant'])
#                                     mycursor.execute(sql, values)
#                                     mydb.commit()
#                                     sql = "INSERT INTO misreport (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s,%s)"
#                                     values = (row['Division'], row['District'], row['Range'], row['Block'],row['Beat'],row['Village'],row['Wing'],row['LandCategory'],row['Land'],row['Scheme'],row['PlantationMonth'],row['Unit'], row['Value'],row['Spaceing'],row['Sitename'],row['KhasraNo'],row['Latitude'],row['Longitude'],row['PlantCategory'],row['Species'],row['NoofPlant'])
#                                     mycursor.execute(sql, values)
#                                     mydb.commit()  
#                                     if request4_count>tunsubmit_count4:
#                                         delete_query = "DELETE FROM user4_uploaded_details ORDER BY id ASC LIMIT 1"
#                                         mycursor.execute(delete_query)
#                                         mydb.commit()

#                         elif 'name' in session and session['name'] == 'user5':
#                             if tunsubmit_count5==0:
#                                 error_message = "You have Submitted all Requested Form"
#                                 return error_message
#                             elif request5_count==tunsubmit_count5:
#                                 error_message = "Please First Download Requested Form"
#                                 return error_message
#                             else:
#                                 for _, row in csvData.iterrows():
                                    
#                                     sql = "INSERT INTO user5_form_details (id,Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s,%s)"
#                                     values = (row['id'],row['Division'], row['District'], row['Range'], row['Block'],row['Beat'],row['Village'],row['Wing'],row['LandCategory'],row['Land'],row['Scheme'],row['PlantationMonth'],row['Unit'], row['Value'],row['Spaceing'],row['Sitename'],row['KhasraNo'],row['Latitude'],row['Longitude'],row['PlantCategory'],row['Species'],row['NoofPlant'])
#                                     mycursor.execute(sql, values)
#                                     mydb.commit()
#                                     sql = "INSERT INTO misreport (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s,%s)"
#                                     values = (row['Division'], row['District'], row['Range'], row['Block'],row['Beat'],row['Village'],row['Wing'],row['LandCategory'],row['Land'],row['Scheme'],row['PlantationMonth'],row['Unit'], row['Value'],row['Spaceing'],row['Sitename'],row['KhasraNo'],row['Latitude'],row['Longitude'],row['PlantCategory'],row['Species'],row['NoofPlant'])
#                                     mycursor.execute(sql, values)
#                                     mydb.commit()
#                                     if request5_count>tunsubmit_count5:
#                                         delete_query = "DELETE FROM user5_uploaded_details ORDER BY id ASC LIMIT 1"
#                                         mycursor.execute(delete_query)
#                                         mydb.commit()    

#                         elif 'name' in session and session['name'] == 'user6':
#                             if tunsubmit_count6==0:
#                                 error_message = "You have Submitted all Requested Form"
#                                 return error_message
#                             elif request6_count==tunsubmit_count6:
#                                 error_message = "Please First Download Requested Form"
#                                 return error_message
#                             else:
#                                 for _, row in csvData.iterrows():
#                                     sql = "INSERT INTO user6_form_details (id,Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s,%s)"
#                                     values = (row['id'],row['Division'], row['District'], row['Range'], row['Block'],row['Beat'],row['Village'],row['Wing'],row['LandCategory'],row['Land'],row['Scheme'],row['PlantationMonth'],row['Unit'], row['Value'],row['Spaceing'],row['Sitename'],row['KhasraNo'],row['Latitude'],row['Longitude'],row['PlantCategory'],row['Species'],row['NoofPlant'])
#                                     mycursor.execute(sql, values)
#                                     mydb.commit()  
#                                     sql = "INSERT INTO misreport (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s,%s)"
#                                     values = (row['Division'], row['District'], row['Range'], row['Block'],row['Beat'],row['Village'],row['Wing'],row['LandCategory'],row['Land'],row['Scheme'],row['PlantationMonth'],row['Unit'], row['Value'],row['Spaceing'],row['Sitename'],row['KhasraNo'],row['Latitude'],row['Longitude'],row['PlantCategory'],row['Species'],row['NoofPlant'])
#                                     mycursor.execute(sql, values)
#                                     mydb.commit() 
#                                     if request6_count>tunsubmit_count6:
#                                         delete_query = "DELETE FROM user6_uploaded_details ORDER BY id ASC LIMIT 1"
#                                         mycursor.execute(delete_query)
#                                         mydb.commit()                                        

#             except ParserError:
#                 error_message = "The number of columns in the CSV file does not match the expected number of columns."
#                 return error_message

             

@app.route('/alert')
def alert():
    message = request.args.get('message', 'Submitted Successfully')
    
    if message == 'Submitted Successfully':
        success = True
    else:
        success = False
    
    return render_template('alert.html', message=message, success=success)

# @app.route("/download_recent", methods=['GET'])
# def download_recent():
    
    if 'name' in session and session['name'] == 'HQ user/ Admin':    
        query = "SELECT * FROM save_details ORDER BY id DESC LIMIT 1"
        mycursor.execute(query)
        recent_row = mycursor.fetchone()

        if recent_row:
            col_names = ['id','Division', 'District', 'Range', 'Block', 'Beat', 'Wing', 'LandCategory', 'Land', 'Scheme']
            recent_data = pd.DataFrame([recent_row], columns=col_names)
            csv_path = 'recent_row.csv'
            recent_data.to_csv(csv_path, index=False)
            return send_file(csv_path, as_attachment=True)
        else:
            return "No recent row found."
    
    elif 'name' in session and session['name'] == 'user1' :
        query1 = "SELECT * FROM user1_uploaded_details ORDER BY id ASC LIMIT 1"
        mycursor.execute(query1)
        all_rows = mycursor.fetchall()

        if all_rows:
            col_names = ['id', 'Division', 'District', 'Range', 'Block', 'Beat', 'Wing', 'LandCategory', 'Land', 'Scheme']
            all_data = pd.DataFrame(all_rows, columns=col_names)
            csv_path = 'all_rows.csv'
            all_data.to_csv(csv_path, index=False)

            insert_query = "INSERT INTO user1_save_details SELECT * FROM user1_uploaded_details ORDER BY id ASC LIMIT 1"
            mycursor.execute(insert_query)
            mydb.commit()

            delete_query = "DELETE FROM user1_uploaded_details ORDER BY id ASC LIMIT 1"
            mycursor.execute(delete_query)
            mydb.commit()

            return send_file(csv_path, as_attachment=True)
        else:
            return "No rows found in user1_uploaded_details."

    elif 'name' in session and session['name'] == 'user2' :
        query1 = "SELECT * FROM user2_uploaded_details ORDER BY id ASC LIMIT 1"
        mycursor.execute(query1)
        all_rows = mycursor.fetchall()

        if all_rows:
            col_names = ['id', 'Division', 'District', 'Range', 'Block', 'Beat', 'Wing', 'LandCategory', 'Land', 'Scheme']
            all_data = pd.DataFrame(all_rows, columns=col_names)
            csv_path = 'all_rows.csv'
            all_data.to_csv(csv_path, index=False)

            insert_query = "INSERT INTO user2_save_details SELECT * FROM user2_uploaded_details ORDER BY id ASC LIMIT 1"
            mycursor.execute(insert_query)
            mydb.commit()

            delete_query = "DELETE FROM user2_uploaded_details ORDER BY id ASC LIMIT 1"
            mycursor.execute(delete_query)
            mydb.commit()

            return send_file(csv_path, as_attachment=True)
        else:
            return "No rows found in user2_uploaded_details."
        
    elif 'name' in session and session['name'] == 'user3' :
        query1 = "SELECT * FROM user3_uploaded_details ORDER BY id ASC LIMIT 1"
        mycursor.execute(query1)
        all_rows = mycursor.fetchall()

        if all_rows:
            col_names = ['id', 'Division', 'District', 'Range', 'Block', 'Beat', 'Wing', 'LandCategory', 'Land', 'Scheme']
            all_data = pd.DataFrame(all_rows, columns=col_names)
            csv_path = 'all_rows.csv'
            all_data.to_csv(csv_path, index=False)

            insert_query = "INSERT INTO user3_save_details SELECT * FROM user3_uploaded_details ORDER BY id ASC LIMIT 1"
            mycursor.execute(insert_query)
            mydb.commit()

            delete_query = "DELETE FROM user3_uploaded_details ORDER BY id ASC LIMIT 1"
            mycursor.execute(delete_query)
            mydb.commit()
            return send_file(csv_path, as_attachment=True)
        else:
            return "No rows found in user3_uploaded_details."
        
    elif 'name' in session and session['name'] == 'user4' :
        query1 = "SELECT * FROM user4_uploaded_details ORDER BY id ASC LIMIT 1"
        mycursor.execute(query1)
        all_rows = mycursor.fetchall()

        if all_rows:
            col_names = ['id', 'Division', 'District', 'Range', 'Block', 'Beat', 'Wing', 'LandCategory', 'Land', 'Scheme']
            all_data = pd.DataFrame(all_rows, columns=col_names)
            csv_path = 'all_rows.csv'
            all_data.to_csv(csv_path, index=False)

            insert_query = "INSERT INTO user4_save_details SELECT * FROM user4_uploaded_details ORDER BY id ASC LIMIT 1"
            mycursor.execute(insert_query)
            mydb.commit()

            delete_query = "DELETE FROM user4_uploaded_details ORDER BY id ASC LIMIT 1"
            mycursor.execute(delete_query)
            mydb.commit()
            return send_file(csv_path, as_attachment=True)
        else:
            return "No rows found in user4_uploaded_details."
        
    elif 'name' in session and session['name'] == 'user5':
        query1 = "SELECT * FROM user5_uploaded_details ORDER BY id ASC LIMIT 1"
        mycursor.execute(query1)
        all_rows = mycursor.fetchall()

        if all_rows:
            col_names = ['id', 'Division', 'District', 'Range', 'Block', 'Beat', 'Wing', 'LandCategory', 'Land', 'Scheme']
            all_data = pd.DataFrame(all_rows, columns=col_names)
            csv_path = 'all_rows.csv'
            all_data.to_csv(csv_path, index=False)

            insert_query = "INSERT INTO user5_save_details SELECT * FROM user5_uploaded_details ORDER BY id ASC LIMIT 1"
            mycursor.execute(insert_query)
            mydb.commit()

            delete_query = "DELETE FROM user5_uploaded_details ORDER BY id ASC LIMIT 1"
            mycursor.execute(delete_query)
            mydb.commit()
            return send_file(csv_path, as_attachment=True)
        else:
            return "No rows found in user5_uploaded_details."
        
    elif 'name' in session and session['name'] == 'user6' :
        query1 = "SELECT * FROM user6_uploaded_details ORDER BY id ASC LIMIT 1"
        mycursor.execute(query1)
        all_rows = mycursor.fetchall()

        if all_rows:
            col_names = ['id', 'Division', 'District', 'Range', 'Block', 'Beat', 'Wing', 'LandCategory', 'Land', 'Scheme']
            all_data = pd.DataFrame(all_rows, columns=col_names)
            csv_path = 'all_rows.csv'
            all_data.to_csv(csv_path, index=False)

            insert_query = "INSERT INTO user6_save_details SELECT * FROM user6_uploaded_details ORDER BY id ASC LIMIT 1"
            mycursor.execute(insert_query)
            mydb.commit()

            delete_query = "DELETE FROM user6_uploaded_details ORDER BY id ASC LIMIT 1"
            mycursor.execute(delete_query)
            mydb.commit()
            return send_file(csv_path, as_attachment=True)
        else:
            return "No rows found in user6_uploaded_details."

@app.route('/send_form')
def send_form():
    return render_template('send_form.html')    

@app.route('/save_recent', methods=['POST'])
def save_recent():
    if 'name' in session and session['name'] == 'HQ user/ Admin':    
        
        if request.form.get('user1'):
            division = "Ambala"
            district = "Sonipat"
            range_value = "Sonipat"
            block = "Sonipat"
            beat = "Jagdishpur"
            village="Bara Gaon"
            wing = "Territorial"
            land_category = ""
            land = ""
            scheme = request.form['scheme']
            plantationmonth=""
            unit = 0
            value = 0
            spaceing = request.form['spaceing']
            sitename = ""
            khasraNo = ""
            latitude = ""
            longitude = ""
            plantcategory = ""
            species = request.form['species']
            noofplant = 0
            mycursor.execute('INSERT INTO user1_form (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
                                                                                                                                                                                                                                                                                                                                            plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
            mydb.commit()
            
            # return redirect(url_for('message1'))

        if request.form.get('user2'):
            division = "Faridabad"
            district = "Faridabad"
            range_value = "Faridabad"
            block = "Ballabgarh"
            beat = "Ballabgarh"
            village="Alampur"
            wing = "Territorial"
            land_category = ""
            land = ""
            scheme = request.form['scheme']
            plantationmonth=""
            unit = 0
            value = 0
            spaceing = request.form['spaceing']
            sitename = ""
            khasraNo = ""
            latitude = ""
            longitude = ""
            plantcategory = ""
            species = request.form['species']
            noofplant = 0
            mycursor.execute('INSERT INTO user2_form (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
                                                                                                                                                                                                                                                                                                                                            plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
            mydb.commit()
            
            # return redirect(url_for('message1'))
        if request.form.get('user3'):
            division = "Gurugram"
            district = "Gurugram"
            range_value = "Gurugram"
            block = "Gurugram"
            beat = "Wazirabad"
            village="Wazirabad"
            wing = "Territorial"
            land_category = ""
            land = ""
            scheme = request.form['scheme']
            plantationmonth=""
            unit = 0
            value = 0
            spaceing = request.form['spaceing']
            sitename = ""
            khasraNo = ""
            latitude = ""
            longitude = ""
            plantcategory = ""
            species = request.form['species']
            noofplant = 0
            mycursor.execute('INSERT INTO user3_form (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
                                                                                                                                                                                                                                                                                                                                            plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
            mydb.commit()
            
            # return redirect(url_for('message1'))
        if request.form.get('user4'):
            division = "Hisar"
            district = "Hisar"
            range_value = "Hisar"
            block = "Sonipat"
            beat = "Jagdishpur"
            village="Bara Gaon"
            wing = "Territorial"
            land_category = ""
            land = ""
            scheme = request.form['scheme']
            plantationmonth=""
            unit = 0
            value = 0
            spaceing = request.form['spaceing']
            sitename = ""
            khasraNo = ""
            latitude = ""
            longitude = ""
            plantcategory = ""
            species = request.form['species']
            noofplant = 0
            mycursor.execute('INSERT INTO user4_form (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
                                                                                                                                                                                                                                                                                                                                            plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
            mydb.commit()
            
            # return redirect(url_for('message1'))
        if request.form.get('user5'):
            division = "Rohtak"
            district = "Rohtak"
            range_value = "Rohtak"
            block = "Sonipat"
            beat = "Jagdishpur"
            village="Bara Gaon"
            wing = "Territorial"
            land_category = ""
            land = ""
            scheme = request.form['scheme']
            plantationmonth=""
            unit = 0
            value = 0
            spaceing = request.form['spaceing']
            sitename = ""
            khasraNo = ""
            latitude = ""
            longitude = ""
            plantcategory = ""
            species = request.form['species']
            noofplant = 0
            mycursor.execute('INSERT INTO user5_form (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
                                                                                                                                                                                                                                                                                                                                            plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
            mydb.commit()
            
            # return redirect(url_for('message1'))
        if request.form.get('user6'):
            division = "Karnal"
            district = "Karnal"
            range_value = "Karnal"
            block = "Sonipat"
            beat = "Jagdishpur"
            village="Bara Gaon"
            wing = "Territorial"
            land_category = ""
            land = ""
            scheme = request.form['scheme']
            plantationmonth=""
            unit = 0
            value = 0
            spaceing = request.form['spaceing']
            sitename = ""
            khasraNo = ""
            latitude = ""
            longitude = ""
            plantcategory = ""
            species = request.form['species']
            noofplant = 0
            mycursor.execute('INSERT INTO user6_form (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
                                                                                                                                                                                                                                                                                                                                            plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
            mydb.commit()
            
        return redirect(url_for('message1'))
        
                    
@app.route('/show_form', methods=['GET']) #Form shown in form of row
def show_form():
    if request.method == 'GET':
        mycursor.execute("SELECT * FROM user1_form_details")
        user1_rows = mycursor.fetchall()
        # Fetch data from user2_form
        mycursor.execute("SELECT * FROM user2_form_details")
        user2_rows = mycursor.fetchall()

        # Fetch data from user3_form
        mycursor.execute("SELECT * FROM user3_form_details")
        user3_rows = mycursor.fetchall()

        # Fetch data from user4_form
        mycursor.execute("SELECT * FROM user4_form_details")
        user4_rows = mycursor.fetchall()

        # Fetch data from user5_form
        mycursor.execute("SELECT * FROM user5_form_details")
        user5_rows = mycursor.fetchall()

        # Fetch data from user6_form
        mycursor.execute("SELECT * FROM user6_form_details")
        user6_rows = mycursor.fetchall()

        # Combine the results into a single list of rows
        rows = user1_rows+user2_rows + user3_rows + user4_rows + user5_rows + user6_rows

        return render_template('plantation.html', rows=rows)


@app.route('/add_details', methods=[ 'POST','GET'])#Form Submitted by user
def add_details():
            
   
    if 'name' in session and session['name'] == 'user1':
            mycursor.execute("SELECT * FROM user1_form")
            rows = mycursor.fetchall()
            record_id = int(rows[0][0])
    
            if request.method == 'GET':
                mycursor.execute("SELECT * FROM user1_form")

        # Fetch all the rows of the result
                rows = mycursor.fetchall()
                record_id=rows[0]
                return render_template('addplant.html', rows=rows)
            elif request.method == 'POST':
        
                division = request.form['field1']
                district = request.form['field2']
                range_value = request.form['field3']
                block =request.form['field4']
                beat = request.form['field5']
                village=request.form['field6']
                wing = request.form['field7']
                land_category =request.form['field8'] 
                land = request.form['field9']
                scheme = request.form['field10']
                plantationmonth=request.form['field11']
                unit = request.form['field12']
                value = request.form['field13']
                spaceing = request.form['field14']
                sitename = request.form['field15']
                khasraNo = request.form['field16']
                latitude = request.form['field17']
                longitude = request.form['field18']
                plantcategory = request.form['field19']
                species = request.form['field20']
                noofplant = request.form['field21']
                mycursor.execute('INSERT INTO user1_form_details (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (division, district, range_value, block, beat, village, wing, land_category, land, scheme,
                    plantationmonth, unit, value, spaceing, sitename, khasraNo, latitude, longitude, plantcategory, species, noofplant))
                mydb.commit()
                mycursor.execute('DELETE FROM user1_form ORDER BY id DESC LIMIT 1')
                mydb.commit()



                return redirect(url_for('message1'))
    elif 'name' in session and session['name'] == 'user2':
            mycursor.execute("SELECT * FROM user2_form")
            rows = mycursor.fetchall()
            
    
            if request.method == 'GET':
                mycursor.execute("SELECT * FROM user2_form")

        # Fetch all the rows of the result
                rows = mycursor.fetchall()
                
                return render_template('addplant.html', rows=rows)
            elif request.method == 'POST':
        
                division = request.form['field1']
                district = request.form['field2']
                range_value = request.form['field3']
                block =request.form['field4']
                beat = request.form['field5']
                village=request.form['field6']
                wing = request.form['field7']
                land_category =request.form['field8'] 
                land = request.form['field9']
                scheme = request.form['field10']
                plantationmonth=request.form['field11']
                unit = request.form['field12']
                value = request.form['field13']
                spaceing = request.form['field14']
                sitename = request.form['field15']
                khasraNo = request.form['field16']
                latitude = request.form['field17']
                longitude = request.form['field18']
                plantcategory = request.form['field19']
                species = request.form['field20']
                noofplant = request.form['field21']
                mycursor.execute('INSERT INTO user2_form_details (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (division, district, range_value, block, beat, village, wing, land_category, land, scheme,
                    plantationmonth, unit, value, spaceing, sitename, khasraNo, latitude, longitude, plantcategory, species, noofplant))
                mydb.commit()
                mycursor.execute('DELETE FROM user2_form ORDER BY id DESC LIMIT 1')
                mydb.commit()



                return redirect(url_for('message1'))
    elif 'name' in session and session['name'] == 'user3':
            mycursor.execute("SELECT * FROM user3_form")
            rows = mycursor.fetchall()
            
    
            if request.method == 'GET':
                mycursor.execute("SELECT * FROM user3_form")

        # Fetch all the rows of the result
                rows = mycursor.fetchall()
                
                return render_template('addplant.html', rows=rows)
            elif request.method == 'POST':
        
                division = request.form['field1']
                district = request.form['field2']
                range_value = request.form['field3']
                block =request.form['field4']
                beat = request.form['field5']
                village=request.form['field6']
                wing = request.form['field7']
                land_category =request.form['field8'] 
                land = request.form['field9']
                scheme = request.form['field10']
                plantationmonth=request.form['field11']
                unit = request.form['field12']
                value = request.form['field13']
                spaceing = request.form['field14']
                sitename = request.form['field15']
                khasraNo = request.form['field16']
                latitude = request.form['field17']
                longitude = request.form['field18']
                plantcategory = request.form['field19']
                species = request.form['field20']
                noofplant = request.form['field21']
                mycursor.execute('INSERT INTO user3_form_details (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (division, district, range_value, block, beat, village, wing, land_category, land, scheme,
                    plantationmonth, unit, value, spaceing, sitename, khasraNo, latitude, longitude, plantcategory, species, noofplant))
                mydb.commit()
                mycursor.execute('DELETE FROM user3_form ORDER BY id DESC LIMIT 1')
                mydb.commit()



                return redirect(url_for('message1'))
            
    elif 'name' in session and session['name'] == 'user4':
            mycursor.execute("SELECT * FROM user4_form")
            rows = mycursor.fetchall()
            
    
            if request.method == 'GET':
                mycursor.execute("SELECT * FROM user4_form")

        # Fetch all the rows of the result
                rows = mycursor.fetchall()
                
                return render_template('addplant.html', rows=rows)
            elif request.method == 'POST':
        
                division = request.form['field1']
                district = request.form['field2']
                range_value = request.form['field3']
                block =request.form['field4']
                beat = request.form['field5']
                village=request.form['field6']
                wing = request.form['field7']
                land_category =request.form['field8'] 
                land = request.form['field9']
                scheme = request.form['field10']
                plantationmonth=request.form['field11']
                unit = request.form['field12']
                value = request.form['field13']
                spaceing = request.form['field14']
                sitename = request.form['field15']
                khasraNo = request.form['field16']
                latitude = request.form['field17']
                longitude = request.form['field18']
                plantcategory = request.form['field19']
                species = request.form['field20']
                noofplant = request.form['field21']
                mycursor.execute('INSERT INTO user4_form_details (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (division, district, range_value, block, beat, village, wing, land_category, land, scheme,
                    plantationmonth, unit, value, spaceing, sitename, khasraNo, latitude, longitude, plantcategory, species, noofplant))
                mydb.commit()
                mycursor.execute('DELETE FROM user4_form ORDER BY id DESC LIMIT 1')
                mydb.commit()



                return redirect(url_for('message1'))
    elif 'name' in session and session['name'] == 'user5':
            mycursor.execute("SELECT * FROM user5_form")
            rows = mycursor.fetchall()
            
    
            if request.method == 'GET':
                mycursor.execute("SELECT * FROM user5_form")

        # Fetch all the rows of the result
                rows = mycursor.fetchall()
                
                return render_template('addplant.html', rows=rows)
            elif request.method == 'POST':
        
                division = request.form['field1']
                district = request.form['field2']
                range_value = request.form['field3']
                block =request.form['field4']
                beat = request.form['field5']
                village=request.form['field6']
                wing = request.form['field7']
                land_category =request.form['field8'] 
                land = request.form['field9']
                scheme = request.form['field10']
                plantationmonth=request.form['field11']
                unit = request.form['field12']
                value = request.form['field13']
                spaceing = request.form['field14']
                sitename = request.form['field15']
                khasraNo = request.form['field16']
                latitude = request.form['field17']
                longitude = request.form['field18']
                plantcategory = request.form['field19']
                species = request.form['field20']
                noofplant = request.form['field21']
                mycursor.execute('INSERT INTO user5_form_details (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (division, district, range_value, block, beat, village, wing, land_category, land, scheme,
                    plantationmonth, unit, value, spaceing, sitename, khasraNo, latitude, longitude, plantcategory, species, noofplant))
                mydb.commit()
                mycursor.execute('DELETE FROM user5_form ORDER BY id DESC LIMIT 1')
                mydb.commit()



                return redirect(url_for('message1'))
            
    elif 'name' in session and session['name'] == 'user6':
            mycursor.execute("SELECT * FROM user6_form")
            rows = mycursor.fetchall()
            
    
            if request.method == 'GET':
                mycursor.execute("SELECT * FROM user6_form")

        # Fetch all the rows of the result
                rows = mycursor.fetchall()
                
                return render_template('addplant.html', rows=rows)
            elif request.method == 'POST':
        
                division = request.form['field1']
                district = request.form['field2']
                range_value = request.form['field3']
                block =request.form['field4']
                beat = request.form['field5']
                village=request.form['field6']
                wing = request.form['field7']
                land_category =request.form['field8'] 
                land = request.form['field9']
                scheme = request.form['field10']
                plantationmonth=request.form['field11']
                unit = request.form['field12']
                value = request.form['field13']
                spaceing = request.form['field14']
                sitename = request.form['field15']
                khasraNo = request.form['field16']
                latitude = request.form['field17']
                longitude = request.form['field18']
                plantcategory = request.form['field19']
                species = request.form['field20']
                noofplant = request.form['field21']
                mycursor.execute('INSERT INTO user6_form_details (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (division, district, range_value, block, beat, village, wing, land_category, land, scheme,
                    plantationmonth, unit, value, spaceing, sitename, khasraNo, latitude, longitude, plantcategory, species, noofplant))
                mydb.commit()
                mycursor.execute('DELETE FROM user6_form ORDER BY id DESC LIMIT 1')
                mydb.commit()



                return redirect(url_for('message1'))
            
        
            # mycursor.execute('INSERT INTO user1_form_details (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
            #                                                                                                                                                                                                                                                                                                                               plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
            # mydb.commit()
            # mycursor.execute('INSERT INTO misreport (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
            #                                                                                                                                                                                                                                                                                                                                 plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
            # mydb.commit()
        
            # return redirect(url_for('message'))
    
    # elif 'name' in session and session['name'] == 'user2' and tunsubmit_count2>0:
    #     if request2_count==tunsubmit_count2:
    #         msg="Please First Download Requested Form"
    #         return redirect(url_for('message',  message=msg))
    #     else:
    #         mycursor.execute('INSERT INTO user2_form_details (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
    #                                                                                                                                                                                                                                                                                                                                       plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
    #         mydb.commit()
    #         mycursor.execute('INSERT INTO misreport (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
    #                                                                                                                                                                                                                                                                                                                                         plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
    #         mydb.commit()
        
    #     return redirect(url_for('message'))
    
    # elif 'name' in session and session['name'] == 'user3' and tunsubmit_count3>0:
    #     if request3_count==tunsubmit_count3:
    #         msg="Please First Download Requested Form"
    #         return redirect(url_for('message',  message=msg))
    #     else:
    #         mycursor.execute('INSERT INTO user3_form_details (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
    #                                                                                                                                                                                                                                                                                                                                       plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
    #         mydb.commit()
    #         mycursor.execute('INSERT INTO misreport (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
    #                                                                                                                                                                                                                                                                                                                                         plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
    #         mydb.commit()

       
    #     return redirect(url_for('message'))
    
    # elif 'name' in session and session['name'] == 'user4' and tunsubmit_count4>0:
    #     if request4_count==tunsubmit_count4:
    #         msg="Please First Download Requested Form"
    #         return redirect(url_for('message',  message=msg))
    #     else:
    #         mycursor.execute('INSERT INTO user4_form_details (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
    #                                                                                                                                                                                                                                                                                                                                       plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
    #         mydb.commit()
    #         mycursor.execute('INSERT INTO misreport (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
    #                                                                                                                                                                                                                                                                                                                                         plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
    #         mydb.commit()

        
    #     return redirect(url_for('message'))
    
    # elif 'name' in session and session['name'] == 'user5' and tunsubmit_count5>0:
    #     if request5_count==tunsubmit_count5:
    #         msg="Please First Download Requested Form"
    #         return redirect(url_for('message',  message=msg))
    #     else:
    #         mycursor.execute('INSERT INTO user5_form_details (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
    #                                                                                                                                                                                                                                                                                                                                       plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
    #         mydb.commit()
    #         mycursor.execute('INSERT INTO misreport (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
    #                                                                                                                                                                                                                                                                                                                                         plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
    #         mydb.commit()

        
    #     return redirect(url_for('message'))
    
    # elif 'name' in session and session['name'] == 'user6' and tunsubmit_count6>0:
    #     if request6_count==tunsubmit_count6:
    #         msg="Please First Download Requested Form"
    #         return redirect(url_for('message',  message=msg))
    #     else:
    #         mycursor.execute('INSERT INTO user6_form_details (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
    #                                                                                                                                                                                                                                                                                                                                       plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
    #         mydb.commit()
    #         mycursor.execute('INSERT INTO misreport (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
    #                                                                                                                                                                                                                                                                                                                                         plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
    #         mydb.commit()
    #         return redirect(url_for('message'))
    # else:
    #     msg="You Have Submitted all form"
    #     return redirect(url_for('message',  message=msg))

@app.route('/saved_form', methods=['POST'])#Accept and reject submitted form
def saved_form():
    if 'accept_button' in request.form:
        row_id = request.form['accept_button']
        # Retrieve the data associated with the row_id
        division = request.form['division_' + row_id]
        district = request.form['district_' + row_id]
        range_val = request.form['range_' + row_id]
        block = request.form['block_' + row_id]
        beat = request.form['beat_' + row_id]
        village = request.form['village_' + row_id]
        wing = request.form['wing_' + row_id]
        land_category = request.form['land_category_' + row_id]
        land = request.form['land_' + row_id]
        schema = request.form['schema_' + row_id]
        plantation_month = request.form['plantation_month_' + row_id]
        unit = request.form['unit_' + row_id]
        value = request.form['value_' + row_id]
        spacing = request.form['spacing_' + row_id]
        site_name = request.form['site_name_' + row_id]
        khasra_no = request.form['khasra_no_' + row_id]
        latitude = request.form['latitude_' + row_id]
        longitude = request.form['longitude_' + row_id]
        plant_category = request.form['plant_category_' + row_id]
        species = request.form['species_' + row_id]
        no_of_plant = request.form['no_of_plant_' + row_id]

        sql = "INSERT INTO user2 (Division, District,  `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (division, district, range_val, block, beat, village, wing, land_category, land, schema, plantation_month, unit, value, spacing, site_name, khasra_no, latitude, longitude, plant_category, species, no_of_plant)
        mycursor.execute(sql, val)
        mydb.commit()
        sql = "INSERT INTO misreport (Division, District,  `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (division, district, range_val, block, beat, village, wing, land_category, land, schema, plantation_month, unit, value, spacing, site_name, khasra_no, latitude, longitude, plant_category, species, no_of_plant)
        mycursor.execute(sql, val)
        mydb.commit()
        if division == "Ambala":
            delete_query = "DELETE FROM user1_form_details WHERE id = %s"
            delete_val = (row_id,)
            mycursor.execute(delete_query, delete_val)
            mydb.commit()
        elif division == "Faridabad":
            delete_query = "DELETE FROM user2_form_details WHERE id = %s"
            delete_val = (row_id,)
            mycursor.execute(delete_query, delete_val)
            mydb.commit()
        elif division == "Gurugram":
            delete_query = "DELETE FROM user3_form_details WHERE id = %s"
            delete_val = (row_id,)
            mycursor.execute(delete_query, delete_val)
            mydb.commit()
        elif division == "Hisar":
            delete_query = "DELETE FROM user4_form_details WHERE id = %s"
            delete_val = (row_id,)
            mycursor.execute(delete_query, delete_val)
            mydb.commit()
        elif division == "Rohtak":
            delete_query = "DELETE FROM user5_form_details WHERE id = %s"
            delete_val = (row_id,)
            mycursor.execute(delete_query, delete_val)
            mydb.commit()
        elif division == "Karnal":
            delete_query = "DELETE FROM user6_form_details WHERE id = %s"
            delete_val = (row_id,)
            mycursor.execute(delete_query, delete_val)
            mydb.commit()
        return redirect('/show_form')
    
    elif 'reject_button' in request.form:
        row_id = request.form['reject_button']
        # Retrieve the data associated with the row_id
        division = request.form['division_' + row_id]
        district = request.form['district_' + row_id]
        range_val = request.form['range_' + row_id]
        block = request.form['block_' + row_id]
        beat = request.form['beat_' + row_id]
        village = request.form['village_' + row_id]
        wing = request.form['wing_' + row_id]
        land_category = request.form['land_category_' + row_id]
        land = request.form['land_' + row_id]
        schema = request.form['schema_' + row_id]
        plantation_month = request.form['plantation_month_' + row_id]
        unit = request.form['unit_' + row_id]
        value = request.form['value_' + row_id]
        spacing = request.form['spacing_' + row_id]
        site_name = request.form['site_name_' + row_id]
        khasra_no = request.form['khasra_no_' + row_id]
        latitude = request.form['latitude_' + row_id]
        longitude = request.form['longitude_' + row_id]
        plant_category = request.form['plant_category_' + row_id]
        species = request.form['species_' + row_id]
        no_of_plant = request.form['no_of_plant_' + row_id]

        if division == "Ambala":
            sql = "INSERT INTO user1_form (Division, District,  `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (division, district, range_val, block, beat, village, wing, land_category, land, schema, plantation_month, unit, value, spacing, site_name, khasra_no, latitude, longitude, plant_category, species, no_of_plant)
            mycursor.execute(sql, val)
            mydb.commit()
            delete_query = "DELETE FROM user1_form_details WHERE id = %s"
            delete_val = (row_id,)
            mycursor.execute(delete_query, delete_val)
            mydb.commit()
        elif division == "Faridabad":
            sql = "INSERT INTO user2_form (Division, District,  `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (division, district, range_val, block, beat, village, wing, land_category, land, schema, plantation_month, unit, value, spacing, site_name, khasra_no, latitude, longitude, plant_category, species, no_of_plant)
            mycursor.execute(sql, val)
            mydb.commit()
            delete_query = "DELETE FROM user2_form_details WHERE id = %s"
            delete_val = (row_id,)
            mycursor.execute(delete_query, delete_val)
            mydb.commit()
        elif division == "Gurugram":
            delete_query = "DELETE FROM user3_form_details WHERE id = %s"
            delete_val = (row_id,)
            mycursor.execute(delete_query, delete_val)
            mydb.commit()
            sql = "INSERT INTO user3_form (Division, District,  `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (division, district, range_val, block, beat, village, wing, land_category, land, schema, plantation_month, unit, value, spacing, site_name, khasra_no, latitude, longitude, plant_category, species, no_of_plant)
            mycursor.execute(sql, val)
            mydb.commit()
        elif division == "Hisar":
            sql = "INSERT INTO user4_form (Division, District,  `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (division, district, range_val, block, beat, village, wing, land_category, land, schema, plantation_month, unit, value, spacing, site_name, khasra_no, latitude, longitude, plant_category, species, no_of_plant)
            mycursor.execute(sql, val)
            mydb.commit()
            delete_query = "DELETE FROM user4_form_details WHERE id = %s"
            delete_val = (row_id,)
            mycursor.execute(delete_query, delete_val)
            mydb.commit()
        elif division == "Rohtak":
            sql = "INSERT INTO user5_form (Division, District,  `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (division, district, range_val, block, beat, village, wing, land_category, land, schema, plantation_month, unit, value, spacing, site_name, khasra_no, latitude, longitude, plant_category, species, no_of_plant)
            mycursor.execute(sql, val)
            mydb.commit()
            delete_query = "DELETE FROM user5_form_details WHERE id = %s"
            delete_val = (row_id,)
            mycursor.execute(delete_query, delete_val)
            mydb.commit()
        elif division == "Karnal":
            sql = "INSERT INTO user6_form (Division, District,  `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (division, district, range_val, block, beat, village, wing, land_category, land, schema, plantation_month, unit, value, spacing, site_name, khasra_no, latitude, longitude, plant_category, species, no_of_plant)
            mycursor.execute(sql, val)
            mydb.commit()
            delete_query = "DELETE FROM user6_form_details WHERE id = %s"
            delete_val = (row_id,)
            mycursor.execute(delete_query, delete_val)
            mydb.commit()    
        return redirect('/show_form')

@app.route('/message')
def message():
    message = request.args.get('message', 'Submitted Successfully')
    
    if message == ' Submitted Successfully':
        success = True
    else:
        success = False
    
    return render_template('message.html', message=message, success=success)

@app.route('/send_email', methods=['POST'])
def send_email():
    msg=""
    # Set up the SMTP server details
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'prakhar060703@gmail.com'
    smtp_password = 'otxgdixydquwfybr'

    # Compose the email
    sender_email = 'prakhar060703@gmail.com'
    receiver_email = 'prakhar060703@gmail.com'
    subject = 'Hello, World!'
    message = 'This is a reminder from Forest Department Please Submit requested form.'

    # Check if the "user1" checkbox is selected
    user1_checkbox_selected = request.form.get('user1') is not None
    user2_checkbox_selected = request.form.get('user2') is not None
    user3_checkbox_selected = request.form.get('user3') is not None
    user4_checkbox_selected = request.form.get('user4') is not None
    user5_checkbox_selected = request.form.get('user5') is not None
    user6_checkbox_selected = request.form.get('user6') is not None

    receiver_emails = []
    if user1_checkbox_selected:  
        receiver_emails.append('prakhar060703@gmail.com') 
    if user2_checkbox_selected:
        receiver_emails.append('dcsingh@yahoo.com') 
    if user3_checkbox_selected:
        receiver_emails.append('Deep.Singh@otomation.com')
    if user4_checkbox_selected:
        receiver_emails.append('20cs3044@rgipt.ac.in') 
    if user5_checkbox_selected:
        receiver_emails.append('saurabhmishra7c@gmail.com')
    if user6_checkbox_selected:
        receiver_emails.append('20cs3010@rgipt.ac.in')
    # Perform your notification sending logic based on the form data
    
        # Create a multipart message and set the headers
    

        # Attach the message to the email
    

        # Create a SMTP session
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Enable secure connection
        server.login(smtp_username, smtp_password)
        for receiver_email in receiver_emails:
            # Create a multipart message and set the headers
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            # Attach the message to the email
            msg.attach(MIMEText(message, 'plain'))

            # Send the email
            server.send_message(msg)
        

    msg='Email sent successfully to ' + ', '.join(receiver_emails)
    return msg
   
@app.route('/mail')
def mail():
    message = request.args.get('message', 'Email not sent')
    
    if message == 'Email not sent':
        success = False
    else:
        success = True
    
    return render_template('mail.html', message=message, success=success)

class City:
    def __init__(self, id, division, district,block,species,khasra,site,scheme,plantcategory,value5,value6,plantationdate,land,landcategory,unit,spaceing):
        self.id = id
        self.division = division
        self.district = district
        self.block = block
        self.species=species
        self.khasra=khasra
        self.site=site
        self.scheme=scheme
        self.plantcategory=plantcategory
        self.value5=value5
        self.value6=value6
        self.plantationdate=plantationdate
        self.land=land
        self.landcategory=landcategory
        self.unit=unit
        self.spaceing=spaceing




@app.route('/mis', methods=['GET'])
def mis():
    return render_template('mis.html', cities=None)

@app.route('/mis', methods=['POST'])
def mis1():
    try:
        if request.method == 'POST':
            division = request.form['division']
            district = request.form['district']
            block = request.form['block']
            species = request.form['species']
            khasra = request.form['khasra']
            site = request.form['site']
            scheme = request.form['scheme']
            plantcategory = request.form['plantcategory']
            value5 = request.form['value5']
            value6 = request.form['value6']

            query = "SELECT id, Division, District, Block, Species, KhasraNo, Sitename, Scheme, PlantCategory, Value, NoofPlant, PlantationMonth, Land, LandCategory, Unit, Spaceing FROM misreport WHERE 1=1"
            parameters = []

            if division:
                query += " AND Division = %s"
                parameters.append(division)
            if district:
                query += " AND District = %s"
                parameters.append(district)
            if block:
                query += " AND Block = %s"
                parameters.append(block)
            if species:
                query += " AND Species = %s"
                parameters.append(species)
            if khasra:
                query += " AND KhasraNo = %s"
                parameters.append(khasra) 
            if site:
                query += " AND Sitename = %s"
                parameters.append(site) 
            if scheme:
                query += " AND Scheme = %s"
                parameters.append(scheme) 
            if plantcategory:
                query += " AND PlantCategory = %s"
                parameters.append(plantcategory)
            if value5:
                query += " AND Value = %s"
                parameters.append(value5)
            if value6:
                query += " AND NoofPlant = %s"
                parameters.append(value6) 

            if parameters:
                mycursor.fetchall()  # Consume any remaining unread results
                mycursor.execute(query, tuple(parameters))
                
                result = mycursor.fetchall()
                cities = []
                for row in result:
                    city = City(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15])
                    cities.append(city)
                    query = "INSERT INTO searchquery ( Division, District, Block, Species, KhasraNo, Sitename, Scheme, PlantCategory, Value, NoofPlant, PlantationMonth, Land, LandCategory, Unit, Spaceing) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    values = (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14],row[15])
                    mycursor.execute(query, values)
                    mydb.commit()
                
                return render_template('mis.html', cities=cities)
            else:
                return render_template('mis.html', cities=None)

        return render_template('mis.html', cities=None)
    except Exception as e:
        # Handle the error gracefully
        # print("An error occurred:", str(e))
        return []

@app.route('/clear')
def clear():
    delete_query = "DELETE FROM searchquery"
    mycursor.execute(delete_query)

# Commit the changes
    mydb.commit()

    return redirect(url_for('mis'))


@app.route('/print_csv')
def print_csv():
    query = "SELECT * FROM searchquery"
    mycursor.execute(query)
    rows = mycursor.fetchall()

    if rows:
        col_names = ['id', 'Division', 'District', 'Block', 'Species', 'KhasraNo', 'Sitename', 'Scheme', 'PlantCategory', 'Value', 'NoofPlant', 'PlantationMonth', 'Land', 'LandCategory', 'Unit', 'Spaceing']
        data = pd.DataFrame(rows, columns=col_names)
        csv_path = 'all_rows.csv'
        data.to_csv(csv_path, index=False)
        return send_file(csv_path, as_attachment=True)
    else:
        return "No rows found in the table."


def get_divisions():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM division")  # Corrected table name
    divisions = mycursor.fetchall()
    mycursor.close()
    return divisions

@app.route('/division')
def division():
    divisions = get_divisions()
    return render_template('division.html', divisions=divisions)

@app.route('/add', methods=['POST'])
def add_division():
    division_name = request.form['division']
    division_id= request.form['id']
    mycursor = mydb.cursor()
    query = "INSERT INTO division (id,Division) VALUES (%s,%s)"  # Corrected table name
    values = (division_id,division_name,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('division'))

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
        return redirect(url_for('division'))

@app.route('/delete/<int:division_id>', methods=['POST'])
def delete_division(division_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM division WHERE id = %s"  # Corrected table name
    values = (division_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('division'))

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

@app.route('/add_page')
def add_page():
    return render_template('division_addblock.html')


@app.route('/edit_selected_divisions', methods=['GET', 'POST'])
def edit_selected_divisions():
    if request.method == 'GET':
        selected_division_ids = request.args.get('division_ids').split(',')

        # Perform the editing for each selected division
        divisions = []
        for division_id in selected_division_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM division WHERE id = %s"
            values = (division_id,)
            mycursor.execute(query, values)
            division = mycursor.fetchone()
            mycursor.close()
            if division:
                divisions.append(division)

        return render_template('edit_divisions.html', divisions=divisions)

    elif request.method == 'POST':
         # Retrieve the new division names from the form
        new_names = {}
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                division_id = key.split('_')[2]  # Extract the division ID from the key
                new_names[division_id] = value

        # Perform the editing for each selected division
        for division_id, new_name in new_names.items():
            # Perform the necessary update operations for the division
            mycursor = mydb.cursor()
            query = "UPDATE division SET Division = %s WHERE id = %s"
            values = (new_name, division_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

        return redirect(url_for('division'))


@app.route('/delete_selected_divisions', methods=['GET'])
def delete_selected_divisions():
        selected_division_ids = request.args.get('division_ids').split(',')

        # Perform the editing for each selected division
        for division_id in selected_division_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM division WHERE id = %s"
            values = (division_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('division')) 




def get_districts():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM district")  # Corrected table name
    districts = mycursor.fetchall()
    mycursor.close()
    return districts

@app.route('/district')
def district():
    districts = get_districts()
    return render_template('district.html', districts=districts)

@app.route('/add1', methods=['POST'])
def add_district():
    division_name=request.form['division']
    district_name = request.form['district']
    division_id= request.form['id']
    mycursor = mydb.cursor()
    query = "INSERT INTO district (id,Division,District) VALUES (%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('district'))

@app.route('/edit_district/<int:district_id>', methods=['GET', 'POST'])
def edit_district(district_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM district WHERE id = %s"  # Corrected table name
        values = (district_id,)
        mycursor.execute(query, values)
        district = mycursor.fetchone()
        mycursor.close()
        return render_template('district_edit.html', district=district)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        mycursor = mydb.cursor()
        query = "UPDATE district SET Division = %s, id=%s, District=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3, district_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('district'))

@app.route('/delete_district/<int:district_id>', methods=['POST'])
def delete_district(district_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM district WHERE id = %s"  # Corrected table name
    values = (district_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('district'))

@app.route('/search_district', methods=['POST'])
def search_district():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM district WHERE District LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    districts = mycursor.fetchall()
    mycursor.close()
    return render_template('district.html', districts=districts)

@app.route('/add_page1')
def add_page1():
    return render_template('district_addblock.html')


@app.route('/edit_selected_districts', methods=['GET', 'POST'])
def edit_selected_districts():
    if request.method == 'GET':
        selected_district_ids = request.args.get('districts_ids').split(',')

        # Perform the editing for each selected division
        districts = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM district WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            district = mycursor.fetchone()
            mycursor.close()
            if district:
                districts.append(district)

        return render_template('edit_districts.html', districts=districts)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_districts = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                district_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{district_id}')
                updated_districts.append((district_id, division_name, district_name))

        # Perform the editing for each selected district
        for district in updated_districts:
            district_id, division_name, district_name = district
            mycursor = mydb.cursor()
            query = "UPDATE district SET Division = %s, District = %s WHERE id = %s"
            values = (division_name, district_name, district_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('district'))


@app.route('/delete_selected_districts', methods=['GET'])
def delete_selected_districts():
        selected_district_ids = request.args.get('districts_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM district WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('district')) 

#Now for Block

def get_blocks():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM block")  # Corrected table name
    blocks = mycursor.fetchall()
    mycursor.close()
    return blocks

@app.route('/block')
def block():
    blocks = get_blocks()
    return render_template('block.html', blocks=blocks)

@app.route('/add2', methods=['POST'])
def add_block():
    division_name=request.form['division']
    district_name = request.form['district']
    division_id= request.form['id']
    block_name=request.form['block']
    mycursor = mydb.cursor()
    query = "INSERT INTO block (id,Division,District,Blockname) VALUES (%s,%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name,block_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('block'))

@app.route('/edit_block/<int:block_id>', methods=['GET', 'POST'])
def edit_block(block_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM block WHERE id = %s"  # Corrected table name
        values = (block_id,)
        mycursor.execute(query, values)
        block = mycursor.fetchone()
        mycursor.close()
        return render_template('block_edit.html', block=block)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        new_name4 = request.form['new_name4']
        mycursor = mydb.cursor()
        query = "UPDATE block SET Division = %s, id=%s, District=%s, Blockname=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3,new_name4, block_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('block'))

@app.route('/delete_block/<int:block_id>', methods=['POST'])
def delete_block(block_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM block WHERE id = %s"  # Corrected table name
    values = (block_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('block'))

@app.route('/search_block', methods=['POST'])
def search_block():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM block WHERE Blockname LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    blocks = mycursor.fetchall()
    mycursor.close()
    return render_template('block.html', blocks=blocks)

@app.route('/add_page2')
def add_page2():
    return render_template('block_addblock.html')


@app.route('/edit_selected_blocks', methods=['GET', 'POST'])
def edit_selected_blocks():
    if request.method == 'GET':
        selected_district_ids = request.args.get('blocks_ids').split(',')

        # Perform the editing for each selected division
        blocks = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM block WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            block = mycursor.fetchone()
            mycursor.close()
            if block:
                blocks.append(block)

        return render_template('edit_blocks.html', blocks=blocks)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_blocks = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                block_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{block_id}')
                block_name = request.form.get(f'new_name2_{block_id}')
                updated_blocks.append((block_id, division_name, district_name,block_name))

        # Perform the editing for each selected district
        for block in updated_blocks:
            block_id, division_name, district_name,block_name = block
            mycursor = mydb.cursor()
            query = "UPDATE block SET Division = %s, District = %s, Blockname = %s WHERE id = %s"
            values = (division_name, district_name,block_name, block_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('block'))


@app.route('/delete_selected_blocks', methods=['GET'])
def delete_selected_blocks():
        selected_district_ids = request.args.get('blocks_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM block WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('block')) 


#Now for Village

def get_villages():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM village")  # Corrected table name
    villages = mycursor.fetchall()
    mycursor.close()
    return villages

@app.route('/village')
def village():
    villages = get_villages()
    return render_template('village.html', villages=villages)

@app.route('/add3', methods=['POST'])
def add_village():
    division_name=request.form['division']
    district_name = request.form['district']
    division_id= request.form['id']
    block_name=request.form['block']
    village_name=request.form['village']
    mycursor = mydb.cursor()
    query = "INSERT INTO village (id,Division,District,Blockname,Village) VALUES (%s,%s,%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name,block_name,village_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('village'))

@app.route('/edit_village/<int:village_id>', methods=['GET', 'POST'])
def edit_village(village_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM village WHERE id = %s"  # Corrected table name
        values = (village_id,)
        mycursor.execute(query, values)
        village = mycursor.fetchone()
        mycursor.close()
        return render_template('village_edit.html', village=village)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        new_name4 = request.form['new_name4']
        new_name5 = request.form['new_name5']
        mycursor = mydb.cursor()
        query = "UPDATE village SET Division = %s, id=%s, District=%s, Blockname=%s, Village=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3,new_name4,new_name5, village_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('village'))

@app.route('/delete_village/<int:village_id>', methods=['POST'])
def delete_village(village_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM village WHERE id = %s"  # Corrected table name
    values = (village_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('village'))

@app.route('/search_village', methods=['POST'])
def search_village():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM village WHERE Village LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    villages = mycursor.fetchall()
    mycursor.close()
    return render_template('village.html', villages=villages)

@app.route('/add_page3')
def add_page3():
    return render_template('village_addblock.html')


@app.route('/edit_selected_villages', methods=['GET', 'POST'])
def edit_selected_villages():
    if request.method == 'GET':
        selected_district_ids = request.args.get('villages_ids').split(',')

        # Perform the editing for each selected division
        villages = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM village WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            village = mycursor.fetchone()
            mycursor.close()
            if village:
                villages.append(village)

        return render_template('edit_villages.html', villages=villages)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_villages = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                village_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{village_id}')
                block_name = request.form.get(f'new_name2_{village_id}')
                village_name = request.form.get(f'new_name3_{village_id}')
                updated_villages.append((village_id, division_name, district_name,block_name,village_name))

        # Perform the editing for each selected district
        for village in updated_villages:
            village_id, division_name, district_name,block_name, village_name = village
            mycursor = mydb.cursor()
            query = "UPDATE village SET Division = %s, District = %s, Blockname = %s, Village=%s WHERE id = %s"
            values = (division_name, district_name,block_name, village_id,village_name)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('village'))


@app.route('/delete_selected_villages', methods=['GET'])
def delete_selected_villages():
        selected_district_ids = request.args.get('villages_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM village WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('village')) 

#Now for Range

def get_ranges():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM ranget")  # Corrected table name
    ranges = mycursor.fetchall()
    mycursor.close()
    return ranges

@app.route('/range')
def range():
    ranges = get_ranges()
    return render_template('range.html', ranges=ranges)

@app.route('/add4', methods=['POST'])
def add_range():
    division_name=request.form['division']
    district_name = request.form['district']
    division_id= request.form['id']
    range_name=request.form['range']
    mycursor = mydb.cursor()
    query = "INSERT INTO ranget (id,Division,District,Ranget) VALUES (%s,%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name,range_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('range'))

@app.route('/edit_range/<int:range_id>', methods=['GET', 'POST'])
def edit_range(range_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM ranget WHERE id = %s"  # Corrected table name
        values = (range_id,)
        mycursor.execute(query, values)
        range = mycursor.fetchone()
        mycursor.close()
        return render_template('range_edit.html', range=range)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        new_name4 = request.form['new_name4']
        mycursor = mydb.cursor()
        query = "UPDATE ranget SET Division = %s, id=%s, District=%s, Ranget=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3,new_name4, range_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('range'))

@app.route('/delete_range/<int:range_id>', methods=['POST'])
def delete_range(range_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM ranget WHERE id = %s"  # Corrected table name
    values = (range_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('range'))

@app.route('/search_range', methods=['POST'])
def search_range():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM ranget WHERE Ranget LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    ranges = mycursor.fetchall()
    mycursor.close()
    return render_template('range.html', ranges=ranges)

@app.route('/add_page4')
def add_page4():
    return render_template('range_addblock.html')


@app.route('/edit_selected_ranges', methods=['GET', 'POST'])
def edit_selected_ranges():
    if request.method == 'GET':
        selected_district_ids = request.args.get('ranges_ids').split(',')

        # Perform the editing for each selected division
        ranges = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM ranget WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            block = mycursor.fetchone()
            mycursor.close()
            if block:
                ranges.append(block)

        return render_template('edit_ranges.html', ranges=ranges)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_ranges = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                range_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{range_id}')
                range_name = request.form.get(f'new_name2_{range_id}')
                updated_ranges.append((range_id, division_name, district_name,range_name))

        # Perform the editing for each selected district
        for block in updated_ranges:
            range_id, division_name, district_name,range_name = block
            mycursor = mydb.cursor()
            query = "UPDATE ranget SET Division = %s, District = %s, Ranget = %s WHERE id = %s"
            values = (division_name, district_name,range_name, range_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('range'))


@app.route('/delete_selected_ranges', methods=['GET'])
def delete_selected_ranges():
        selected_district_ids = request.args.get('ranges_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM ranget WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('range')) 

#Now for Beat
def get_beats():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM beat")  # Corrected table name
    beats = mycursor.fetchall()
    mycursor.close()
    return beats

@app.route('/beat')
def beat():
    beats = get_beats()
    return render_template('beat.html', beats=beats)

@app.route('/add5', methods=['POST'])
def add_beat():
    division_name=request.form['division']
    district_name = request.form['district']
    division_id= request.form['id']
    beat_name=request.form['beat']
    mycursor = mydb.cursor()
    query = "INSERT INTO beat (id,Division,District,Beat) VALUES (%s,%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name,beat_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('beat'))

@app.route('/edit_beat/<int:beat_id>', methods=['GET', 'POST'])
def edit_beat(beat_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM beat WHERE id = %s"  # Corrected table name
        values = (beat_id,)
        mycursor.execute(query, values)
        beat = mycursor.fetchone()
        mycursor.close()
        return render_template('beat_edit.html', beat=beat)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        new_name4 = request.form['new_name4']
        mycursor = mydb.cursor()
        query = "UPDATE beat SET Division = %s, id=%s, District=%s, Beat=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3,new_name4, beat_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('beat'))

@app.route('/delete_beat/<int:beat_id>', methods=['POST'])
def delete_beat(beat_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM beat WHERE id = %s"  # Corrected table name
    values = (beat_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('beat'))

@app.route('/search_beat', methods=['POST'])
def search_beat():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM beat WHERE Beat LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    beats = mycursor.fetchall()
    mycursor.close()
    return render_template('beat.html', beats=beats)

@app.route('/add_page5')
def add_page5():
    return render_template('beat_addblock.html')


@app.route('/edit_selected_beats', methods=['GET', 'POST'])
def edit_selected_beats():
    if request.method == 'GET':
        selected_district_ids = request.args.get('beats_ids').split(',')

        # Perform the editing for each selected division
        beats = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM beat WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            block = mycursor.fetchone()
            mycursor.close()
            if block:
                beats.append(block)

        return render_template('edit_beats.html', beats=beats)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_beats = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                beat_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{beat_id}')
                beat_name = request.form.get(f'new_name2_{beat_id}')
                updated_beats.append((beat_id, division_name, district_name,beat_name))

        # Perform the editing for each selected district
        for block in updated_beats:
            beat_id, division_name, district_name,beat_name = block
            mycursor = mydb.cursor()
            query = "UPDATE beat SET Division = %s, District = %s, Beat = %s WHERE id = %s"
            values = (division_name, district_name,beat_name, beat_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('beat'))


@app.route('/delete_selected_beats', methods=['GET'])
def delete_selected_beats():
        selected_district_ids = request.args.get('beats_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM beat WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('beat')) 

#Now for Wing
def get_wings():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM wing")  # Corrected table name
    wings = mycursor.fetchall()
    mycursor.close()
    return wings

@app.route('/wing')
def wing():
    wings = get_wings()
    return render_template('wing.html', wings=wings)

@app.route('/add6', methods=['POST'])
def add_wing():
    wing_name = request.form['wing']
    division_id= request.form['id']
    mycursor = mydb.cursor()
    query = "INSERT INTO wing (id,Wing) VALUES (%s,%s)"  # Corrected table name
    values = (division_id,wing_name,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('wing'))

@app.route('/edit_wing/<int:wing_id>', methods=['GET', 'POST'])
def edit_wing(wing_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM wing WHERE id = %s"  # Corrected table name
        values = (wing_id,)
        mycursor.execute(query, values)
        wing = mycursor.fetchone()
        mycursor.close()
        return render_template('wing_edit.html', wing=wing)  # Updated template name
    elif request.method == 'POST':
        new_name = request.form['new_name']
        new_name1=request.form['new_name1']
        mycursor = mydb.cursor()
        query = "UPDATE wing SET Wing = %s, id=%s WHERE id = %s"  # Corrected table name
        values = (new_name,new_name1, wing_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('wing'))

@app.route('/delete_wing/<int:wing_id>', methods=['POST'])
def delete_wing(wing_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM wing WHERE id = %s"  # Corrected table name
    values = (wing_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('wing'))

@app.route('/search_wing', methods=['POST'])
def search_wing():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM wing WHERE Wing LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    wings = mycursor.fetchall()
    mycursor.close()
    return render_template('wing.html', wings=wings)

@app.route('/add_page6')
def add_page6():
    return render_template('wing_addblock.html')


@app.route('/edit_selected_wings', methods=['GET', 'POST'])
def edit_selected_wings():
    if request.method == 'GET':
        selected_division_ids = request.args.get('wings_ids').split(',')

        # Perform the editing for each selected division
        wings = []
        for division_id in selected_division_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM wing WHERE id = %s"
            values = (division_id,)
            mycursor.execute(query, values)
            division = mycursor.fetchone()
            mycursor.close()
            if division:
                wings.append(division)

        return render_template('edit_wings.html', wings=wings)

    elif request.method == 'POST':
         # Retrieve the new division names from the form
        new_names = {}
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                division_id = key.split('_')[2]  # Extract the division ID from the key
                new_names[division_id] = value

        # Perform the editing for each selected division
        for division_id, new_name in new_names.items():
            # Perform the necessary update operations for the division
            mycursor = mydb.cursor()
            query = "UPDATE wing SET Wing = %s WHERE id = %s"
            values = (new_name, division_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

        return redirect(url_for('wing'))


@app.route('/delete_selected_wings', methods=['GET'])
def delete_selected_wings():
        selected_division_ids = request.args.get('wings_ids').split(',')

        # Perform the editing for each selected division
        for division_id in selected_division_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM wing WHERE id = %s"
            values = (division_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('wing')) 


# now for Land
def get_lands():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM land")  # Corrected table name
    lands = mycursor.fetchall()
    mycursor.close()
    return lands

@app.route('/land')
def land():
    lands = get_lands()
    return render_template('land.html', lands=lands)

@app.route('/add7', methods=['POST'])
def add_land():
    division_name=request.form['landc']
    district_name = request.form['landd']
    division_id= request.form['id']
    mycursor = mydb.cursor()
    query = "INSERT INTO land (id,Landc,Landd) VALUES (%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('land'))

@app.route('/edit_land/<int:land_id>', methods=['GET', 'POST'])
def edit_land(land_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM land WHERE id = %s"  # Corrected table name
        values = (land_id,)
        mycursor.execute(query, values)
        land = mycursor.fetchone()
        mycursor.close()
        return render_template('land_edit.html', land=land)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        mycursor = mydb.cursor()
        query = "UPDATE land SET Landc = %s, id=%s, Landd=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3, land_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('land'))

@app.route('/delete_land/<int:land_id>', methods=['POST'])
def delete_land(land_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM land WHERE id = %s"  # Corrected table name
    values = (land_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('land'))

@app.route('/search_land', methods=['POST'])
def search_land():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM land WHERE Landc LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    lands = mycursor.fetchall()
    mycursor.close()
    return render_template('land.html', lands=lands)

@app.route('/add_page7')
def add_page7():
    return render_template('land_addblock.html')


@app.route('/edit_selected_lands', methods=['GET', 'POST'])
def edit_selected_lands():
    if request.method == 'GET':
        selected_district_ids = request.args.get('lands_ids').split(',')

        # Perform the editing for each selected division
        lands = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM land WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            district = mycursor.fetchone()
            mycursor.close()
            if district:
                lands.append(district)

        return render_template('edit_lands.html', lands=lands)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_districts = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                district_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{district_id}')
                updated_districts.append((district_id, division_name, district_name))

        # Perform the editing for each selected district
        for district in updated_districts:
            district_id, division_name, district_name = district
            mycursor = mydb.cursor()
            query = "UPDATE land SET Landc = %s, Landd = %s WHERE id = %s"
            values = (division_name, district_name, district_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('land'))


@app.route('/delete_selected_lands', methods=['GET'])
def delete_selected_lands():
        selected_district_ids = request.args.get('lands_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM land WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('land')) 

#Now for Units
def get_units():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM unit")  # Corrected table name
    units = mycursor.fetchall()
    mycursor.close()
    return units

@app.route('/unit')
def unit():
    units = get_units()
    return render_template('unit.html', units=units)

@app.route('/add8', methods=['POST'])
def add_unit():
    division_name=request.form['unit']
    district_name = request.form['short']
    division_id= request.form['id']
    mycursor = mydb.cursor()
    query = "INSERT INTO unit (id,Unit,Short) VALUES (%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('unit'))

@app.route('/edit_unit/<int:unit_id>', methods=['GET', 'POST'])
def edit_unit(unit_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM unit WHERE id = %s"  # Corrected table name
        values = (unit_id,)
        mycursor.execute(query, values)
        unit = mycursor.fetchone()
        mycursor.close()
        return render_template('unit_edit.html', unit=unit)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        mycursor = mydb.cursor()
        query = "UPDATE unit SET Unit = %s, id=%s, Short=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3, unit_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('unit'))

@app.route('/delete_unit/<int:unit_id>', methods=['POST'])
def delete_unit(unit_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM unit WHERE id = %s"  # Corrected table name
    values = (unit_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('unit'))

@app.route('/search_unit', methods=['POST'])
def search_unit():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM unit WHERE Unit LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    units = mycursor.fetchall()
    mycursor.close()
    return render_template('unit.html', units=units)

@app.route('/add_page8')
def add_page8():
    return render_template('unit_addblock.html')


@app.route('/edit_selected_units', methods=['GET', 'POST'])
def edit_selected_units():
    if request.method == 'GET':
        selected_district_ids = request.args.get('units_ids').split(',')

        # Perform the editing for each selected division
        units = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM unit WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            district = mycursor.fetchone()
            mycursor.close()
            if district:
                units.append(district)

        return render_template('edit_units.html', units=units)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_districts = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                district_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{district_id}')
                updated_districts.append((district_id, division_name, district_name))

        # Perform the editing for each selected district
        for district in updated_districts:
            district_id, division_name, district_name = district
            mycursor = mydb.cursor()
            query = "UPDATE unit SET Unit = %s, Short = %s WHERE id = %s"
            values = (division_name, district_name, district_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('unit'))


@app.route('/delete_selected_units', methods=['GET'])
def delete_selected_units():
        selected_district_ids = request.args.get('units_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM unit WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('unit'))

#now for Plants

def get_plants():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM plant")  # Corrected table name
    plants = mycursor.fetchall()
    mycursor.close()
    return plants

@app.route('/plant')
def plant():
    plants = get_plants()
    return render_template('plant.html', plants=plants)

@app.route('/add9', methods=['POST'])
def add_plant():
    division_name=request.form['plant']
    district_name = request.form['species']
    division_id= request.form['id']
    mycursor = mydb.cursor()
    query = "INSERT INTO plant (id,Plant,Species) VALUES (%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('plant'))

@app.route('/edit_plant/<int:plant_id>', methods=['GET', 'POST'])
def edit_plant(plant_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM plant WHERE id = %s"  # Corrected table name
        values = (plant_id,)
        mycursor.execute(query, values)
        plant = mycursor.fetchone()
        mycursor.close()
        return render_template('plant_edit.html', plant=plant)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        mycursor = mydb.cursor()
        query = "UPDATE plant SET Plant = %s, id=%s, Species=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3, plant_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('plant'))

@app.route('/delete_plant/<int:plant_id>', methods=['POST'])
def delete_plant(plant_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM plant WHERE id = %s"  # Corrected table name
    values = (plant_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('plant'))

@app.route('/search_plant', methods=['POST'])
def search_plant():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM plant WHERE Plant LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    plants = mycursor.fetchall()
    mycursor.close()
    return render_template('plant.html', plants=plants)

@app.route('/add_page9')
def add_page9():
    return render_template('plant_addblock.html')


@app.route('/edit_selected_plants', methods=['GET', 'POST'])
def edit_selected_plants():
    if request.method == 'GET':
        selected_district_ids = request.args.get('plants_ids').split(',')

        # Perform the editing for each selected division
        plants = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM plant WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            district = mycursor.fetchone()
            mycursor.close()
            if district:
                plants.append(district)

        return render_template('edit_plants.html', plants=plants)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_districts = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                district_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{district_id}')
                updated_districts.append((district_id, division_name, district_name))

        # Perform the editing for each selected district
        for district in updated_districts:
            district_id, division_name, district_name = district
            mycursor = mydb.cursor()
            query = "UPDATE plant SET Plant = %s, Species = %s WHERE id = %s"
            values = (division_name, district_name, district_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('plant'))


@app.route('/delete_selected_plants', methods=['GET'])
def delete_selected_plants():
        selected_district_ids = request.args.get('plants_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM plant WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('plant'))

#Now for Species
def get_specieses():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM species")  # Corrected table name
    specieses = mycursor.fetchall()
    mycursor.close()
    return specieses

@app.route('/species')
def species():
    specieses = get_specieses()
    return render_template('species.html', specieses=specieses)

@app.route('/add10', methods=['POST'])
def add_species():
    division_name=request.form['species']
    district_name = request.form['scientific']
    division_id= request.form['id']
    mycursor = mydb.cursor()
    query = "INSERT INTO species (id,Species,Scientific) VALUES (%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('species'))

@app.route('/edit_species/<int:species_id>', methods=['GET', 'POST'])
def edit_species(species_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM species WHERE id = %s"  # Corrected table name
        values = (species_id,)
        mycursor.execute(query, values)
        species = mycursor.fetchone()
        mycursor.close()
        return render_template('species_edit.html', species=species)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        mycursor = mydb.cursor()
        query = "UPDATE species SET Species = %s, id=%s, Scientific=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3, species_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('species'))

@app.route('/delete_species/<int:species_id>', methods=['POST'])
def delete_species(species_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM species WHERE id = %s"  # Corrected table name
    values = (species_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('species'))

@app.route('/search_species', methods=['POST'])
def search_species():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM species WHERE Species LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    specieses = mycursor.fetchall()
    mycursor.close()
    return render_template('species.html', specieses=specieses)

@app.route('/add_page10')
def add_page10():
    return render_template('species_addblock.html')


@app.route('/edit_selected_specieses', methods=['GET', 'POST'])
def edit_selected_specieses():
    if request.method == 'GET':
        selected_district_ids = request.args.get('specieses_ids').split(',')

        # Perform the editing for each selected division
        specieses = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM species WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            district = mycursor.fetchone()
            mycursor.close()
            if district:
                specieses.append(district)

        return render_template('edit_specieses.html', specieses=specieses)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_districts = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                district_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{district_id}')
                updated_districts.append((district_id, division_name, district_name))

        # Perform the editing for each selected district
        for district in updated_districts:
            district_id, division_name, district_name = district
            mycursor = mydb.cursor()
            query = "UPDATE species SET Species = %s, Scientific = %s WHERE id = %s"
            values = (division_name, district_name, district_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('species'))


@app.route('/delete_selected_specieses', methods=['GET'])
def delete_selected_specieses():
        selected_district_ids = request.args.get('specieses_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM species WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('species'))

#Now for Scheme
def get_schemes():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM scheme")  # Corrected table name
    schemes = mycursor.fetchall()
    mycursor.close()
    return schemes

@app.route('/scheme')
def scheme():
    schemes = get_schemes()
    return render_template('scheme.html', schemes=schemes)

@app.route('/add11', methods=['POST'])
def add_scheme():
    division_name=request.form['schemen']
    district_name = request.form['schemed']
    division_id= request.form['id']
    mycursor = mydb.cursor()
    query = "INSERT INTO scheme (id,Schemen,Schemed) VALUES (%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('scheme'))

@app.route('/edit_scheme/<int:scheme_id>', methods=['GET', 'POST'])
def edit_scheme(scheme_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM scheme WHERE id = %s"  # Corrected table name
        values = (scheme_id,)
        mycursor.execute(query, values)
        scheme = mycursor.fetchone()
        mycursor.close()
        return render_template('scheme_edit.html', scheme=scheme)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        mycursor = mydb.cursor()
        query = "UPDATE scheme SET Schemen = %s, id=%s, Schemed=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3, scheme_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('scheme'))

@app.route('/delete_scheme/<int:scheme_id>', methods=['POST'])
def delete_scheme(scheme_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM scheme WHERE id = %s"  # Corrected table name
    values = (scheme_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('scheme'))

@app.route('/search_scheme', methods=['POST'])
def search_scheme():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM scheme WHERE Schemen LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    schemes = mycursor.fetchall()
    mycursor.close()
    return render_template('scheme.html', schemes=schemes)

@app.route('/add_page11')
def add_page11():
    return render_template('scheme_addblock.html')


@app.route('/edit_selected_schemes', methods=['GET', 'POST'])
def edit_selected_schemes():
    if request.method == 'GET':
        selected_district_ids = request.args.get('schemes_ids').split(',')

        # Perform the editing for each selected division
        schemes = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM scheme WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            district = mycursor.fetchone()
            mycursor.close()
            if district:
                schemes.append(district)

        return render_template('edit_schemes.html', schemes=schemes)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_districts = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                district_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{district_id}')
                updated_districts.append((district_id, division_name, district_name))

        # Perform the editing for each selected district
        for district in updated_districts:
            district_id, division_name, district_name = district
            mycursor = mydb.cursor()
            query = "UPDATE scheme SET Schemen = %s, Schemed = %s WHERE id = %s"
            values = (division_name, district_name, district_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('scheme'))


@app.route('/delete_selected_schemes', methods=['GET'])
def delete_selected_schemes():
        selected_district_ids = request.args.get('schemes_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM scheme WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('scheme'))

#Now for Site Name
def get_sites():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sitename")  # Corrected table name
    sites = mycursor.fetchall()
    mycursor.close()
    return sites

@app.route('/site')
def site():
    sites = get_sites()
    return render_template('site.html', sites=sites)

@app.route('/add12', methods=['POST'])
def add_site():
    division_name=request.form['division']
    district_name = request.form['district']
    division_id= request.form['id']
    site_name=request.form['site']
    mycursor = mydb.cursor()
    query = "INSERT INTO sitename (id,Division,District,Sitename) VALUES (%s,%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name,site_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('site'))

@app.route('/edit_site/<int:site_id>', methods=['GET', 'POST'])
def edit_site(site_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM sitename WHERE id = %s"  # Corrected table name
        values = (site_id,)
        mycursor.execute(query, values)
        site = mycursor.fetchone()
        mycursor.close()
        return render_template('site_edit.html', site=site)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        new_name4 = request.form['new_name4']
        mycursor = mydb.cursor()
        query = "UPDATE sitename SET Division = %s, id=%s, District=%s, Sitename=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3,new_name4, site_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('site'))

@app.route('/delete_site/<int:site_id>', methods=['POST'])
def delete_site(site_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM sitename WHERE id = %s"  # Corrected table name
    values = (site_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('site'))

@app.route('/search_site', methods=['POST'])
def search_site():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM sitename WHERE Sitename LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    sites = mycursor.fetchall()
    mycursor.close()
    return render_template('site.html', sites=sites)

@app.route('/add_page12')
def add_page12():
    return render_template('site_addblock.html')


@app.route('/edit_selected_sites', methods=['GET', 'POST'])
def edit_selected_sites():
    if request.method == 'GET':
        selected_district_ids = request.args.get('sites_ids').split(',')

        # Perform the editing for each selected division
        sites = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM sitename WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            block = mycursor.fetchone()
            mycursor.close()
            if block:
                sites.append(block)

        return render_template('edit_sites.html', sites=sites)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_ranges = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                range_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{range_id}')
                range_name = request.form.get(f'new_name2_{range_id}')
                updated_ranges.append((range_id, division_name, district_name,range_name))

        # Perform the editing for each selected district
        for block in updated_ranges:
            range_id, division_name, district_name,range_name = block
            mycursor = mydb.cursor()
            query = "UPDATE sitename SET Division = %s, District = %s, Sitename = %s WHERE id = %s"
            values = (division_name, district_name,range_name, range_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('site'))


@app.route('/delete_selected_sites', methods=['GET'])
def delete_selected_sites():
        selected_district_ids = request.args.get('sites_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM sitename WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('site')) 

#Now for Khsra Number
def get_khasras():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM khasra")  # Corrected table name
    khasras = mycursor.fetchall()
    mycursor.close()
    return khasras

@app.route('/khasra')
def khasra():
    khasras = get_khasras()
    return render_template('khasra.html', khasras=khasras)

@app.route('/add13', methods=['POST'])
def add_khasra():
    division_name=request.form['division']
    district_name = request.form['district']
    division_id= request.form['id']
    khasra_name=request.form['khasra']
    mycursor = mydb.cursor()
    query = "INSERT INTO khasra (id,Division,District,Khasra) VALUES (%s,%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name,khasra_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('khasra'))

@app.route('/edit_khasra/<int:khasra_id>', methods=['GET', 'POST'])
def edit_khasra(khasra_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM khasra WHERE id = %s"  # Corrected table name
        values = (khasra_id,)
        mycursor.execute(query, values)
        khasra = mycursor.fetchone()
        mycursor.close()
        return render_template('khasra_edit.html', khasra=khasra)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        new_name4 = request.form['new_name4']
        mycursor = mydb.cursor()
        query = "UPDATE khasra SET Division = %s, id=%s, District=%s, Khkhasra=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3,new_name4, khasra_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('khasra'))

@app.route('/delete_khasra/<int:khasra_id>', methods=['POST'])
def delete_khasra(khasra_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM khasra WHERE id = %s"  # Corrected table name
    values = (khasra_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('khasra'))

@app.route('/search_khasra', methods=['POST'])
def search_khasra():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM khasra WHERE Khasra LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    khasras = mycursor.fetchall()
    mycursor.close()
    return render_template('khasra.html', khasras=khasras)

@app.route('/add_page13')
def add_page13():
    return render_template('khasra_addblock.html')


@app.route('/edit_selected_khasras', methods=['GET', 'POST'])
def edit_selected_khasras():
    if request.method == 'GET':
        selected_district_ids = request.args.get('khasras_ids').split(',')

        # Perform the editing for each selected division
        khasras = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM khasra WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            block = mycursor.fetchone()
            mycursor.close()
            if block:
                khasras.append(block)

        return render_template('edit_khasras.html', khasras=khasras)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_ranges = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                range_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{range_id}')
                range_name = request.form.get(f'new_name2_{range_id}')
                updated_ranges.append((range_id, division_name, district_name,range_name))

        # Perform the editing for each selected district
        for block in updated_ranges:
            range_id, division_name, district_name,range_name = block
            mycursor = mydb.cursor()
            query = "UPDATE khasra SET Division = %s, District = %s, Khasra = %s WHERE id = %s"
            values = (division_name, district_name,range_name, range_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('khasra'))


@app.route('/delete_selected_khasras', methods=['GET'])
def delete_selected_khasras():
        selected_district_ids = request.args.get('khasras_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM khasra WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('khasra')) 

#No of Plant
def get_nplants():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM noofplant")  # Corrected tabnplant
    nplants = mycursor.fetchall()
    mycursor.close()
    return nplants

@app.route('/nplant')
def nplant():
    nplants = get_nplants()
    return render_template('nplant.html', nplants=nplants)

@app.route('/add14', methods=['POST'])
def add_nplant():
    division_name=request.form['plant']
    district_name = request.form['nplant']
    division_id= request.form['id']
    mycursor = mydb.cursor()
    query = "INSERT INTO noofplant (id,Plantname,Noofplant) VALUES (%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('nplant'))

@app.route('/edit_nplant/<int:nplant_id>', methods=['GET', 'POST'])
def edit_nplant(nplant_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM noofplant WHERE id = %s"  # Corrected table name
        values = (nplant_id,)
        mycursor.execute(query, values)
        nplant = mycursor.fetchone()
        mycursor.close()
        return render_template('nplant_edit.html', nplant=nplant)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        mycursor = mydb.cursor()
        query = "UPDATE noofplant SET Plantname = %s, id=%s, Noofplant=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3, nplant_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('nplant'))

@app.route('/delete_nplant/<int:nplant_id>', methods=['POST'])
def delete_nplant(nplant_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM noofplant WHERE id = %s"  # Corrected table name
    values = (nplant_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('nplant'))

@app.route('/search_nplant', methods=['POST'])
def search_nplant():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM noofplant WHERE Noofplant LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    nplants = mycursor.fetchall()
    mycursor.close()
    return render_template('nplant.html', nplants=nplants)

@app.route('/add_page14')
def add_page14():
    return render_template('nplant_addblock.html')


@app.route('/edit_selected_nplants', methods=['GET', 'POST'])
def edit_selected_nplants():
    if request.method == 'GET':
        selected_district_ids = request.args.get('nplants_ids').split(',')

        # Perform the editing for each selected division
        nplants = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM noofplant WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            district = mycursor.fetchone()
            mycursor.close()
            if district:
                nplants.append(district)

        return render_template('edit_nplants.html', nplants=nplants)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_districts = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                district_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{district_id}')
                updated_districts.append((district_id, division_name, district_name))

        # Perform the editing for each selected district
        for district in updated_districts:
            district_id, division_name, district_name = district
            mycursor = mydb.cursor()
            query = "UPDATE noofplant SET Plantname = %s, Noofplant = %s WHERE id = %s"
            values = (division_name, district_name, district_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('nplant'))


@app.route('/delete_selected_nplants', methods=['GET'])
def delete_selected_nplants():
        selected_district_ids = request.args.get('nplants_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM noofplant WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('nplant'))

#Now for Lattitude
def get_latitudes():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM latitude")  # Corrected table name
    latitudes = mycursor.fetchall()
    mycursor.close()
    return latitudes

@app.route('/latitude')
def latitude():
    latitudes = get_latitudes()
    return render_template('latitude.html', latitudes=latitudes)

@app.route('/add15', methods=['POST'])
def add_latitude():
    division_name=request.form['site']
    district_name = request.form['latitude']
    division_id= request.form['id']
    mycursor = mydb.cursor()
    query = "INSERT INTO latitude (id,Sitename,Latitude) VALUES (%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('latitude'))

@app.route('/edit_latitude/<int:latitude_id>', methods=['GET', 'POST'])
def edit_latitude(latitude_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM latitude WHERE id = %s"  # Corrected table name
        values = (latitude_id,)
        mycursor.execute(query, values)
        latitude = mycursor.fetchone()
        mycursor.close()
        return render_template('latitude_edit.html', latitude=latitude)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        mycursor = mydb.cursor()
        query = "UPDATE latitude SET Sitename = %s, id=%s, Latitude=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3, latitude_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('latitude'))

@app.route('/delete_latitude/<int:latitude_id>', methods=['POST'])
def delete_latitude(latitude_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM latitude WHERE id = %s"  # Corrected table name
    values = (latitude_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('latitude'))

@app.route('/search_latitude', methods=['POST'])
def search_latitude():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM latitude WHERE Latitude LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    latitudes = mycursor.fetchall()
    mycursor.close()
    return render_template('latitude.html', latitudes=latitudes)

@app.route('/add_page15')
def add_page15():
    return render_template('latitude_addblock.html')


@app.route('/edit_selected_latitudes', methods=['GET', 'POST'])
def edit_selected_latitudes():
    if request.method == 'GET':
        selected_district_ids = request.args.get('latitudes_ids').split(',')

        # Perform the editing for each selected division
        latitudes = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM latitude WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            district = mycursor.fetchone()
            mycursor.close()
            if district:
                latitudes.append(district)

        return render_template('edit_latitudes.html', latitudes=latitudes)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_districts = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                district_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{district_id}')
                updated_districts.append((district_id, division_name, district_name))

        # Perform the editing for each selected district
        for district in updated_districts:
            district_id, division_name, district_name = district
            mycursor = mydb.cursor()
            query = "UPDATE latitude SET Sitename = %s, Latitude = %s WHERE id = %s"
            values = (division_name, district_name, district_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('latitude'))


@app.route('/delete_selected_latitudes', methods=['GET'])
def delete_selected_latitudes():
        selected_district_ids = request.args.get('latitudes_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM latitude WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('latitude'))
#Now for Longitude
def get_longitudes():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM longitude")  # Corrected table name
    longitudes = mycursor.fetchall()
    mycursor.close()
    return longitudes

@app.route('/longitude')
def longitude():
    longitudes = get_longitudes()
    return render_template('longitude.html', longitudes=longitudes)

@app.route('/add16', methods=['POST'])
def add_longitude():
    division_name=request.form['site']
    district_name = request.form['longitude']
    division_id= request.form['id']
    mycursor = mydb.cursor()
    query = "INSERT INTO longitude (id,Sitename,Longitude) VALUES (%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('longitude'))

@app.route('/edit_longitude/<int:longitude_id>', methods=['GET', 'POST'])
def edit_longitude(longitude_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM longitude WHERE id = %s"  # Corrected table name
        values = (longitude_id,)
        mycursor.execute(query, values)
        longitude = mycursor.fetchone()
        mycursor.close()
        return render_template('longitude_edit.html', longitude=longitude)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        mycursor = mydb.cursor()
        query = "UPDATE longitude SET Sitename = %s, id=%s, Longitude=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3, longitude_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('longitude'))

@app.route('/delete_longitude/<int:longitude_id>', methods=['POST'])
def delete_longitude(longitude_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM longitude WHERE id = %s"  # Corrected table name
    values = (longitude_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('longitude'))

@app.route('/search_longitude', methods=['POST'])
def search_longitude():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM longitude WHERE Longitude LIKE %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    longitudes = mycursor.fetchall()
    mycursor.close()
    return render_template('longitude.html', longitudes=longitudes)

@app.route('/add_page16')
def add_page16():
    return render_template('longitude_addblock.html')


@app.route('/edit_selected_longitudes', methods=['GET', 'POST'])
def edit_selected_longitudes():
    if request.method == 'GET':
        selected_district_ids = request.args.get('longitudes_ids').split(',')

        # Perform the editing for each selected division
        longitudes = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM longitude WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            district = mycursor.fetchone()
            mycursor.close()
            if district:
                longitudes.append(district)

        return render_template('edit_longitudes.html', longitudes=longitudes)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_districts = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                district_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{district_id}')
                updated_districts.append((district_id, division_name, district_name))

        # Perform the editing for each selected district
        for district in updated_districts:
            district_id, division_name, district_name = district
            mycursor = mydb.cursor()
            query = "UPDATE longitude SET Sitename = %s, Longitude = %s WHERE id = %s"
            values = (division_name, district_name, district_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('longitude'))


@app.route('/delete_selected_longitudes', methods=['GET'])
def delete_selected_longitudes():
        selected_district_ids = request.args.get('longitudes_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM longitude WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('longitude'))

#Now  for Spaceing
def get_spaceings():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM spaceing")  # Corrected table name
    spaceings = mycursor.fetchall()
    mycursor.close()
    return spaceings

@app.route('/spaceing')
def spaceing():
    spaceings = get_spaceings()
    return render_template('spaceing.html', spaceings=spaceings)

@app.route('/add17', methods=['POST'])
def add_spaceing():
    division_name=request.form['plant']
    district_name = request.form['spaceing']
    division_id= request.form['id']
    mycursor = mydb.cursor()
    query = "INSERT INTO spaceing (id,Plantname,Spaceing) VALUES (%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('spaceing'))

@app.route('/edit_spaceing/<int:spaceing_id>', methods=['GET', 'POST'])
def edit_spaceing(spaceing_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM spaceing WHERE id = %s"  # Corrected table name
        values = (spaceing_id,)
        mycursor.execute(query, values)
        spaceing = mycursor.fetchone()
        mycursor.close()
        return render_template('spaceing_edit.html', spaceing=spaceing)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        mycursor = mydb.cursor()
        query = "UPDATE spaceing SET Plantname = %s, id=%s, Spaceing=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3, spaceing_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('spaceing'))

@app.route('/delete_spaceing/<int:spaceing_id>', methods=['POST'])
def delete_spaceing(spaceing_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM spaceing WHERE id = %s"  # Corrected table name
    values = (spaceing_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('spaceing'))

@app.route('/search_spaceing', methods=['POST'])
def search_spaceing():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM spaceing WHERE Spaceing Like %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    spaceings = mycursor.fetchall()
    mycursor.close()
    return render_template('spaceing.html', spaceings=spaceings)

@app.route('/add_page17')
def add_page17():
    return render_template('spaceing_addblock.html')


@app.route('/edit_selected_spaceings', methods=['GET', 'POST'])
def edit_selected_spaceings():
    if request.method == 'GET':
        selected_district_ids = request.args.get('spaceings_ids').split(',')

        # Perform the editing for each selected division
        spaceings = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM spaceing WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            district = mycursor.fetchone()
            mycursor.close()
            if district:
                spaceings.append(district)

        return render_template('edit_spaceings.html', spaceings=spaceings)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_districts = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                district_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{district_id}')
                updated_districts.append((district_id, division_name, district_name))

        # Perform the editing for each selected district
        for district in updated_districts:
            district_id, division_name, district_name = district
            mycursor = mydb.cursor()
            query = "UPDATE spaceing SET Plantname = %s, Spaceing = %s WHERE id = %s"
            values = (division_name, district_name, district_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('spaceing'))


@app.route('/delete_selected_spaceings', methods=['GET'])
def delete_selected_spaceings():
        selected_district_ids = request.args.get('spaceings_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM spaceing WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('spaceing'))

#now for Value
def get_values():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM value")  # Corrected table name
    values = mycursor.fetchall()
    mycursor.close()
    return values

@app.route('/value')
def value():
    values = get_values()
    return render_template('value.html', values=values)

@app.route('/add18', methods=['POST'])
def add_value():
    division_name=request.form['plant']
    district_name = request.form['value']
    division_id= request.form['id']
    mycursor = mydb.cursor()
    query = "INSERT INTO value (id,Plantname,Value) VALUES (%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('value'))

@app.route('/edit_value/<int:value_id>', methods=['GET', 'POST'])
def edit_value(value_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM value WHERE id = %s"  # Corrected table name
        values = (value_id,)
        mycursor.execute(query, values)
        value = mycursor.fetchone()
        mycursor.close()
        return render_template('value_edit.html', value=value)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        mycursor = mydb.cursor()
        query = "UPDATE spaceing SET Plantname = %s, id=%s, Value=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3, value_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('value'))

@app.route('/delete_value/<int:value_id>', methods=['POST'])
def delete_value(value_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM value WHERE id = %s"  # Corrected table name
    values = (value_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('value'))

@app.route('/search_value', methods=['POST'])
def search_value():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM value WHERE Value Like %s"  # Corrected table name
    valuesd = ('%' + search_value + '%',)
    mycursor.execute(query, valuesd)
    values = mycursor.fetchall()
    mycursor.close()
    return render_template('value.html', values=values)

@app.route('/add_page18')
def add_page18():
    return render_template('value_addblock.html')


@app.route('/edit_selected_values', methods=['GET', 'POST'])
def edit_selected_values():
    if request.method == 'GET':
        selected_district_ids = request.args.get('values_ids').split(',')

        # Perform the editing for each selected division
        values = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM value WHERE id = %s"
            valuesd = (district_id,)
            mycursor.execute(query, valuesd)
            district = mycursor.fetchone()
            mycursor.close()
            if district:
                values.append(district)

        return render_template('edit_values.html', values=values)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_districts = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                district_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{district_id}')
                updated_districts.append((district_id, division_name, district_name))

        # Perform the editing for each selected district
        for district in updated_districts:
            district_id, division_name, district_name = district
            mycursor = mydb.cursor()
            query = "UPDATE value SET Plantname = %s, Value = %s WHERE id = %s"
            valuesd = (division_name, district_name, district_id)
            mycursor.execute(query, valuesd)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('value'))


@app.route('/delete_selected_values', methods=['GET'])
def delete_selected_values():
        selected_district_ids = request.args.get('values_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM value WHERE id = %s"
            valuesd = (district_id,)
            mycursor.execute(query, valuesd)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('value'))

#Now for Plantation Date
def get_plantationdates():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM plantationdate")  # Corrected table name
    plantationdates = mycursor.fetchall()
    mycursor.close()
    return plantationdates

@app.route('/plantationdate')
def plantationdate():
    plantationdates = get_plantationdates()
    return render_template('plantationdate.html', plantationdates=plantationdates)

@app.route('/add19', methods=['POST'])
def add_plantationdate():
    division_name=request.form['plant']
    district_name = request.form['plantationdate']
    division_id= request.form['id']
    mycursor = mydb.cursor()
    query = "INSERT INTO plantationdate (id,Plantname,Plantationdate) VALUES (%s,%s,%s)"  # Corrected table name
    values = (division_id,division_name,district_name)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('plantationdate'))

@app.route('/edit_plantationdate/<int:plantationdate_id>', methods=['GET', 'POST'])
def edit_plantationdate(plantationdate_id):
    if request.method == 'GET':
        mycursor = mydb.cursor()
        query = "SELECT * FROM plantationdate WHERE id = %s"  # Corrected table name
        values = (plantationdate_id,)
        mycursor.execute(query, values)
        plantationdate = mycursor.fetchone()
        mycursor.close()
        return render_template('plantationdate_edit.html', plantationdate=plantationdate)  # Updated template name
    elif request.method == 'POST':
        new_name2 = request.form['new_name2']
        new_name1=request.form['new_name1']
        new_name3 = request.form['new_name3']
        mycursor = mydb.cursor()
        query = "UPDATE plantationdate SET Plantname = %s, id=%s, Plantationdate=%s WHERE id = %s"  # Corrected table name
        values = (new_name2,new_name1,new_name3, plantationdate_id)
        mycursor.execute(query, values)
        mydb.commit()
        mycursor.close()
        return redirect(url_for('plantationdate'))

@app.route('/delete_plantationdate/<int:plantationdate_id>', methods=['POST'])
def delete_plantationdate(plantationdate_id):
    mycursor = mydb.cursor()
    query = "DELETE FROM plantationdate WHERE id = %s"  # Corrected table name
    values = (plantationdate_id,)
    mycursor.execute(query, values)
    mydb.commit()
    mycursor.close()
    return redirect(url_for('plantationdate'))

@app.route('/search_plantationdate', methods=['POST'])
def search_plantationdate():
    search_value = request.form['search']
    mycursor = mydb.cursor()
    query = "SELECT * FROM plantationdate WHERE Plantationdate Like %s"  # Corrected table name
    values = ('%' + search_value + '%',)
    mycursor.execute(query, values)
    plantationdates = mycursor.fetchall()
    mycursor.close()
    return render_template('plantationdate.html', plantationdates=plantationdates)

@app.route('/add_page19')
def add_page19():
    return render_template('plantationdate_addblock.html')


@app.route('/edit_selected_plantationdates', methods=['GET', 'POST'])
def edit_selected_plantationdates():
    if request.method == 'GET':
        selected_district_ids = request.args.get('plantationdates_ids').split(',')

        # Perform the editing for each selected division
        plantationdates = []
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "SELECT * FROM plantationdate WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            district = mycursor.fetchone()
            mycursor.close()
            if district:
                plantationdates.append(district)

        return render_template('edit_plantationdates.html', plantationdates=plantationdates)

    elif request.method == 'POST':
        # Retrieve the new division and district names from the form
        updated_districts = []
        for key, value in request.form.items():
            if key.startswith('new_name_'):
                district_id = key.split('_')[2]
                division_name = value
                district_name = request.form.get(f'new_name1_{district_id}')
                updated_districts.append((district_id, division_name, district_name))

        # Perform the editing for each selected district
        for district in updated_districts:
            district_id, division_name, district_name = district
            mycursor = mydb.cursor()
            query = "UPDATE spaceing SET Plantname = %s, Plantationdate = %s WHERE id = %s"
            values = (division_name, district_name, district_id)
            mycursor.execute(query, values)
            mydb.commit()
            mycursor.close()

    return redirect(url_for('plantationdate'))


@app.route('/delete_selected_plantationdates', methods=['GET'])
def delete_selected_plantationdates():
        selected_district_ids = request.args.get('plantationdates_ids').split(',')

        # Perform the editing for each selected division
        for district_id in selected_district_ids:
            mycursor = mydb.cursor()
            query = "DELETE FROM plantationdate WHERE id = %s"
            values = (district_id,)
            mycursor.execute(query, values)
            mycursor.close()
            mydb.commit()

        return redirect(url_for('plantationdate'))


@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/form_details',  methods=['POST','GET'])
def form_details():
    if request.method == 'POST':
        msg=""
        division = "Ambala"
        district = "Sonipat"
        range_value = "Sonipat"
        block = "Sonipat"
        beat = "Jagdishpur"
        village="Bara Gaon"
        wing = "Territorial"
        land_category = ""
        land = ""
        scheme = ""
        plantationmonth=""
        unit = 0
        value = 0
        spaceing = ""
        sitename = ""
        khasraNo = ""
        latitude = ""
        longitude = ""
        plantcategory = ""
        species = request.form['species']
        noofplant = 0
        if request.form.get('user1'):
            mycursor.execute('INSERT INTO user1_form (Division, District, `Range`, Block, Beat, Village, Wing, LandCategory, Land, Scheme, PlantationMonth, Unit, Value, Spaceing, Sitename, KhasraNo, Latitude, Longitude, PlantCategory, Species, NoofPlant ) VALUES ( %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)', (division, district, range_value, block, beat, village, wing, land_category, land, scheme, 
                                                                                                                                                                                                                                                                                                                                            plantationmonth,unit,value,spaceing,sitename,khasraNo,latitude,longitude,plantcategory,species,noofplant))
            mydb.commit()
            
            return redirect(url_for('message1'))
    
        else:
            msg="Error"
            return redirect(url_for('message1',  message=msg))
    elif request.method == 'GET':
        mycursor.execute("SELECT * FROM user1_form")

        # Fetch all the rows of the result
        rows = mycursor.fetchall()
        return render_template('form.html', rows=rows)
    
    
@app.route('/message1')
def message1():
    message = request.args.get('message', 'Submitted Successfully')
    
    if message == ' Submitted Successfully':
        success = True
    else:
        success = False
    
    return render_template('message1.html', message=message, success=success)

@app.route('/display_details',methods=[ 'GET','POST'])
def display_details():
    mycursor.execute("SELECT * FROM user1_form")
    rows = mycursor.fetchall()
    record_id = int(rows[0][0])
    
    if request.method == 'GET':
        mycursor.execute("SELECT * FROM user1_form")

        # Fetch all the rows of the result
        rows = mycursor.fetchall()
        record_id=rows[0]
        return render_template('user1.html', rows=rows)
    elif request.method == 'POST':
        
        division = request.form['field1']
        district = request.form['field2']
        range_value = request.form['field3']
        block =request.form['field4']
        beat = request.form['field5']
        village=request.form['field6']
        wing = request.form['field7']
        land_category =request.form['field8'] 
        land = request.form['field9']
        scheme = request.form['field10']
        plantationmonth=request.form['field11']
        unit = request.form['field12']
        value = request.form['field13']
        spaceing = request.form['field14']
        sitename = request.form['field15']
        khasraNo = request.form['field16']
        latitude = request.form['field17']
        longitude = request.form['field18']
        plantcategory = request.form['field19']
        species = request.form['field20']
        noofplant = request.form['field21']
        mycursor.execute('UPDATE user1_form SET Division = %s, District = %s, `Range` = %s, Block = %s, Beat = %s, Village = %s, Wing = %s, LandCategory = %s, Land = %s, Scheme = %s, PlantationMonth = %s, Unit = %s, Value = %s, Spaceing = %s, Sitename = %s, KhasraNo = %s, Latitude = %s, Longitude = %s, PlantCategory = %s, Species = %s, NoofPlant = %s WHERE id = %s',
                 (division, district, range_value, block, beat, village, wing, land_category, land, scheme,
                  plantationmonth, unit, value, spaceing, sitename, khasraNo, latitude, longitude, plantcategory, species, noofplant, record_id))
        mydb.commit()

            
        return redirect(url_for('message1'))
    
      
    

if __name__ == "__main__":
    app.run()
