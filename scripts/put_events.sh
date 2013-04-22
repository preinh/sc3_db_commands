#!/bin/bash
trap 'exit 1' 2 # traps Ctrl-C (signal 2)

DB="postgresql:////user:pass@host/db"
DB="mysql://user:pass@host/db"
DB="sqlite://s//user:pass@host/db"

echo "Copy all Erice events to $DB"
for i in `ls *.iag_before.gz`; do
  gunzip -c $i | scdb -i - -b 1000 -d $DB
done
