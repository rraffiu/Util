#!/bin/bash

show_help() {
    echo ""
    echo "Usage: $0 PATTERN [DIRECTORY]"
    echo
    echo "Deletes files matching the pattern from the specified directory and its subdirectories."
    echo
    echo "  PATTERN      The file pattern to search for (e.g., \"*.log\")."
    echo "  DIRECTORY    The directory to search within (default is current directory)."
    echo
    echo "Options:"
    echo "  -h, --help   Display this help message and exit."
    echo ""
}

# Check for help flag
if [[ "$1" == "--help" || "$1" == "-h" ]]; then
    show_help
    exit 0
fi
if [ -z "$1" ]; then
    echo ""
    echo "ERROR: File name or pattern is required."
    show_help
    exit 1
fi
FILE_PATTERN=${1}
DIR=${2:-.}
echo ""
echo "WARRNING! all the files matching pattern '$FILE_PATTERN'"
echo  "  in the directory '$DIR' and all its subdirectories will be deleted."
read -p "Do you wanto proceed? (y/n): " choice

if [[ $choice == "y" || $choice == "Y" ]]; then
        find "$DIR" -type f -name "$FILE_PATTERN" -exec rm {} \;
        echo "Deleted all files matching pattern '$FILE_PATTERN' in directory '$DIR' and its subdirectories."
else
        echo ""
        echo "Bye. No harm done."
        echo ""
        exit 1
fi





