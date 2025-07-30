# taskli ✨

A simple but beautiful command-line task manager with persistent storage.


## Installation

```bash
pip install taskli
```

## Quick Start

```bash
# Add a task
taskli add "Buy groceries"

# List all tasks
taskli list

# Mark task #1 as in-progress
taskli mark-in-progress 1

# Mark task #1 as done
taskli mark-done 1

# Update a task
taskli update 1 "Buy organic groceries"

# Delete a task
taskli delete 1
```

## Features

✔️ Add/update/delete tasks  
✔️ Mark tasks as todo/in-progress/done  
✔️ Persistent JSON storage  
✔️ Clean terminal interface with colors  
✔️ Filter tasks by status  

## All Commands

```
taskli add <task>         Add new task
taskli list [status]      Show tasks (optional: todo/in-progress/done)
taskli update <id> <task> Update a task
taskli delete <id>        Delete a task
taskli mark-in-progress <id>  Set task to in-progress
taskli mark-done <id>     Complete a task
```

