from app import pymysql, api
from flask import jsonify, abort, make_response, request

connection = pymysql.connect(host='0.0.0.0',
                             port=33062,
                             user='root',
                             password='root',
                             db='hernandb',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()


@api.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': "bad request"}), 400)


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': "not found"}), 404)


@api.errorhandler(500)
def internal_server_error(error):
    return make_response(jsonify({'error': "internal server error"}), 500)


@api.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    query = "SELECT * FROM tasks WHERE id = '%d'" % task_id
    cursor.execute(query)
    result = cursor.fetchone()
    if result is None:
        abort(404)
    else:
        result['done'] = bool(result['done'])
        return jsonify({'task': result})


@api.route('/tasks', methods=['GET'])
def get_tasks():
    query = "SELECT * FROM tasks"
    cursor.execute(query)
    results = cursor.fetchall()
    for result in results:
        result['done'] = bool(result['done'])
    return jsonify({'tasks': results})


@api.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or ('title' and 'description') not in request.json:
        abort(400)

    query = "INSERT INTO tasks VALUES (0, '%s','%s', FALSE)" % (
        request.json['title'], request.json.get('description', ''))
    response = cursor.execute(query)

    if response:
        connection.commit()
        return jsonify({'result': True}), 201
    else:
        connection.rollback()
        abort(500)


@api.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    vals = []

    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) is str:
        vals.append("title = '%s'" % request.json['title'])

    if 'description' in request.json and type(request.json['description']) is str:
        vals.append("description = '%s'" % request.json['description'])

    if 'done' in request.json and type(request.json['done']) is bool:
        vals.append('done = %s' % request.json['done'])

    query = ""

    for val in vals:
        query = query + val
        if val is not vals[-1]:
            query = query + ','

    query = "update tasks set " + query + " where id = %d" % task_id

    response = cursor.execute(query)
    if response:
        connection.commit()
        return jsonify({'result': True})
    else:
        connection.rollback()
        abort(404)


@api.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    query = "DELETE FROM tasks WHERE id = '%d'" % task_id
    response = cursor.execute(query)
    if response:
        connection.commit()
        return jsonify({'result': True})
    else:
        connection.rollback()
        abort(404)
