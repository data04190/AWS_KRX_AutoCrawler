#! /bin/bash

#fullcode 업데이트
python3 /home/ubuntu/fullcode_update.py

#s3 업로드
aws s3 cp fullcode.csv s3://kmk-practice/fullcode.csv
