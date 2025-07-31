#!/bin/bash

# Replace with your actual mount point
DRIVE="/Volumes/ShopTwo"

# Gently "touch" a file every 10 minutes
if [ -d "$DRIVE" ]; then
  stat "$DRIVE" > /dev/null
fi

