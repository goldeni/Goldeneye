#!/bin/bash
if [ $1 = "all" ]; then
	awk -F '\t' '{print $2}' codes.txt	
else if [ $1 = "1" ]; then
	awk '{ for (i = 1; i <= 9; i++) /00$i/ print $2 }' codes.txt
fi

