#!/bin/bash

## Do not expand globs to themselves if they don't match
shopt -s nullglob

run_files(){
  ## if a target has been passed as an argument, use that; if not,
  ## default to '.', the current directory.
  target=${1:-.}
  for i in "$target"/*; do
    if [ -d "$i" ]; then
      run_files "$i"
    elif [[ $i == *.py ]]; then
      echo "Running $i..."
      ~/venv/bin/python "$i"
    fi
  done
}

run_files "$@"
