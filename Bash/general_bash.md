# Useful bash commands

1. To find out all the locations of the foo command:
```type -a foo```

2. To print the full path including the filename:
   ```realpath filename```

3. Having trouble figuring out how a macro is being expanded?  Try
    pasting the line into a terminal and adding a "-E". For example try
    changing ```mpicc -DFOO -DBAR -c foo.c``` into
   ```mpicc -DFOO -DBAR -E foo.c > foo.i``` and look at the ```foo.i``` file.

4. Execute last three (n) commands repeately. Press the up-arrow key three (n) times, the press ```Cntrl o```.
   This is execute one command and bring the next one up. Repeat as many times as needed.

5. To grep from sorted files like 'OSZICAR' in vasp,

   ```ls OSZICAR.* | sort -t. -k2,2n | xargs grep "T=" | awk '{print $2, $4, $6, $8, $10, $12}' > Etot_T_vs_time.txt ```.

6. How to find the oldest file in a directory or its subdirectories,

   ```find /path/to/directory -type f -printf '%T+ %p\n' | sort | head -n 1```.

