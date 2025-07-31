#!/bin/bash

# Replace with your actual mount point
DRIVE="/Volumes/ShopOne"

# Gently "touch" a file every 10 minutes
if [ -d "$DRIVE" ]; then
  stat "$DRIVE" > /dev/null
fi

