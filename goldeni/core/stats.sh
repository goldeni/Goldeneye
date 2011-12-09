#!/bin/bash
awk -F '\t' '{print $2}' codes.txt
