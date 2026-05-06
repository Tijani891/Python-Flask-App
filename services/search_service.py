from models.todo import Todo, TodoStatus, Priority
from models.category import Category
from datetime import datetime


def search_todos(user_id, query, status=None, priority=None,
                 category_id=None, due_before=None, due_after=None):
    search_query = Todo.query.filter_by(user_id=user_id)

    if query:
        search_term = f"%{query}%"
        search_query = search_query.filter(
            Todo.content.ilike(search_term) |
            Todo.description.ilike(search_term)
        )

    if status:
        try:
            search_query = search_query.filter_by(status=TodoStatus(status))
        except ValueError:
            pass

    if priority:
        try:
            search_query = search_query.filter_by(priority=Priority(priority))
        except ValueError:
            pass

    if category_id:
        search_query = search_query.filter_by(category_id=category_id)

    if due_before:
        try:
            due_before_dt = datetime.strptime(due_before, "%Y-%m-%d")
            search_query = search_query.filter(Todo.due_date <= due_before_dt)
        except ValueError:
            pass

    if due_after:
        try:
            due_after_dt = datetime.strptime(due_after, "%Y-%m-%d")
            search_query = search_query.filter(Todo.due_date >= due_after_dt)
        except ValueError:
            pass

    return search_query.order_by(Todo.date_created.desc()).all()


def get_todos_due_today(user_id):
    today = datetime.utcnow().date()
    return Todo.query.filter_by(user_id=user_id).filter(
        Todo.due_date >= datetime.combine(today, datetime.min.time()),
        Todo.due_date < datetime.combine(today, datetime.max.time()),
        Todo.status.notin_([TodoStatus.COMPLETED, TodoStatus.CANCELLED])
    ).all()


def get_overdue_todos(user_id):
    return Todo.query.filter_by(user_id=user_id).filter(
        Todo.due_date < datetime.utcnow(),
        Todo.status.notin_([TodoStatus.COMPLETED, TodoStatus.CANCELLED])
    ).order_by(Todo.due_date.asc()).all()