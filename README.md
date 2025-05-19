# Personal Progress Tracker

This is a simple command line application for tracking progress on personal tasks. Tasks are stored locally in `tasks.json`.

## Usage

```
python progress_tracker.py list
python progress_tracker.py add "Task description" TARGET
python progress_tracker.py update INDEX PROGRESS
python progress_tracker.py complete INDEX
```

- `list` shows all current tasks.
- `add` creates a new task with a description and target progress value.
- `update` sets the progress for the given task index.
- `complete` marks the specified task as completed.

Examples:

```
python progress_tracker.py add "Read 10 pages" 10
python progress_tracker.py update 1 5
python progress_tracker.py complete 1
```

The tasks are stored in `tasks.json` in the same directory as the script.
