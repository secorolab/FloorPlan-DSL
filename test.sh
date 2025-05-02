#!/bin/bash

mkdir -p gen/dot/fpm2/metamodels && mkdir -p gen/dot/fpm2/models
mkdir -p gen/dot/variation/metamodels && mkdir -p gen/dot/variation/models
mkdir -p gen/variations
mkdir -p gen/json-ld/v2

# Generate diagrams for floorplan-v2 (meta)models
textx generate src/floorplan_dsl/grammar/fpm2/*.tx --target dot -o gen/dot/fpm2/metamodels --overwrite && dot -Tpng -O gen/dot/fpm2/metamodels/*.dot
textx generate models/*.fpm --target dot -o gen/dot/fpm2/models --overwrite && dot -Tpng -O gen/dot/fpm2/models/*.dot

# Generate diagrams for variation (meta)models
textx generate src/floorplan_dsl/grammar/variation/*.tx --target dot -o gen/dot/variation/metamodels --overwrite && dot -Tpng -O gen/dot/variation/metamodels/*.dot
textx generate models/*.variation --target dot -o gen/dot/variation/models --overwrite && dot -Tpng -O gen/dot/variation/models/*.dot

# Generate floorplan variations
textx generate models/hospital.variation --target fpm-v2 --variations 1 -o gen/variations
textx generate models/hbrs.variation --target fpm-v2 --variations 1 -o gen/variations
textx generate models/kitchen.variation --target fpm-v2 --variations 1 -o gen/variations

# Generate json-ld models
textx generate models/*.fpm --target json-ld -o gen/json-ld/v2 --overwrite
