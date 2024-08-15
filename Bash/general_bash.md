# Useful bash commands

1. To find out all the locations of the foo command:
```type -a foo```

2. To print the full path including the filename:
   ```realpath filename```

3. Having trouble figuring out how a macro is being expanded?  Try
    pasting the line into a terminal and adding a "-E". For example try
    changing ```mpicc -DFOO -DBAR -c foo.c``` into
   ```mpicc -DFOO -DBAR -E foo.c > foo.i``` and look at the ```foo.i``` file.
