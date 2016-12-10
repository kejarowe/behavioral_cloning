#!/bin/bash

find . -name *.csv -exec sed -i -e 's/\/Users\/krowe\/sdc_nano\/behavioral_cloning/\/home\/ubuntu\/behavioral_cloning/g' {} \;
