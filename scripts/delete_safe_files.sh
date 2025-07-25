#!/bin/bash

echo "🧹 Starting deletion of safe files..."

for file in safe_to_delete_wav.txt safe_to_delete_csv.txt safe_to_delete_csv_s2.txt safe_to_delete_wav_s2.txt; do
  if [ -f "$file" ]; then
    echo "🗑️  Deleting files listed in $file"
    tr '\n' '\0' < "$file" | xargs -0 rm -f
  else
    echo "⚠️  $file not found, skipping..."
  fi
done

echo "✅ Deletion complete."

