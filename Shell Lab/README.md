## My Shell

This shell attempts to use whatever the PS1 variable is set to before my shell runs.
If nothing has been set to the PS1, then my shell will set the PS1 variable to $.

##Change Dir
The shell will recognize whenever the user enters cd into the prompt. My shell will change directory by calling the cd method.
If the user wants to change to a directory with spaces, the "" are not needed. My shell also recognizes the ~ key and will take
the user to his/her home directory.

##Redirection
Redirection is built into the method called forkit. The forkit method is used to fork and exec programs. My shell looks for the
different cases of when either < or > is entered into the prompt. Within the forkit method, the right if statement is chosen.
Depending on which symbol is used, either FD0 or FD1 is manipulated. Then, exec is called to execute the redirection.

##Direct Paths
If the user enters /bin/ls or another direct path, then my shell will try to exec that program directly rather than look for the path.
This is done in the forkit method. The right if statement is chosen and the shell will exec that program directly.



