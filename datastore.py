global stack1
global stack2
global key_to_val
global val_to_count
stack1 = []
stack2 = []
key_to_val = {}
val_to_count = {}

def print_bad_arguments_error(command):
    print("Improper number of arguments for the command " + command + "!")

def start_repl():
    command = raw_input("> ")
    while command:
        tokens = command.split(" ")
        if tokens[0] == 'GET':
            do_get(tokens)
        elif tokens[0] == 'SET':
            do_set(tokens)
        elif tokens[0] == 'DELETE':
            do_delete(tokens)
        elif tokens[0] == 'COUNT':
            do_count(tokens)
        elif tokens[0] == 'BEGIN':
            do_begin()
        elif tokens[0] == 'ROLLBACK':
            do_rollback()
        elif tokens[0] == 'COMMIT':
            do_commit()
        else:
            print("Unrecognized command")
        command = raw_input("> ")

def do_get(tokens):
    if len(tokens) < 2:
        print_bad_arguments_error("GET")
        return
    key = tokens[1]
    if key in key_to_val:
        print(key + " = " + key_to_val[key])
    else:
        print(key + " not set")

def do_set(tokens):
    if len(tokens) < 3:
        print_bad_arguments_error("SET")
        return
    key = tokens[1]
    value = tokens[2]
    if key in key_to_val and key_to_val[key] != value:
        val_to_count[key_to_val[key]] -= 1
    if key not in key_to_val or key_to_val[key] != value:
        key_to_val[key] = value
        if value not in val_to_count:
            val_to_count[value] = 0
        val_to_count[value] += 1

def do_delete(tokens):
    if len(tokens) < 2:
        print_bad_arguments_error("DELETE")
        return
    key = tokens[1]
    if key in key_to_val:
        val = key_to_val.pop(key)
        val_to_count[val] -= 1
    else:
        print(key + " not set")

def do_count(tokens):
    if len(tokens) < 2:
        print_bad_arguments_error("COUNT")
        return
    value = tokens[1]
    if value not in val_to_count:
        print("0")
    else:
        print(val_to_count[value])

def do_begin():
    old1 = key_to_val.copy()
    old2 = val_to_count.copy()
    stack1.append(old1)
    stack2.append(old2)

def do_rollback():
    if len(stack1) == 0:
        print("NO TRANSACTION")
        return
    global key_to_val
    global val_to_count
    key_to_val = stack1.pop()
    val_to_count = stack2.pop()

def do_commit():
    if len(stack1) == 0:
        print("NO TRANSACTION")
        return
    stack1.pop()
    stack2.pop() 
        
if __name__== "__main__" :
    start_repl()