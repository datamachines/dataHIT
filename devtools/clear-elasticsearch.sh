#!/bin/bash
# reformat a simple yaml into bash variables
# sed -e 's/:[^:\/\/]/="/g;s/$/"/g;s/ *=/=/g' file.yaml > file.sh
# TODO: fix the line above to appropriately source the es index name to clear
curl -XDELETE 'localhost:9200/datahit01?pretty'
