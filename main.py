import flet as ft
from db import main_db

def main(page: ft.Page):
    page.title = 'ToDo List'
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)

    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text in main_db.get_task():
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task_text))
        page.update()

    def create_task_row(task_id, task_text):
        task_field = ft.TextField(value=task_text, expand=True, read_only=True)

        row_task = ft.Row()

        def enable_edit(_):
            task_field.read_only = False
            task_field.update()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            task_field.update()
            page.update()

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)

        def delete_task(_):
            main_db.delete_task(task_id=task_id)
            task_list.controls.remove(row_task)
            task_field.update()
            page.update()

        delete_button = ft.IconButton(ft.Icons.DELETE, on_click=delete_task)

        row_task.controls = [task_field, edit_button, save_button, delete_button]
        return row_task
    
    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task)
            print(task_id)
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task))
            print(task_list)
            task_input.value = None
            page.update()

    task_input = ft.TextField(label='text the task', expand=True, on_submit=add_task)
    task_button = ft.IconButton(ft.Icons.SEND, on_click=add_task)








    page.add(ft.Row([task_input, task_button]), task_list)
    load_tasks()
if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main) 

