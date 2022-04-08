from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('payroll.html')


@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com')


@app.route("/addpayroll", methods=['POST'])
def AddPayroll():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    pri_skill = request.form['pri_skill']
    location = request.form['location']
    emp_image_file = request.files['emp_image_file']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()
    cursor.execute(insert_sql, (emp_id, first_name, last_name, pri_skill, location))
    db_conn.commit()
    emp_name = "" + first_name + " " + last_name
    # Uplaod image file in S3 #
    
        

    print("all modification done...")
    return render_template('AddEmpOutput.html', name=emp_name)


#Show payroll#
@app.route("/diplayPayroll",methods=['POST'])
def fetchdata():
    cursor = db_conn.cursor()
    cursor.execute("SELECT Payroll_Id, Employee_Name, Pay_Per_Hour, Total_Hour_Work,Ot_Time, Total_Ot_Time, Total_Salary FROM payroll")
    i = cursor.fetchall()
    return render_template('payroll.html', data=i)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
