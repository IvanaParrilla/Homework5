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
app.config['MYSQL_DATABASE_DB'] = 'oscarData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Oscars Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_female')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, cities=result)


@app.route('/view/<int:city_id>', methods=['GET'])
def record_view(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_female WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', city=result[0])


@app.route('/edit/<int:city_id>', methods=['GET'])
def form_edit_get(city_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_female WHERE id=%s', city_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', city=result[0])


@app.route('/edit/<int:city_id>', methods=['POST'])
def form_update_post(city_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('year'), request.form.get('age'), request.form.get('name'),
                 request.form.get('movie'), city_id)
    sql_update_query = """UPDATE oscar_age_female t SET t.year = %s, t.age = %s, t.name = %s, t.movie = 
    %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/cities/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Oscar Award Form')


@app.route('/cities/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('id'), request.form.get('year'), request.form.get('age'),
                 request.form.get('name'), request.form.get('movie'))
    sql_insert_query = """INSERT INTO oscar_age_female (id,`year`,age,`name`,movie) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:city_id>', methods=['POST'])
def form_delete_post(city_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM oscar_age_female WHERE id = %s """
    cursor.execute(sql_delete_query, city_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/oscar', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_female')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscar/<int:city_id>', methods=['GET'])
def api_retrieve(city_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_female WHERE id=%s', city_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/oscar/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/oscar/<int:city_id>', methods=['PUT'])
def api_edit(city_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/oscar/<int:city_id>', methods=['DELETE'])
def api_delete(city_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)