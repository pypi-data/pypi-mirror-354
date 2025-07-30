#!/bin/bash

DIR="$1"

if [ -z "$DIR" ]; then
  echo "No directory provided."
  exit 1
fi

UNAME=$(uname)
if [[ "$UNAME" == "Darwin" || "$UNAME" == "Linux" ]]; then
  chmod -R u+rwX "$DIR"

elif [[ "$UNAME" == *"MINGW"* || "$UNAME" == *"MSYS"* || "$UNAME" == *"CYGWIN"* ]]; then
  icacls "$DIR" /grant Everyone:F /T > /dev/null

else
  echo "Unsupported OS: $UNAME"
  exit 1
fi
