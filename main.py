import click


class MyCommands(click.Group):
    pass



@click.command()
@click.option("--name", prompt="Enter your name", help="The name of the user")
def hello(name):
    click.echo(f"Hello {name}!")

PRIORITIES = {
    'o': 'optional',
    "l": 'low',
    "m": 'medium',
    "h": 'high',
    "c": 'crucial'
}

@click.command()
@click.argument('priority', type=click.Choice(PRIORITIES.keys()), default='m')
@click.argument('todofile', type=click.Path(exists=False), required=False)
@click.option('--name', prompt="Enter the todo name", help="The name of todo item")
@click.option('--description', prompt="Enter the desc", help="desc of the todo item")

def add_todo(name, description, priority, todofile):
    filename = todofile if todofile is not None else "mytodos.txt"
    with open(filename, "a+") as f:
        f.write(f"{name} : {description} :[Priority:{PRIORITIES[priority]}]\n")

@click.command()
@click.argument("idx", type=int, required=True)
def delete_todo(idx):
    with open('mytodos.txt', 'r') as f:
        todo_list = f.read().splitlines()
        if 0 <= idx < len(todo_list):
            todo_list.pop(idx - 1)  # Adjust for 0-based index
            with open("mytodos.txt", "w") as fw:
                fw.write("\n".join(todo_list))
                fw.write("\n")
        else:
            click.echo(f"Index {idx} is out of range.")

@click.command()
@click.option("--priority", type=click.Choice(PRIORITIES.keys()))
@click.argument("todofile", type=click.Path(exists=True))
def list_todos(priority, todofile):
    filename = todofile if todofile is not None else "mytodos.txt"
    with open(filename, "r") as f:
        todo_list = f.read().splitlines()
        if priority is None:
            for idx, todo in enumerate(todo_list):
                print(f"({idx}) - {todo}")
        else:
            for idx, todo in enumerate(todo_list):
                if f"[Priority:{PRIORITIES[priority]}]" in todo:
                    print(f"({idx}) - {todo}")
mycommands= MyCommands()
mycommands.add_command(hello)
mycommands.add_command(add_todo)
mycommands.add_command(delete_todo)
mycommands.add_command(list_todos)

if __name__ == "__main__":
    mycommands()
