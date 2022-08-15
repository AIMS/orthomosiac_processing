#!/bin/bash
echo OIOI $1

cd /metashape
mkdir /data/
aws s3 cp --recursive s3://techdev-image-processing-aims-gov-au/sample_photos/$2 /data/data
/metashape/metashape-pro/metashape.sh -r src/$1.py -platform offscreen /data/data/input /data/data/output
aws s3 cp --recursive /data/data/output s3://techdev-image-processing-aims-gov-au/sample_photos/$2/output
