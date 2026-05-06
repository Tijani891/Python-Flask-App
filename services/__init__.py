from services.auth_service import register_user, authenticate_user, change_password
from services.todo_service import (
    get_user_todos, create_todo, update_todo,
    delete_todo, complete_todo, get_todo_stats,
    get_or_create_category, get_or_create_tag,
)
from services.search_service import search_todos, get_todos_due_today, get_overdue_todos