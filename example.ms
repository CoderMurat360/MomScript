# Welcome to MomScript!

# comments can be put on their own line starting with a hashtag

# if you want to enter debug mode (debug mode prints the tokens and variable storage after each line run
# for now, it's in a comment
# debug

# print Hello World to the console
print "Hello World!"

# make variables!
set int num 17
set str name "Murat"
set float decimal 6.7
set bool condition True

# print variables!
print num
print name
print decimal
print condition

# change the values of variables!
change str name "User"
print num

# print the type of the variable and change it!
show_type num
type_change num str
show_type num

# user input
input set answer print "Do you like animals? "
print answer
input change answer print "Do you like spiders? "
print answer

# math expressions, string concatenation, and boolean expressions
# AND you can use equal signs if you want to!
set int equation = 20 + (4*6) / 10
set str full_name = name + ": You!"
set bool condition = True and (True or (False and True))

print equation
print full_name
print condition

# and finally, if-statements! (indentation is not required)
if condition then {
  print "Hello there."
}
