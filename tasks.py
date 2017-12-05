from flask import jsonify, abort, make_response, request
from app import api
import json


def open_db():
    f = open('db.json', 'r')
    data = json.load(f)
    f.close()
    return data


def save_db(data):
    file = open('db.json', 'w')
    json.dump(data, file)
    file.close()


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@api.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    data = open_db()
    task = [item for item in data if item['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task})


@api.route('/tasks', methods=['GET'])
def get_tasks():
    data = open_db()
    return jsonify({'tasks': data})


@api.route('/tasks', methods=['POST'])
def create_task():
    data = open_db()
    if not request.json or not 'title' in request.json:
        abort(400)
    item = {
        'id': data[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    data.append(item)
    save_db(data)
    return jsonify({'task': item}), 201


@api.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = open_db()
    task = [task for task in data if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    save_db(data)
    return jsonify({'task': task[0]})


@api.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    data = open_db()
    task = [item for item in data if item['id'] == task_id]
    if len(task) == 0:
        abort(404)
    data.remove(task[0])
    save_db(data)
    return jsonify({'result': True})
