#!/bin/bash

usage(){
	echo "usage: -c <number of cluster> -p <number of points per cluster> -f <data file path> -t <type of data['point' or 'DNA']> -v [max value] -h [threshold] -l <logpath>"
};

c=
p=
f=
t=
v=
h=
l=
point="point"
dna="DNA"

while getopts ":c:p:f:t:v:h:l:" opt; do
	case $opt in
		c)
			c=$OPTARG
			;;
		p)
			p=$OPTARG
			;;
		f)
			f=$OPTARG
			;;
		t)
			t=$OPTARG
			;;
		v)
			v=$OPTARG
			;;
		h)
			h=$OPTARG
			;;
		l)
			l=$OPTARG
			;;
		\?)
			echo "Unknown parameter tag" >&2
			usage
			;;
	esac
done

if [ -z "$c" ] || [ -z "$p" ] || [ -z "$f" ] || [ -z "$t" ] || [ -z "$v" ] || [ -z "$h" ] || [ -z "$l" ];then
    usage
	exit 1
fi

if [ "$t" != "$point" ] && [ "$t" != "$dna" ];then
	echo "data type must be point or DNA"
	usage
	exit 1
fi


echo "here"
#python generaterawdata.py
#python src/ParallelMachine.py
