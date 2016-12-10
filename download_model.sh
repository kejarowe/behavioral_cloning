#!/bin/bash

scp -i ~/sdc_nano/udacity_sdc_nano_aws_key.pem ubuntu@54.67.79.18:~/behavioral_cloning/scripts/model.json .
scp -i ~/sdc_nano/udacity_sdc_nano_aws_key.pem ubuntu@54.67.79.18:~/behavioral_cloning/scripts/model.h5 .