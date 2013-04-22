#!/bin/bash
trap 'echo "script aborted by CTRL-C"; exit 1' SIGINT # traps Ctrl-C (signal 2)

DB="postgresql://user:pass@host/db"

echo "Dump all events from $DB"
for i in `scevtls -d $DB`; do
  echo "Processing event $i";
  scxmldump -fPAMm -E $i -d $DB | gzip > $i.iag_before.gz;
done

echo "Finished";
exit 0;
