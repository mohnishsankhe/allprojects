import json
import argparse
from pathlib import Path

DATA_FILE = Path('tasks.json')

# Load tasks from file
if DATA_FILE.exists():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
else:
    tasks = []


def save_tasks():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2)


def list_tasks():
    if not tasks:
        print('No tasks found.')
        return
    for idx, task in enumerate(tasks, 1):
        status = 'done' if task.get('completed') else f"{task.get('progress', 0)}/{task.get('target', '?')}"
        print(f"{idx}. {task['description']} - {status}")


def add_task(description, target):
    task = {
        'description': description,
        'target': target,
        'progress': 0,
        'completed': False
    }
    tasks.append(task)
    save_tasks()
    print('Task added.')


def update_task(index, progress):
    try:
        task = tasks[index]
    except IndexError:
        print('Invalid task index.')
        return
    task['progress'] = progress
    if progress >= task.get('target', progress):
        task['completed'] = True
    save_tasks()
    print('Task updated.')


def complete_task(index):
    try:
        task = tasks[index]
    except IndexError:
        print('Invalid task index.')
        return
    task['completed'] = True
    task['progress'] = task.get('target', task.get('progress', 0))
    save_tasks()
    print('Task marked complete.')


def main():
    parser = argparse.ArgumentParser(description='Personal Progress Tracker')
    subparsers = parser.add_subparsers(dest='command')

    parser_list = subparsers.add_parser('list', help='List all tasks')

    parser_add = subparsers.add_parser('add', help='Add a new task')
    parser_add.add_argument('description', help='Task description')
    parser_add.add_argument('target', type=int, help='Target progress value')

    parser_update = subparsers.add_parser('update', help='Update task progress')
    parser_update.add_argument('index', type=int, help='Task index starting from 1')
    parser_update.add_argument('progress', type=int, help='New progress value')

    parser_complete = subparsers.add_parser('complete', help='Mark task complete')
    parser_complete.add_argument('index', type=int, help='Task index starting from 1')

    args = parser.parse_args()

    if args.command == 'list':
        list_tasks()
    elif args.command == 'add':
        add_task(args.description, args.target)
    elif args.command == 'update':
        update_task(args.index - 1, args.progress)
    elif args.command == 'complete':
        complete_task(args.index - 1)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
