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
    Employee_Name = request.form['Employee_Name']
    Pay_Per_Hour = request.form['Pay_Per_Hour']
    Total_Hour_Work = request.form['Total_Hour_Work']
    Ot_Time = request.form['Ot_Time']
    Total_Ot_Time = request.form['Total_Ot_Time']
    Total_Salary = request.form['Total_Salary']

    insert_sql = "INSERT INTO payroll VALUES (%s, %s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()
    cursor.execute(insert_sql, (Employee_Name, Pay_Per_Hour, Total_Hour_Work, Ot_Time, Total_Ot_Time, Total_Salary))
    db_conn.commit()
   
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
