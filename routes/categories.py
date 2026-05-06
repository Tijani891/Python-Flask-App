from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from forms.todo_forms import CategoryForm
from models.category import Category
from extensions import db

categories_bp = Blueprint('categories', __name__, url_prefix='/categories')


@categories_bp.route('/')
@login_required
def index():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('categories/index.html', categories=categories)


@categories_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CategoryForm()
    if form.validate_on_submit():
        existing = Category.query.filter_by(
            name=form.name.data,
            user_id=current_user.id
        ).first()
        if existing:
            flash('Category with this name already exists.', 'danger')
        else:
            category = Category(
                name=form.name.data,
                color=form.color.data,
                user_id=current_user.id,
            )
            db.session.add(category)
            db.session.commit()
            flash('Category created successfully!', 'success')
            return redirect(url_for('categories.index'))

    return render_template('categories/create.html', form=form)


@categories_bp.route('/\u003cint:category_id\u003e/edit', methods=['GET', 'POST'])
@login_required
def edit(category_id):
    category = Category.query.filter_by(
        id=category_id,
        user_id=current_user.id
    ).first_or_404()

    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        category.color = form.color.data
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('categories.index'))

    return render_template('categories/edit.html', form=form, category=category)


@categories_bp.route('/\u003cint:category_id\u003e/delete', methods=['POST'])
@login_required
def delete(category_id):
    category = Category.query.filter_by(
        id=category_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('categories.index'))