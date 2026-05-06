from extensions import db
from models.todo import Todo, TodoStatus, Priority
from models.category import Category
from models.tag import Tag
from datetime import datetime
from flask import abort


def get_user_todos(user_id, status=None, priority=None, category_id=None, overdue=False):
    query = Todo.query.filter_by(user_id=user_id)

    if status:
        query = query.filter_by(status=status)

    if priority:
        query = query.filter_by(priority=priority)

    if category_id:
        query = query.filter_by(category_id=category_id)

    if overdue:
        query = query.filter(
            Todo.due_date < datetime.utcnow(),
            Todo.status.notin_([TodoStatus.COMPLETED, TodoStatus.CANCELLED])
        )

    return query.order_by(Todo.date_created.desc()).all()


def create_todo(user_id, content, description=None, priority='medium',
                due_date=None, category_id=None):
    todo = Todo(
        content=content,
        description=description,
        priority=Priority(priority),
        status=TodoStatus.PENDING,
        due_date=due_date,
        user_id=user_id,
        category_id=category_id,
    )
    try:
        db.session.add(todo)
        db.session.commit()
        return todo, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)


def update_todo(todo_id, user_id, **kwargs):
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
    if not todo:
        return None, "Task not found"

    for key, value in kwargs.items():
        if hasattr(todo, key) and value is not None:
            setattr(todo, key, value)

    if kwargs.get('status') == TodoStatus.COMPLETED and not todo.completed_at:
        todo.completed_at = datetime.utcnow()

    try:
        db.session.commit()
        return todo, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)


def delete_todo(todo_id, user_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
    if not todo:
        return False, "Task not found"

    try:
        db.session.delete(todo)
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)


def complete_todo(todo_id, user_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=user_id).first()
    if not todo:
        return None, "Task not found"

    if todo.status == TodoStatus.COMPLETED:
        return None, "Task already completed"

    todo.status = TodoStatus.COMPLETED
    todo.completed_at = datetime.utcnow()

    try:
        db.session.commit()
        return todo, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)


def get_todo_stats(user_id):
    todos = Todo.query.filter_by(user_id=user_id).all()

    total = len(todos)
    completed = sum(1 for t in todos if t.status == TodoStatus.COMPLETED)
    pending = sum(1 for t in todos if t.status == TodoStatus.PENDING)
    in_progress = sum(1 for t in todos if t.status == TodoStatus.IN_PROGRESS)
    cancelled = sum(1 for t in todos if t.status == TodoStatus.CANCELLED)
    overdue = sum(1 for t in todos if t.is_overdue())

    by_priority = {
        'urgent': sum(1 for t in todos if t.priority == Priority.URGENT),
        'high': sum(1 for t in todos if t.priority == Priority.HIGH),
        'medium': sum(1 for t in todos if t.priority == Priority.MEDIUM),
        'low': sum(1 for t in todos if t.priority == Priority.LOW),
    }

    completion_rate = round((completed / total * 100), 1) if total > 0 else 0

    return {
        'total': total,
        'completed': completed,
        'pending': pending,
        'in_progress': in_progress,
        'cancelled': cancelled,
        'overdue': overdue,
        'completion_rate': completion_rate,
        'by_priority': by_priority,
    }


def get_or_create_category(name, color, user_id):
    category = Category.query.filter_by(name=name, user_id=user_id).first()
    if not category:
        category = Category(name=name, color=color, user_id=user_id)
        db.session.add(category)
        db.session.commit()
    return category


def get_or_create_tag(name, color='#28a745'):
    tag = Tag.query.filter_by(name=name).first()
    if not tag:
        tag = Tag(name=name, color=color)
        db.session.add(tag)
        db.session.commit()
    return tag