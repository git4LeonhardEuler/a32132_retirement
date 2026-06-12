#!/bin/bash
if [ $# -eq 0 ]
  then
    echo -n "a32132"
  else
    echo -n " $1"
fi
sleep 1
bash a32132.sh "vaut plus que 32 sans 32"
