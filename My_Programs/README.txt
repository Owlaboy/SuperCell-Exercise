In the programs I wrote, I used the following libraries, sys, os, json and threading.
I wrote and tested the programs on a Linux machine.
I wrote the commands to work with the complete file path.

To run the files please make them executable first.
I made them exectuable with the command: chmod +x <filename>

In my implementation of the second exercise, I used a similar structure as the first exercise.
For every input line, I created a new thread calling a modified version of the same function from exercise 1.
The main differences are that I removed the check for different types of updates and I added thread synchronization into the functions. 
Whenever I had to access the common dictionary with all the current states, I locked the threads to make sure there weren't any accidental errors.
