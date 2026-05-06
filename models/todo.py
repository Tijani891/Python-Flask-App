from extensions import db
from datetime import datetime
import enum


class Priority(str, enum.Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    URGENT = 'urgent'


class TodoStatus(str, enum.Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class Todo(db.Model):
    __tablename__ = 'todos'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=True)
    priority = db.Column(db.Enum(Priority), default=Priority.MEDIUM)
    status = db.Column(db.Enum(TodoStatus), default=TodoStatus.PENDING)
    due_date = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tags = db.relationship('Tag', secondary='todo_tags', backref='todos', lazy=True)

    def is_overdue(self):
        if self.due_date and self.status not in [TodoStatus.COMPLETED, TodoStatus.CANCELLED]:
            return datetime.utcnow() > self.due_date
        return False

    def __repr__(self):
        return f'<Todo {self.id}: {self.content[:30]}>'