#!/bin/bash
set -x
set -e

hdfs dfs -rm -f -r /user/root/*

# Creating HDFS Directory
hdfs dfs -mkdir -p /user/root/pre-processing
hdfs dfs -mkdir -p /user/root/aggregates
hdfs dfs -mkdir -p /user/root/index
hdfs dfs -mkdir -p /user/root/mergetree
hdfs dfs -mkdir -p /user/root/relationships
hdfs dfs -mkdir -p /user/root/relationships-ids
hdfs dfs -mkdir -p /user/root/correlations
hdfs dfs -mkdir -p /user/root/data

# Loading Spatial Structures
hdfs dfs -copyFromLocal -f ../data/neighborhood.txt /user/root/neighborhood
hdfs dfs -copyFromLocal -f ../data/neighborhood-graph.txt /user/root/neighborhood-graph
hdfs dfs -copyFromLocal -f ../data/zipcode.txt /user/root/zipcode
hdfs dfs -copyFromLocal -f ../data/zipcode-graph.txt /user/root/zipcode-graph

# Loading 'datasets' File
hdfs dfs -copyFromLocal -f ../data/dataset/datasets.txt /user/root/data/datasets

# load data
hdfs dfs -copyFromLocal -f dp/dp* /user/root/data/
