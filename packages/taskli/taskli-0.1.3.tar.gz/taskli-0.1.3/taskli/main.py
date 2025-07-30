#!/usr/bin/env python3

import typer
from datetime import datetime
from rich import print
import json
from pathlib import Path
from typing import Optional

app = typer.Typer()
task_list = []

DATA_FILE ="tasks.json"
DATA_PATH = Path(DATA_FILE)

def load_tasks():
    """Load tasks once at startup"""
    global task_list
    if DATA_PATH.exists():
        with open(DATA_FILE, "r") as f:
            task_list = json.load(f)
    else:
        task_list = []

#saving data to json
def save_tasks(tasks):
    """Save tasks to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)


#global load tasks_list
load_tasks()


#add
@app.command()
def add(task:str):
    task_dict={
        "id":len(task_list)+1,
        "desc":task,
        "status":"todo",
        "created_at":datetime.now().strftime("%H:%M:%S, %d/%m/%Y"),
        "updated_at":datetime.now().strftime("%H:%M:%S, %d/%m/%Y")
    }

    task_list.append(task_dict)
    save_tasks(task_list)

#update
@app.command()
def update(id:int, task:str):
    task_list[id-1]["desc"] = task
    task_list[id-1]["updated_at"] = datetime.now().strftime("%H:%M:%S, %d/%m/%Y")
    save_tasks(task_list)

#delete
@app.command()
def delete(id:int):
    if id < 1 or id > len(task_list):
        print(f"[red]Error:[/red] Invalid task ID {id}")
        return
    del task_list[id-1]
    for index, task in enumerate(task_list, start=1):
        task["id"] = index
    save_tasks(task_list)

@app.command()
def mark_in_progress(id:int):
    if id < 1 or id > len(task_list):
        print(f"[red]Error:[/red] Invalid task ID {id}")
        return
    task_list[id-1]["status"] = "in-progress"
    save_tasks(task_list)

@app.command()
def mark_done(id:int):
    if id < 1 or id > len(task_list):
        print(f"[red]Error:[/red] Invalid task ID {id}")
        return
    task_list[id-1]["status"] = "done"
    save_tasks(task_list)
    
from rich.console import Console
from rich.table import Table

@app.command()
def list(category: Optional[str] = typer.Argument(None, help="Filter by status: 'done', 'in-progress', or 'todo'")):
    if not task_list:
        console.print("[yellow]No tasks found![/yellow]")
        return
    
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    
    # Add columns
    table.add_column("ID", style="cyan", width=4)
    table.add_column("Description", style="green", min_width=20)
    table.add_column("Status", style="yellow")
    table.add_column("Last Updated", style="dim")

    if category is None:  
        # Show all tasks
        for task in task_list:
            table.add_row(
                str(task["id"]),
                task["desc"],
                task["status"],
                task["updated_at"]
            )
        if task_list:  # If there are tasks, print the table
            console.print(table)
        else:
            console.print("[yellow]No tasks found![/yellow]")
    else:
        # Filter by category
        has_tasks = False
        for task in task_list:
            if task["status"] == category:
                has_tasks = True
                table.add_row(
                    str(task["id"]),
                    task["desc"],
                    task["status"],
                    task["updated_at"]
                )
        if has_tasks:
            console.print(table)
        else:
            console.print(f"No tasks in '[yellow]{category}[/yellow]' status")
    
    

if __name__ == "__main__":
    app()
    