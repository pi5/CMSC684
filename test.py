import sys

done = False
while not done:
    option = input("Enter choice: ")
    option = int(option)
    if (option == 1):
        print "One"

    elif (option == 2):
        print "Two"

    elif (option == 3):
        print "Three"

    else:
        done = True
