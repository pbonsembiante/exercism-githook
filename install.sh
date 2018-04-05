#!/bin/bash

echo "Getting exercises directory..."

dir=$(exercism debug 2>/dev/null | grep "Exercises Directory" 2>/dev/null)
dir=$(awk '{print $3}' <<< $dir)

git_dir=$(echo $dir/.git/)

if [ -d $git_dir ]
then
    echo "Directory found at:" $dir

    hookfile=$(echo $git_dir/hooks/pre-commit)
    if [ -n $hookfile ]
    then
        cp -f pre-commit.py $hookfile
    fi

else
    echo "A git repository must exist in " $dir
fi
