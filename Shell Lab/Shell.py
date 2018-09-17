import os, sys

#Tokenizer to create a list that splits the user's input so that it can later be
#analyzed to determine what the user's command is.
def getCommand(userInput):
    userInput = userInput.split(" ")
    return userInput


#This method will determine the type of redirection: either nothing, input, or output redirection.
def redirectionType(userInput):
    type = "nothing"
    for word in userInput:
        if word == ">":
            type = "output"
            return type
        if word == "<":
            type = "input"
            return type
    return type


def forkIt(inputs,type):
    import os, sys, time, re

    pid = os.getpid()

   # os.write(1, ("About to fork (pid:%d)\n" % pid).encode())

    rc = os.fork()

    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:  # child
      #  os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" %
      #               (os.getpid(), pid)).encode())

        #The user wants to do output redirection. So will close FD1 so that instead of outputing the
        #results of the user's command to the display, it will output it to the specified input.
        if type == "output":

            #The last two entries in the list will be the output redirect char '>' and the file name.
            #Need to remove them from the list so that execve can be called without those two entries.
            fileName = inputs[len(inputs)-1]
            del inputs[len(inputs)-1]
            del inputs[len(inputs)-1]

            # redirect child's stdout by closing FD1
            os.close(1)
            # opening the user's file so that the command's output can be written to this location
            sys.stdout = open(fileName, "w")
            fd = sys.stdout.fileno()
            os.set_inheritable(fd, True)
            os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())


        elif type == "input":

            fileName = inputs[len(inputs) - 1]
            del inputs[len(inputs) - 1]
            del inputs[len(inputs) - 1]

            # redirect child's stdin by closing FD0
            os.close(0)
            # opening the user's file so that it can read the input from the given file
            sys.stdin = open(fileName, "r")
            fd = sys.stdin.fileno()
            os.set_inheritable(fd, True)
            os.write(2, ("Child: opened fd=%d for reading\n" % fd).encode())

        for dir in re.split(":", os.environ['PATH']):  # try each directory in the path
            program = "%s/%s" % (dir, inputs[0])
           # os.write(1, ("Child:  ...trying to exec %s\n" % program).encode())
            try:
                os.execve(program, inputs, os.environ)  # try to exec program
            except FileNotFoundError:  # ...expected
                pass  # ...fail quietly

        os.write(2, ("Child:    Could not exec %s\n" % inputs[0]).encode())
        sys.exit(1)  # terminate with error

    else:  # parent (forked ok)
       # os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" %
       #              (pid, rc)).encode())
        childPidCode = os.wait()
        os.write(1, ("Parent: Child %d terminated with exit code %d\n" %
                     childPidCode).encode())



userInput = "start"
while userInput != "exit":
    userInput = input("$")
    if userInput == "exit":
        os.exit()
    else:
        #Creates a list containing the user's inputs and is split by a space. Then, finds the redirection type
        #by analyzing this list.
        inputs = getCommand(userInput)
        type = redirectionType(inputs)
        forkIt(inputs,type)
