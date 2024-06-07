#!/bin/bash

python3 /usr/src/app/src/exsce_floorplan/exsce_floorplan.py -- models/hospital.floorplan
textx generate models/examples/hospital.variation --target exsce-floorplan-dsl --variations 10 --output output 
ls -R