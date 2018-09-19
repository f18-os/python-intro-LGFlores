## My Shell

This shell attempts to use whatever the PS1 variable is set to before my shell runs.
If nothing has been set to the PS1, then my shell will set the PS1 variable to $.

#Change Dir
The shell will recognize whenever the user enters cd into the prompt. My shell will change directory by calling the cd method.
If the user wants to change to a directory with spaces, the "" are not needed. My shell also recognizes the ~ key and will take
the user to his/her home directory.



