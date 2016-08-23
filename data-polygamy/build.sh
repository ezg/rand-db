#!/bin/bash
set -x
set -e

(cd ../data-polygamy/ && mvn clean package)
cp ../data-polygamy/target/data-polygamy-0.1-jar-with-dependencies.jar ./data-polygamy.jar
