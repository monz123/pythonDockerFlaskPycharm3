from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'employeeData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Bio Metric Statistics of Office Workers'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM employeeInfo')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, employeeDetail=result)

@app.route('/view/<int:emp_id>', methods=['GET'])
def record_view(emp_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM employeeInfo WHERE id=%s', emp_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', employeeDetail=result[0])

@app.route('/edit/<int:emp_id>', methods=['GET'])
def form_edit_get(emp_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM employeeInfo WHERE id=%s', emp_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', employeeDetail=result[0])

@app.route('/edit/<int:emp_id>', methods=['POST'])
def form_update_post(emp_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Name'), request.form.get('Age'), request.form.get('Sex'),
                 request.form.get('Weight_lbs'), request.form.get('Height_in'),
                 request.form.get('fldCapitalStatus'), request.form.get('fldPopulation'), city_id)
    sql_update_query = """UPDATE tblCitiesImport t SET t.fldName = %s, t.fldLat = %s, t.fldLong = %s, t.fldCountry = 
    %s, t.fldAbbreviation = %s, t.fldCapitalStatus = %s, t.fldPopulation = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
