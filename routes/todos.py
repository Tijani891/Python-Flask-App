from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from forms.todo_forms import TodoForm, CategoryForm
from services.todo_service import (
    get_user_todos, create_todo, update_todo,
    delete_todo, complete_todo, get_todo_stats,
    get_or_create_category,
)
from services.search_service import search_todos, get_todos_due_today, get_overdue_todos
from models.todo import Todo, TodoStatus, Priority
from models.category import Category

todos_bp = Blueprint('todos', __name__, url_prefix='/todos')


@todos_bp.route('/')
@login_required
def index():
    status = request.args.get('status')
    priority = request.args.get('priority')
    category_id = request.args.get('category_id', type=int)

    todos = get_user_todos(
        user_id=current_user.id,
        status=status,
        priority=priority,
        category_id=category_id,
    )
    categories = Category.query.filter_by(user_id=current_user.id).all()
    stats = get_todo_stats(current_user.id)
    due_today = get_todos_due_today(current_user.id)
    overdue = get_overdue_todos(current_user.id)

    return render_template('todos/index.html',
                           todos=todos,
                           categories=categories,
                           stats=stats,
                           due_today=due_today,
                           overdue=overdue)


@todos_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = TodoForm()
    form.category_id.choices = [(0, 'No Category')] + [
        (c.id, c.name)
        for c in Category.query.filter_by(user_id=current_user.id).all()
    ]

    if form.validate_on_submit():
        todo, error = create_todo(
            user_id=current_user.id,
            content=form.content.data,
            description=form.description.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            category_id=form.category_id.data if form.category_id.data != 0 else None,
        )
        if error:
            flash(error, 'danger')
        else:
            flash('Task created successfully!', 'success')
            return redirect(url_for('todos.index'))

    return render_template('todos/create.html', form=form)


@todos_bp.route('/\u003cint:todo_id\u003e/edit', methods=['GET', 'POST'])
@login_required
def edit(todo_id):
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first_or_404()
    form = TodoForm(obj=todo)
    form.category_id.choices = [(0, 'No Category')] + [
        (c.id, c.name)
        for c in Category.query.filter_by(user_id=current_user.id).all()
    ]

    if form.validate_on_submit():
        todo, error = update_todo(
            todo_id=todo_id,
            user_id=current_user.id,
            content=form.content.data,
            description=form.description.data,
            priority=Priority(form.priority.data),
            status=TodoStatus(form.status.data),
            due_date=form.due_date.data,
            category_id=form.category_id.data if form.category_id.data != 0 else None,
        )
        if error:
            flash(error, 'danger')
        else:
            flash('Task updated successfully!', 'success')
            return redirect(url_for('todos.index'))

    return render_template('todos/edit.html', form=form, todo=todo)


@todos_bp.route('/\u003cint:todo_id\u003e/complete', methods=['POST'])
@login_required
def complete(todo_id):
    todo, error = complete_todo(todo_id, current_user.id)
    if error:
        flash(error, 'danger')
    else:
        flash('Task marked as complete!', 'success')
    return redirect(url_for('todos.index'))


@todos_bp.route('/\u003cint:todo_id\u003e/delete', methods=['POST'])
@login_required
def delete(todo_id):
    success, error = delete_todo(todo_id, current_user.id)
    if error:
        flash(error, 'danger')
    else:
        flash('Task deleted successfully!', 'success')
    return redirect(url_for('todos.index'))


@todos_bp.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    status = request.args.get('status')
    priority = request.args.get('priority')
    category_id = request.args.get('category_id', type=int)

    results = search_todos(
        user_id=current_user.id,
        query=query,
        status=status,
        priority=priority,
        category_id=category_id,
    )

    return render_template('todos/search.html', results=results, query=query)


@todos_bp.route('/stats')
@login_required
def stats():
    stats = get_todo_stats(current_user.id)
    return render_template('todos/stats.html', stats=stats)