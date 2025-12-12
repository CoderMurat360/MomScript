import shlex
import sys

# make a dictionary that will contain the variables
variables = {}
# if an error comes up in the code, set this to true, which will break the loop.
error = False
# at the start of each program, ask the user if they want to enter debug mode
# debug mode will print the parts of the line and the current state of "variables"
debug_mode = False

# evaluates how variables are assigned
def variable_assignment(_type, name, value):
    global error
    global variables
    if _type == "int":
        try:
            variables[name] = int(value)
        except ValueError:
            print("Error: the variable's assigned type does not go with its value.")
            error = True
            return
    if _type == "str":
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
            variables[name] = str(value)
        else:
            print("Error: the variable's assigned type does not go with its value.")
            error = True
            return
        # try:
        #     variables[name] = str(value)
        # except ValueError:
        #     print("Error: the variable's assigned type does not go with its value.")
        #     error = True
        #     return
    if _type == "float":
        try:
            variables[name] = float(value)
        except ValueError:
            print("Error: the variable's assigned type does not go with its value.")
            error = True
            return
    if _type == "bool":
        value = value.lower()
        if value == "true":
            variables[name] = True
        elif value == "false":
            variables[name] = False
        else:
            print("Error: the variable's assigned type does not go with its value.")
            error = True
            return

# evaluates how type casting works
def variable_type_change(_type, name):
    global error
    global variables
    if _type == "int":
        try:
            variables[name] = int(variables[name])
        except ValueError:
            print("Error: the variable's type could not be changed.")
            error = True
            return
    if _type == "str":
        try:
            variables[name] = str(variables[name])
        except ValueError:
            print("Error: the variable's type could not be changed.")
            error = True
            return
    if _type == "float":
        try:
            variables[name] = float(variables[name])
        except ValueError:
            print("Error: the variable's type could not be changed.")
            error = True
            return
    if _type == "bool":
        try:
            variables[name] = bool(variables[name])
        except ValueError:
            print("Error: the variable's type could not be changed.")
            error = True
            return

# evaluates printing to the console
def output(value):
    global error
    global variables
    
    # if the message is a string, print it (of course, without the quotes
    if value.startswith('"') and value.endswith('"'):
        value = value[1:-1]
    # if it's a variable's name, then print the value of the variable.
    elif value in variables:
        value = variables[value]
    # if it's none of these, give an error
    # this will be changed later
    else:
        # neither a quoted string nor a variable name -> error
        print("Error: The message to print is neither a variable or a string.")
        error = True
        return

    print(value)

# function to read a line of code
# take the line as a parameter
def read_code(line):
    global error
    global variables
    global debug_mode
    var_type = ""
    var_name = ""
    var_value = ""
    print_val = ""

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

    # get the first word of the line, which is the command
    # in this language, each line will have a command, what the line does
    # ex: "print" to print to the console, "set" to make a variable, "change" to change a variable's value
    command = parts[0]

    # if command is "set", add a variable to the dictionary
    if command == "set":
        var_type = parts[1] # first get the type
        var_name = parts[2] # then the variable name
        var_value = parts[3] # then the variable's value
        # so an example line would be:
        # set int x 16     or
        # set str name "Yippeee"
        # command type name value

        # if the name is already in the dictionary, then give the user an error and stop
        if var_name in variables:
            print("Error: This variable already exists. Did you mean to use 'change'?")
            error = True
            return

        # evaluate which type the variable's value should be
        variable_assignment(var_type, var_name, var_value)
   
    # if the command is "change", change the value of an already existing variable
    # i got rid of "changeto", it was a bad name.
    elif command == "change":
        var_type = parts[1]
        var_name = parts[2]
        var_value = parts[3]

        # if it's not an already existing variable, GET OUT
        if not(var_name in variables):
            print("Error: This variable does not exist. Did you mean to use 'set'?")
            error = True
            return
       
        # evaluate which type the variable's value should be
        variable_assignment(var_type, var_name, var_value)

   
    # if command is "print", print. If it's a variable, then print the value of the variable.
    elif command == "print":
        # get the print message
        print_val = " ".join(parts[1:])
        output(print_val)
   
    # if the command is input, basically do python input based on this syntax:
    # input set [variable name] print [message]
    # basically when you call the input command, declare a variable
    # and print the message to go with the input
    # BUT "set" could also be "change", if the variable already exists
    elif command == "input":
        # get the type of variable command
        # get the name of the variable
        var_command = parts[1]
        var_name = parts[2]

        # then get the print value
        # the thing that will be printed will be everything after the print command
        print_val = " ".join(parts[4:])
        # if the message is a string, get rid of the quotes
        if print_val.startswith('"') and print_val.endswith('"'):
            print_val = print_val[1:-1]
        # if it's a variable's name, then make it the value of the variable.
        elif print_val in variables:
            print_val = variables[print_val]
       
        if var_command == "set":
            # if the name is already in the dictionary, then give the user an error and stop
            if var_name in variables:
                print("Error: This variable already exists. Did you mean to use 'change'?")
                error = True
                return

            variables[var_name] = input(print_val)
       
        if var_command == "change":
            # if it's not an already existing variable, GET OUT
            if not(var_name in variables):
                print("Error: This variable does not exist. Did you mean to use 'set'?")
                error = True
                return
           
            variables[var_name] = input(print_val)
   
   
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

    debug_mode = bool(input("Do you want to enter debug mode? "))
    
    with open(filename, "r") as f:
        for line in f:
            read_code(line)
            if error:
                break
