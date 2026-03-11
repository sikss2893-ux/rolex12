from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

# Хранилище задач в памяти (простой список)
tasks = []
next_id = 1

class Task:
    def __init__(self, title, priority='medium', deadline=None):
        global next_id
        self.id = next_id
        self.title = title
        self.completed = False
        self.priority = priority
        self.deadline = deadline
        next_id += 1
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed,
            'priority': self.priority,
            'deadline': self.deadline
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify([task.to_dict() for task in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    global next_id
    data = request.json
    
    new_task = Task(
        title=data['title'],
        priority=data.get('priority', 'medium'),
        deadline=data.get('deadline')
    )
    tasks.append(new_task)
    
    return jsonify({'id': new_task.id}), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def toggle_task(id):
    task = next((t for t in tasks if t.id == id), None)
    if task:
        task.completed = not task.completed
        return jsonify({'success': True})
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    tasks = [t for t in tasks if t.id != id]
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    