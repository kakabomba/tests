#!/bin/bash


def_w=100
def_h=100
def_canvas_color='rgb(255,255,255)'

function usage {
  echo "$0 --src dirsrc --dst dirdst [--w $def_w] [--h $def_h] [canvas_color=$def_canvas_color]"
  exit 0
}

source=''
dst=''
src=''
w=$def_w
h=$def_h
canvas_color=$def_canvas_color

#eval set -- "$args"
while [ $# -ge 1 ]; do
  case "$1" in
    --)
        # No more options left.
        shift
        break
       ;;
    --w)
            w="$2"
            shift
            ;;
    --h)
            h="$2"
            shift
            ;;
    --src)
            src="$2"
            shift
            ;;
    --dst)
            dst="$2"
            shift
            ;;
    --canvas_color)
            canvas_color="$2"
            shift
            ;;
    -h)
        usage    
        ;;
  esac

  shift
done


#echo  "$w ==  || $h ==  || $src ==  || $dst ==  || $canvas_color=="
#exit

if [[ "$w" == "" || "$h" == "" || "$src" == ""  ||  "$dst" == ""  || "$canvas_color" == "" ]]; then
  usage
fi

echo "rm $dst/*"
rm $dst/*

i=0

for file in $src/*; do
  echo "convert '$file' -resize "$w"x"$h" -gravity center -background "$canvas_color" -extent "$w"x"$h $dst/$(printf "%05d" $i).gif
  convert "$file" -resize "$w"x"$h" -gravity center -background "$canvas_color" -extent "$w"x"$h" $dst/$(printf "%05d" $i).gif
  i=$(( $i + 1 ))
done
