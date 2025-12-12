# Welcome to MomScript!

# comments can be put on their own line starting with a hashtag

# print a string
print "Hello World!"

# make variables!
set int num 17
set str name "Murat"
set float decimal 6.7
set bool condition true

# print variables!
print num
print name
print decimal
print condition

# change the values of variables!
# you can even change their type!
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
