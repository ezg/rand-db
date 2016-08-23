#!/bin/bash
set -x
set -e

m='r3.4xlarge'
n=1

datasets=('dp100-1' 'dp100-2')

resfile=rand-exp.result

rm -f $resfile

rep=10
for i in $(seq 1 $rep); do
  python rand.py > dp/dp100-1
  python rand.py > dp/dp100-2

  bash setup.sh

  # pre-processing
  for d in "${datasets[@]}"; do
    hadoop jar data-polygamy.jar edu.nyu.vida.data_polygamy.pre_processing.PreProcessing -m $m -n $n -dn $d -dh ${d}.header -dd ${d}.defaults -t week -s city -cs city -i 0 0
  done

  # scalar function
  hadoop jar data-polygamy.jar edu.nyu.vida.data_polygamy.scalar_function_computation.Aggregation -f -m $m -n $n -g 'dp100-1' 0 0 'dp100-2' 0 0

  # index
  hadoop jar data-polygamy.jar edu.nyu.vida.data_polygamy.feature_identification.IndexCreation -f -m $m -n $n -g 'dp100-1' 'dp100-2'

  # relationship
  hadoop jar data-polygamy.jar edu.nyu.vida.data_polygamy.relationship_computation.Relationship -f -r -m $m -n $n -g1 'dp100-1' -g2 'dp100-2'

  # output
  if hdfs dfs -getmerge /user/root/relationships/dp100-1-dp100-2/month-city-events-restricted /tmp/output.$i; then
    cat /tmp/output.$i >> $resfile
  else
    echo "none" >> $resfile
  fi
done
