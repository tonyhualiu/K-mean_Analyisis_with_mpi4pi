#!/bin/bash

a=
b=

while getopts ":a:h:" opt; do
	case $opt in
		a)
			a=$OPTARG
			echo "-a was triggered! $OPTARG" >&2
			;;
		:)
			echo "Option -$OPTAG requires an argument!" >&2
			exit 1
			;;
		h)
			b=$OPTARG
			echo "h" >&2
			;;
		/*)
			echo "bad opt"
	esac
done

if [-z ${a}] || [-z ${b}]
then
	echo "lalla"
	exit 1
fi

