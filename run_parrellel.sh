#!/bin/bash

usage(){
	echo "usage: \n\t-c <number of cluster>\n\t-n <number of processor>\n\t-m <path of machine file>\n\t-p <number of points per cluster>\n\t-f <data file path>\n\t-t <type of data['point' or 'DNA']>\n\t-v <max value of point or length of DNA>\n\t-h <threshold>\n\t-l <logpath>\nall must be speficified."
};

c=
n=
m=
p=
f=
t=
v=
h=
l=
point="point"
dna="DNA"

while getopts ":c:n:m:p:f:t:v:h:l:" opt; do
	case $opt in
		c)
			c=$OPTARG
			;;
		n)
			n=$OPTARG
			;;
		m)
			m=$OPTARG
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

if [ -z "$c" ] || [ -z "$n" ] || [ -z "$m" ] || [ -z "$p" ] || [ -z "$f" ] || [ -z "$t" ] || [ -z "$v" ] || [ -z "$h" ] || [ -z "$l" ];then
    usage
	exit 1
fi

if [ "$t" != "$point" ] && [ "$t" != "$dna" ];then
	echo "data type must be point or DNA"
	usage
	exit 1
fi

if [ "$t" = "$point" ];then	
	python generaterawdata.py -c $c -p $p -o $f -v $v
else
	python generatorawdata.py -c $c -p $p -o $f -v $v
fi

mpiexec -n $n -machinefile $m python src/ParallelMachine.py $c $f $t $h $l 
