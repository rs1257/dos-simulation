#!/bin/bash

contiki="/contiki/examples/sky"
length=84

echo "Removing old files"
rm -f $HOME/$contiki/*.sky
rm -rf -f $HOME/$contiki/obj_sky/

for entry in "/mnt/c/Users/Ryan/Google Drive (rs1257@york.ac.uk)/Summer Project - Ryan Smith/Code/"*
do
  entry=${entry:84}
  echo $entry
  torm=$HOME/${contiki}/$entry
  rm -f $torm
  
done

echo "Copying new files"
cp -a -rf -f "/mnt/c/Users/Ryan/Google Drive (rs1257@york.ac.uk)/Summer Project - Ryan Smith/Code/." $HOME/${contiki}

echo "Done"