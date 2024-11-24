from flask import Flask, request, jsonify
from mod.DB.work_db import Work
from flask_cors import CORS
from mod.summ import SumTask
import json

app = Flask(__name__)
CORS(app)
DB = Work()

class FlaskModule():
    def __init__(self):
        app.run(host='localhost', port=5000, debug=True)

    @app.route('/create_children', methods=['POST'])
    def create_children():
        login = request.form.get('login')
        password =  request.form.get('password')
        print(login)
        print(password)
        result = DB.create_children(login, password)
        return jsonify({"status": "success", "message": result}), 200

    @app.route('/create_parents', methods=['POST'])
    def create_parents():
        login = request.form.get('login')
        password =  request.form.get('password')
        result = DB.create_parents(login, password)
        return jsonify({"status": "success", "message": result}), 200


    @app.route('/create_teacher', methods=['POST'])
    def create_teacher():
        login = request.form.get('login')
        password =  request.form.get('password')

        result = DB.create_teacher(login, password)
        return jsonify({"status": "success", "message": result}), 200


    @app.route('/login_children', methods=['POST'])
    def login_children():
        login = request.form.get('login')
        password =  request.form.get('password')
        result = DB.login_children(login, password)
        return jsonify({"status": "success", "message": result}), 200


    @app.route('/children_by_parent', methods=['GET'])
    def children_by_parent():
        parent_login = request.args.get('parent_login')  # Получаем логин родителя из параметров запроса

        children_info = DB.get_children_by_parent_login(parent_login)  # Вызываем метод получения детей
        if isinstance(children_info, str):  # Если возвращается сообщение об ошибке
            return jsonify({"status": "error", "message": children_info}), 404

        return jsonify({"status": "success", "children": json.loads(children_info)}), 200


    @app.route('/children_by_teacher', methods=['GET'])
    def children_by_teacher():
        teacher_login = request.args.get('teacher_login')  # Получаем логин учителя из параметров запроса

        children_info = DB.get_children_by_teacher_login(teacher_login)  # Вызываем метод получения детей
        try:
            return jsonify({"status": "success", "children": children_info}), 200
        except:
            return jsonify({"status": "success", "children": {}}), 200



    @app.route('/login_parents', methods=['POST'])
    def login_parents():
        login = request.form.get('login')
        password =  request.form.get('password')
        result = DB.login_parents(login, password)
        return jsonify({"status": "success", "message": result}), 200

    @app.route('/login_teacher', methods=['POST'])
    def login_teacher():
        login = request.form.get('login')
        password =  request.form.get('password')
        result = DB.login_teacher(login, password)
        return jsonify({"status": "success", "message": result}), 200


    @app.route('/tasks', methods=['GET'])
    def get_teacher_tasks():
        login = request.args.get('login')
        result = DB.inset_profile_teacher_task(login)
        return jsonify({"status": "success", "message": result}), 200


    @app.route('/update_teach', methods=['PUT'])
    def update_teach():
        data = request.json
        login = data.get('login')
        login_children = data.get('login_children')
        if not all([login, login_children]):
            return jsonify({"status": "error", "message": "Не все данные заполнены"}), 400
        result = DB.update_teach(login, login_children)
        return jsonify({"status": "success", "message": result}), 200

    @app.route('/update_parents', methods=['PUT'])
    def update_parents():
        data = request.json
        login = data.get('login')
        login_children = data.get('login_children')
        if not all([login, login_children]):
            return jsonify({"status": "error", "message": "Не все данные заполнены"}), 400
        result = DB.update_parents(login, login_children)
        return jsonify({"status": "success", "message": result}), 200

    @app.route('/create_task', methods=['POST'])
    def create_task():
        data = request.json
        login_children = data.get('login_children')
        access_level = data.get('access_level')
        task_name = data.get('task_name')  # Добавлено
        task_text = data.get('task_text')
        status = data.get('status')
        deadline = data.get('deadline')
        from_login = data.get('from_login')

        result = DB.create_task(login_children, access_level, task_name, task_text, status, deadline, from_login)
        return jsonify({"status": "success", "message": result}), 200

    @app.route('/update_task_status', methods=['PUT'])
    def update_task_status():
        data = request.json
        task_id = data.get('task_id')
        new_status = data.get('new_status')
        if not all([task_id, new_status]):
            return jsonify({"status": "error", "message": "Не все данные заполнены"}), 400
        result = DB.update_task_status(task_id, new_status)
        return jsonify({"status": "success", "message": result}), 200

    @app.route('/delete_task', methods=['DELETE'])
    def delete_task():
        data = request.json
        task_id = data.get('task_id')
        if not task_id:
            return jsonify({"status": "error", "message": "Не все данные заполнены"}), 400
        result = DB.delete_task(task_id)
        return jsonify({"status": "success", "message": result}), 200

    @app.route('/create_note', methods=['POST'])
    def create_note():
        data = request.json
        login_children = data.get('login_children')
        access_level = data.get('access_level')
        notes_text = data.get('notes_text')
        if not all([login_children, access_level, notes_text]):
            return jsonify({"status": "error", "message": "Не все данные заполнены"}), 400
        result = DB.create_note(login_children, access_level, notes_text)
        return jsonify({"status": "success", "message": result}), 200

    @app.route('/delete_note', methods=['DELETE'])
    def delete_note():
        data = request.json
        note_id = data.get('note_id')
        if not note_id:
            return jsonify({"status": "error", "message": "Не все данные заполнены"}), 400
        result = DB.delete_note(note_id)
        return jsonify({"status": "success", "message": result}), 200

    @app.route('/get_all_tasks', methods=['POST'])
    def get_all_tasks():
        data = request.get_json()
        login = data.get('login')
        result = DB.get_all_tasks(login)
        return jsonify({"status": "success", "tasks": result}), 200

    @app.route('/get_notes_by_login', methods=['GET'])
    def get_notes_by_login():
        login_children = request.args.get('login_children')
        result = DB.get_notes_by_login(login_children)
        return jsonify({"status": "success", "notes": result}), 200


    @app.route('/task_sum', methods=['GET'])
    def get_task_sum():
        login = request.args.get('login')
        sum_task = SumTask()
        result = sum_task.task_filter(login)
        return jsonify({"status": "success", "data": result}), 200


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True) 