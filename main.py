# Copyright (C) 2023 Riccardo Miccini <https://miccio-dk.github.io/> - All Rights Reserved
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


@app.get("/todos")
def read_todos():
    todos = {}
    with open('TODO.md') as fp:
        for line in fp:
            if line.startswith('# '):
                current_cat = line[2:].strip()
                attr_idx = current_cat.find('{')
                if attr_idx != -1:
                    tags_str = current_cat[attr_idx:].strip('{}')
                    tags_list = [kv.strip() for kv in tags_str.split(',')]
                    tags_list = [kv.split(':') for kv in tags_list]
                    tags = {k.strip(): v.strip() for k, v in tags_list}
                    current_cat = current_cat[:attr_idx].strip()
                assert current_cat not in todos
                todos[current_cat] = { 'todo': [], 'doing': [], 'done': [], 'tags': tags }
            elif line.startswith('- '):
                todos[current_cat]['todo'].append(line[2:].strip())
            elif line.startswith('. '):
                todos[current_cat]['doing'].append(line[2:].strip())
            elif line.startswith('x '):
                todos[current_cat]['done'].append(line[2:].strip())
    return todos


@app.post("/todos")
def write_todos(todos):
    print(todos)
    # TODO implement
    return todos


app.mount("/", StaticFiles(directory="static",html = True), name="static")
