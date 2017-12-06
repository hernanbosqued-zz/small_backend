from flask import jsonify, abort, make_response, request
from app import api
import pymysql as mysql

conn = mysql.connect("localhost", "root", "ATLanta1904", "prueba")
cursor = conn.cursor()


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': "not found"}))


@api.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'error': "internal server error"}))


@api.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    query = "select * from tasks where id = %d " % task_id
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        abort(404)
    else:
        return jsonify({'task': result})


@api.route('/tasks', methods=['GET'])
def get_tasks():
    cursor.execute("select * from tasks")
    result = cursor.fetchall()
    return jsonify({'tasks': result})


@api.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or ('title' and 'description') not in request.json:
        abort(400)

    try:
        query = "insert into tasks values (0, '%s','%s', false)" % (
            request.json['title'], request.json.get('description', ''))
        cursor.execute(query)
        conn.commit()
        return jsonify({'result': True}), 201
    except:
        conn.rollback()
        abort(500)


@api.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    vals = []

    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) is not str:
        abort(400)
    else:
        vals.append("title = '%s'" % request.json['title'])
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    else:
        vals.append("description = '%s'" % request.json['description'])
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    else:
        vals.append('done = %s' % request.json['done'])

    query = ""

    for val in vals:
        query = query + val
        if val is not vals[-1]:
            query = query + ','

    query = "update tasks set " + query + " where id = %d" % task_id

    try:
        cursor.execute(query)
        conn.commit()
        return jsonify({'result': True})
    except:
        conn.rollback()
        abort(500)


@api.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        query = "delete from tasks where id = %d" % task_id
        cursor.execute(query)
        conn.commit()
        return jsonify({'result': True})
    except:
        conn.rollback()
        abort(500)
