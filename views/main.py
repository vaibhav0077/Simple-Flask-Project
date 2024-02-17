from flask import Blueprint, render_template, flash, redirect, url_for, request
from .. import db
from flask_login import login_required, current_user
from ..models import User, Todo


main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/task', methods=['GET', 'POST'])
@login_required
def task():
    if request.method == 'POST':
        task_text = request.form.get('task_text')
        if task_text:
            new_task = Todo(text=task_text,
                            user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully.', 'success')
            return redirect(url_for('main.task'))
        else:
            flash('Task text cannot be empty.', 'danger')
            return redirect(url_for('main.add_task'))
    else:
        user = User.query.filter_by(id=current_user.id)
        return render_template('tasks.html', tasks=user[0].todos)


@main.route('/task/edit/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def edit_task(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    if request.method == 'POST':
        todo.text = request.form.get('task_text')
        db.session.commit()
        flash('Task updated successfully.', 'success')
        return redirect(url_for('main.task'))

    return render_template('edit_task.html', todo=todo)


@main.route('/task/<int:todo_id>', methods=['POST'])
@login_required
def delete_task(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        if todo.user_id == current_user.id:
            db.session.delete(todo)
            db.session.commit()
            flash('Todo deleted successfully.', 'success')
        else:
            flash('You are not authorized to delete this todo.', 'danger')
    else:
        flash('Todo not found.', 'danger')
    return redirect(url_for('main.task'))
