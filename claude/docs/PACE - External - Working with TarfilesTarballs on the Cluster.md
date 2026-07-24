---
created: 2026-02-26T19:47:01 (UTC -08:00)
tags: []
author:
---

# PACE - External - Working with Tarfiles/Tarballs on the Cluster

---

## Working with Tarfiles/Tarballs on the Cluster

### Overview

-   A tarfile (also known as a tarball) is a collection of many files into an archive file
-   This guide will cover how to work with tarfiles on the Cluster

### Commands Cheatsheet

-   General Command: `tar`
-   Operations: you must use one and only one of these arguments
    -   `-x` : extract
    -   `-c` : create
    -   `-t` : list files
    -   `-r` : append to existing
    -   `--delete` : delete from existing
-   Options : these are combined with operations
    -   `v` : verbose
    -   `f` : used to include tarfile name
    -   `z` : specifies compression with gzip
    -   `-C` : used to extract to a different directory (without this working directory is default), will be included after tarfile name
-   Also Included : separate list of file names to be extracted
-   All of these can be combined together to create a command like `tar -[Operation][Options] archive_file file_names`
-   Here are some examples:
    -   `tar -xf tarfile.tar test.txt` : extract `test.txt` from the tarfile `tarfile.tar` in working directory
    -   `tar -xvf tarfile.tar -C ~/documents` : extract contents of `tarfile.tar` to `~/documents` with verbose terminal output
    -   `tar -tvf tarfile.tar` : view all files with verbose output from `tarfile.tar`
    -   `tar -cvf new_tarfile.tar test1.txt test2.txt test3.txt` : collect the txt files and create new archive file `new_tarfile.tar` out of them

### View Contents of a Tarfile

-   You can view the contents of a tarfile with `tar -tvf tarfile.tar`
-   This will output information including the files' sizes, creation times, and their relative paths from the current directory

-   It is recommended that you extract tar files with a filesize less than 7TB into the scratch directory `~/scratch`
-   First we will navigate to the tarfile path with `cd absolute_path_to_tarfile`
-   Then we will extract its contents to the scratch space with `tar -xvf tarfile.tar -C ~/scratch`
-   This will also output the names of the files extracted
-   Finally, we will navigate to the scratch directory to view the extracted files with `cd ~/scratch`
-   You can also use this same extraction method for tarfiles compressed with Gz and Bz2 (.gz and .bz2 files)

-   There may be times where you only want to extract part of a tarfile
-   For example, the tar file that you're extracting has a size greater than 7TB so you only want to extract parts of it into the scratch directory
-   You can do this with `tar -xvf tarfile.tar file_path1 file_path2 directory_path1`
-   Make sure the paths of the files you want to extract are the same as the pathnames displayed when viewing the contents of the tarfile with `tar -tvf tarfile.tar`

### Adding Files to Tarfile

-   To add files/directories to an existing tarfile, use `tar -rvf tarfile.tar newfile1 newfile2 directory1`
-   You can add as many directories or file as you want on the same line as long as they are each separated by a space

### Removing Files from Tarfile

-   To remove files/directories from an existing tarfile, use `tar --delete -f tarfile.tar file_to_delete`
-   Make sure the path of the file/directory you want to delete is the same as the pathname displayed by `tar -tvf tarfile.tar`
-   You can remove as many directories and files as you want on the same line as long as they are each separated by a space

### Create a Tarfile

-   To create a tarfile, use `tar -cvf tarfile.tar file1 file2 directory1`
-   `tarfile.tar` is the name of the tarfile to be created
-   The files afterwards are the paths of the files to be included in the tarfile
-   To create a tarfile and compress it with gzip, use `tar -czf tarfile.tar.gz file1 file2 directory1`

### Delete a Tarfile

-   You can delete a tarfile the same way you delete any other file on Cluster, with `rm name_of_file`
-   If you want to delete the directory generated from extracting a tarfile, you will use `rm -rf name_of_directory`

### Copy Important Files to Safe Place

-   Once you are finished working in the `~/scratch` directory, you may want to transfer some files to the project directory on Phoenix (`~/p-<PI account>-0`) to keep them in a safer location that is not routinely cleaned out.
-   To do this, you will use the copy command like this `cp -r ~/scratch/{file1, file2, directory1} ~/data`
-   The first argument includes the paths of the input files and the second includes the path of the directory to transfer them to

