import shlex
import sys

# make a dictionary that will contain the variables
variables = {}
# if an error comes up in the code, set this to true, which will break the loop.
error = False
# if the user puts "debug" in the code, this will be true and it will print the parts of the line and variables
debug_mode = False
# if we are skipping lines because of a false if-condition
skip = False
# how many { ... } levels deep we are while skipping
skip_depth = 0

# handle expressions (math, string concat, boolean expressions)
def expression(expr):
    global variables, error
    
    # only allow stuff that can be variables, currently just int, float, string, and bool, but can be more in the future
    allowed_names = variables.copy()
    return eval(expr, {"__builtins__": {}}, allowed_names)

# evaluates how variables are assigned
def variable_assignment(_type, name, value):
    global error, variables
    
    if _type == "int":
        try:
            # evaluate expressions with eval()
            result = expression(value)
            variables[name] = int(result)
        except Exception:
            print("Error: the variable's assigned type does not go with its value.")
            error = True
            return
    elif _type == "str":
        try:
            # evaluate expressions with eval()
            result = expression(value)
            variables[name] = str(result)
        except Exception:
            print("Error: the variable's assigned type does not go with its value.")
            error = True
            return
    elif _type == "float":
        try:
            # evaluate expressions with eval()
            result = expression(value)
            variables[name] = float(result)
        except Exception:
            print("Error: the variable's assigned type does not go with its value.")
            error = True
            return
    elif _type == "bool":
        try:
            # evaluate expressions with eval()
            result = expression(value)
            variables[name] = bool(result)
        except Exception:
            print("Error: the variable's assigned type does not go with its value.")
            error = True
            return
    else:
        print("Error: unknown type.")
        error = True
        return

# evaluates how type casting works
def variable_type_change(_type, name):
    global error, variables
    if _type == "int":
        try:
            variables[name] = int(variables[name])
        except ValueError:
            print("Error: the variable's type could not be changed.")
            error = True
            return
    elif _type == "str":
        try:
            variables[name] = str(variables[name])
        except ValueError:
            print("Error: the variable's type could not be changed.")
            error = True
            return
    elif _type == "float":
        try:
            variables[name] = float(variables[name])
        except ValueError:
            print("Error: the variable's type could not be changed.")
            error = True
            return
    elif _type == "bool":
        try:
            variables[name] = bool(variables[name])
        except ValueError:
            print("Error: the variable's type could not be changed.")
            error = True
            return
    else:
        print("Error: unknown type.")
        error = True
        return

# evaluates printing to the console
def printing(parts, start = 1):
    global error, variables

    # if the line is only "print", then just print an empty line
    if len(parts) == 1:
        print()
        return
    
    # get the value of the print message
    value = " ".join(parts[start:])
    
    if value in variables:
        print(variables[value])
        return
    
    # but if it is an expression!!!! 
    try:
        result = expression(value)
        print(result)
        return
    except Exception:
        print("Error: could not evaluate expression.")
        error = True
        return

# evaluates input prompts (the print part of input)
def input_prompt(parts, start = 4):
    global error, variables

    # if nothing is given for the prompt, just return an empty string
    if start >= len(parts):
        return ""
    
    # get the prompt message
    value = " ".join(parts[start:])

    # if it's a variable
    if value in variables:
        return str(variables[value])
    
    # if it's an expression
    try:
        result = expression(value)
        return str(result)
    except Exception:
        print("Error: could not evaluate expression in input prompt.")
        error = True
        return None

# handles skipping false if-statements
def if_skipping(parts):
    global skip, skip_depth
    for token in parts:
        if token == "{":
            skip_depth += 1
        elif token == "}":
            skip_depth -= 1
            if skip_depth == 0:
                # close the block that started the skip
                skip = False

# handles if-statements
def if_statements(parts):
    global skip, skip_depth, error

    # Step 1: find 'then' (allow optional colon 'then:')
    then_index = None
    # go through each token in parts to find "then"
    for i, token in enumerate(parts):
        # if 'then' is found, ignore the colon if it's there, then save the index and break
        if token.rstrip(":") == "then":
            then_index = i
            break
        
    # if 'then' wasnt found, give an error
    if then_index is None:
        print("Error: if statement is missing 'then'.")
        error = True
        return

    # Step 2: make sure the condition is everything between 'if' and 'then'
    # if there is nothing between 'if' and 'then', give an error
    if then_index <= 1:
        print("Error: 'if' statement has no condition before 'then'.")
        error = True
        return

    # get the condition
    condition = " ".join(parts[1:then_index])

    # Step 3: make sure that there is a '{' after 'then'
    open_brace = False
    # go through parts to make sure that there is a '{'}
    for token in parts[then_index + 1:]:
        # if there is, then set has_open_brace to true and break
        if token == "{":
            open_brace = True
            break
    # so now, if there is no open brace, give an error
    if not open_brace:
        print("Error: if statement is missing '{'.")
        error = True
        return

    # Step 4: evaluate the condition
    try:
        # try to evaluate the condition
        condition_result = bool(expression(condition))
    except Exception:
        # uh oh, looks like we couldnt! ERROR
        print("Error: could not evaluate if-condition.")
        error = True
        return

    # Step 5: decide whether to skip the block or execute it
    # if the condition is true, just excecute the block normally
    if condition_result:
        # no skip mode, so the lines inside the block will be executed normally
        return
    # but if the condition is false, then start skip mode
    else:
        # start skipping until the '}'.
        skip = True
        # and since the '{' has been found, start at depth 1.
        skip_depth = 1
        return


# main function to read a line of code
def read_code(line):
    global error, variables, debug_mode, skip, skip_depth
    var_type = ""
    var_name = ""
    var_value = ""

    # take away all leading and trailing whitespace
    # and split the line into parts
    parts = shlex.split(line, posix = False)

    # old way of splitting the lines (just in case)
    # og_parts = line.strip().split()

    # skip empty lines
    if len(parts) == 0:
        return
   
    # if the line is a comment (indicated by a #) then skip the line
    if parts[0] == "#":
        return  
    
    # if the line is only one part and that is "debug" start debug mode and continue on with the program
    if len(parts) == 1 and parts[0] == "debug":
        debug_mode = True
        return
    
    # if we are currently skipping a false if-statement
    if skip:
        if_skipping(parts)
        return

    # closing brace when not skipping: just end the statement
    if parts[0] == "}":
        return

    # get the first word of the line, which is the command
    # in this language, each line will have a command, what the line does
    # ex: "print" to print to the console, "set" to make a variable, "change" to change a variable's value
    command = parts[0]

    # if the command is if, then do an if-statement: if <condition> then {...}
    if command == "if":
        if_statements(parts)

    # if command is "set", add a variable to the dictionary
    elif command == "set":
        var_type = parts[1] # first get the type
        var_name = parts[2] # then the variable name

        # find where the value/expression starts
        start_idx = 3
        if start_idx < len(parts) and parts[start_idx] == "=":
            start_idx += 1
        
        # get the variable value/expression
        var_value = " ".join(parts[start_idx:]) 
        
        # if the name is already in the dictionary, then give the user an error and stop
        if var_name in variables:
            print("Error: This variable already exists. Did you mean to use 'change'?")
            error = True
            return

        # evaluate which type the variable's value should be
        variable_assignment(var_type, var_name, var_value)
   
    # if the command is "change", change the value of an already existing variable
    elif command == "change":
        var_type = parts[1]
        var_name = parts[2]
        
        # find where the value/expression starts
        start_idx = 3
        if start_idx < len(parts) and parts[start_idx] == "=":
            start_idx += 1
        
        # get the variable value/expression
        var_value = " ".join(parts[start_idx:]) 
        
        # if it's not an already existing variable, GET OUT
        if not(var_name in variables):
            print("Error: This variable does not exist. Did you mean to use 'set'?")
            error = True
            return
       
        # evaluate which type the variable's value should be
        variable_assignment(var_type, var_name, var_value)


    # if command is "print", print. If it's a variable, then print the value of the variable.
    elif command == "print":
        printing(parts)
   
    # if the command is input, basically do python input based on this syntax:
    # input [set or change] [variable name] print [message]
    elif command == "input":
        # get the type of variable command
        # get the name of the variable
        var_command = parts[1]
        var_name = parts[2]

        # get the prompt message
        prompt = input_prompt(parts)
        if error or prompt is None:
            return # stop if there was an error
       
        if var_command == "set":
            # if the name is already in the dictionary, then give the user an error and stop
            if var_name in variables:
                print("Error: This variable already exists. Did you mean to use 'change'?")
                error = True
                return

            variables[var_name] = input(prompt)
       
        if var_command == "change":
            # if it's not an already existing variable, GET OUT
            if not(var_name in variables):
                print("Error: This variable does not exist. Did you mean to use 'set'?")
                error = True
                return
           
            variables[var_name] = input(prompt)
   
   
    # if the command is "type_change", then it will change the type of an existing variable
    # sytnax: type_change [variable name] [new type]
    elif command == "type_change":
        var_name = parts[1]
        new_type = parts[2]
       
        # if it's not an already existing variable, GET OUT
        if not(var_name in variables):
            print("Error: This variable does not exist. Did you mean to use 'set'?")
            error = True
            return
       
        # evaluate which type the variable should be
        variable_type_change(new_type, var_name)
       
    # if the command is "show_type" print the type of the variable
    # syntax: show_type [variable name]
    elif command == "show_type":
        var_name = parts[1]

        # if it's not an already existing variable, GET OUT
        if not(var_name in variables):
            print("Error: This variable does not exist. Did you mean to use 'set'?")
            error = True
            return

        print(type(variables[var_name]))
    
    # if it is not a known command, give an error
    else:
        print("Error: This command does not exist.")
        error = True
        return

    if debug_mode:
        print(parts)
        print(variables)
    

if __name__ == "__main__":
    # if you run: python main.py somefile.ms
    # this will use "somefile.ms"
    filename = sys.argv[1] if len(sys.argv) > 1 else "code.ms"

    with open(filename, "r") as f:
        for line in f:
            read_code(line)
            if error:
                break
