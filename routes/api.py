from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from services.todo_service import (
    get_user_todos, create_todo, update_todo,
    delete_todo, complete_todo, get_todo_stats,
)
from services.search_service import search_todos
from models.todo import TodoStatus, Priority

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


@api_bp.route('/todos', methods=['GET'])
@login_required
def get_todos():
    status = request.args.get('status')
    priority = request.args.get('priority')
    category_id = request.args.get('category_id', type=int)

    todos = get_user_todos(
        user_id=current_user.id,
        status=status,
        priority=priority,
        category_id=category_id,
    )

    return jsonify({
        'status': 'success',
        'count': len(todos),
        'todos': [{
            'id': t.id,
            'content': t.content,
            'description': t.description,
            'priority': t.priority.value,
            'status': t.status.value,
            'due_date': t.due_date.isoformat() if t.due_date else None,
            'completed_at': t.completed_at.isoformat() if t.completed_at else None,
            'is_overdue': t.is_overdue(),
            'category_id': t.category_id,
            'date_created': t.date_created.isoformat(),
        } for t in todos]
    })


@api_bp.route('/todos', methods=['POST'])
@login_required
def create_todo_api():
    data = request.get_json()
    if not data or not data.get('content'):
        return jsonify({'status': 'error', 'message': 'content is required'}), 400

    todo, error = create_todo(
        user_id=current_user.id,
        content=data['content'],
        description=data.get('description'),
        priority=data.get('priority', 'medium'),
        category_id=data.get('category_id'),
    )

    if error:
        return jsonify({'status': 'error', 'message': error}), 400

    return jsonify({
        'status': 'success',
        'todo': {
            'id': todo.id,
            'content': todo.content,
            'priority': todo.priority.value,
            'status': todo.status.value,
            'date_created': todo.date_created.isoformat(),
        }
    }), 201


@api_bp.route('/todos/\u003cint:todo_id\u003e', methods=['PUT'])
@login_required
def update_todo_api(todo_id):
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400

    todo, error = update_todo(todo_id, current_user.id, **data)
    if error:
        return jsonify({'status': 'error', 'message': error}), 404

    return jsonify({
        'status': 'success',
        'todo': {
            'id': todo.id,
            'content': todo.content,
            'priority': todo.priority.value,
            'status': todo.status.value,
        }
    })


@api_bp.route('/todos/\u003cint:todo_id\u003e', methods=['DELETE'])
@login_required
def delete_todo_api(todo_id):
    success, error = delete_todo(todo_id, current_user.id)
    if error:
        return jsonify({'status': 'error', 'message': error}), 404

    return jsonify({'status': 'success', 'message': 'Task deleted successfully'})


@api_bp.route('/todos/\u003cint:todo_id\u003e/complete', methods=['POST'])
@login_required
def complete_todo_api(todo_id):
    todo, error = complete_todo(todo_id, current_user.id)
    if error:
        return jsonify({'status': 'error', 'message': error}), 400

    return jsonify({
        'status': 'success',
        'todo': {
            'id': todo.id,
            'content': todo.content,
            'status': todo.status.value,
            'completed_at': todo.completed_at.isoformat(),
        }
    })


@api_bp.route('/todos/search', methods=['GET'])
@login_required
def search_todos_api():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'status': 'error', 'message': 'q parameter is required'}), 400

    results = search_todos(
        user_id=current_user.id,
        query=query,
        status=request.args.get('status'),
        priority=request.args.get('priority'),
    )

    return jsonify({
        'status': 'success',
        'count': len(results),
        'results': [{
            'id': t.id,
            'content': t.content,
            'priority': t.priority.value,
            'status': t.status.value,
        } for t in results]
    })


@api_bp.route('/stats', methods=['GET'])
@login_required
def stats_api():
    stats = get_todo_stats(current_user.id)
    return jsonify({'status': 'success', 'stats': stats})