#!/bin/bash

# Commented out until migration to scenery_builder is complete
#python3 /usr/src/app/src/exsce_floorplan/exsce_floorplan.py -- models/hospital.floorplan

mkdir -p gen/dot/fpm1/metamodels && mkdir -p gen/dot/fpm2/metamodels && mkdir -p gen/dot/fpm1/models && mkdir -p gen/dot/fpm2/models 
mkdir -p gen/dot/variation/metamodels && mkdir -p gen/dot/variation/models
mkdir -p gen/variations
mkdir -p gen/json-ld/v2

# Generate diagrams for floorplan-v1 (meta)models
textx generate src/floorplan_dsl/grammar/fpm1/*.tx --target dot -o gen/dot/fpm1/metamodels --overwrite && dot -Tpng -O gen/dot/fpm1/metamodels/*.dot
textx generate models/examples/*.floorplan --target dot -o gen/dot/fpm1/models --overwrite && dot -Tpng -O gen/dot/fpm1/models/*.dot

# Convert floorplan models from v1 to v2
textx generate models/examples/*.floorplan --target floorplan-v2 -o models/examples 

# Generate diagrams for floorplan-v2 (meta)models
textx generate src/floorplan_dsl/grammar/fpm2/*.tx --target dot -o gen/dot/fpm2/metamodels --overwrite && dot -Tpng -O gen/dot/fpm2/metamodels/*.dot
textx generate models/examples/*.fpm2 --target dot -o gen/dot/fpm2/models --overwrite && dot -Tpng -O gen/dot/fpm2/models/*.dot

# Generate diagrams for variation (meta)models
textx generate src/floorplan_dsl/grammar/variation/*.tx --target dot -o gen/dot/variation/metamodels --overwrite && dot -Tpng -O gen/dot/variations/metamodels/*.dot
textx generate models/examples/*.variation --target dot -o gen/dot/variation/models --overwrite && dot -Tpng -O gen/dot/variation/models/*.dot

# Generate floorplan variations
textx generate models/examples/hospital.variation --target floorplan-v2 --variations 1 -o gen/variations 
textx generate models/examples/hbrs.variation --target floorplan-v2 --variations 1 -o gen/variations 
textx generate models/examples/kitchen.variation --target floorplan-v2 --variations 1 -o gen/variations 

# Generate json-ld models
textx generate models/examples/*.fpm2 --target json-ld -o gen/json-ld/v2 --overwrite 
