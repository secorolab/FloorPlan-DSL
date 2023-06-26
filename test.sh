#!/bin/bash

python3 /src/exsce_floorplan/exsce_floorplan.py -- models/hospital.floorplan
textx generate models/hospital.variation --target exsce-floorplan-dsl --variations 10 --output output 
ls -R