---
title: Generating variations
layout: default
parent: Tutorials
---

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

# How to introduce variations into the environment

The objective of this tutorial is to demonstrate how to specify variations of FloorPlan DSL models and generate new concrete environments. The variation model discussed in this tutorial is available [here](../models/examples/hospital.variation).

The variations of an environment are specified with the Variation DSL in a separate model. We create a new file and give it a name with the appropiate format: `<file_name>.variation`. The first line of the model imports the concrete environment where we will introduce the variations. 


```
import "hospital.fpm"
```

We can then declare the spacial attributes we wish to associate to one of the three probability distributions: normal, discrete, and uniform:

```
<attribute>: normal(mean=<mean value, in meters>, std=<standard deviation, in meters>)
<attribute>: discrete([
        (<weight 1>, <value, in meters>),
        (<weight 2>, <value, in meters>),
        ...
        (<weight n>, <value, in meters>)
    ]) // Important: all the weights must sum to 1
<attribute>: uniform([<value 1, in meters>, <value 2, in meters>, ... , <value m, in meters>])


```

We can refer to attributes through references to the corresponding spaces or features. We need to provide the FQN of the attribute inside of the scope of the reference.

```
hallway: {
    location.transformation.translation.x : normal(mean=0.0, std=5.0)
    defaults.wall.thickness : discrete([
        (0.2, 0.14),
        (0.4, 0.35),
        (0.4, 0.51)
    ])
}
```

For features such as columns and dividers, we need to provide the FQN that include the space they belong to:

```
reception.divider_central: {
    height : normal(mean=1.0, std=0.2)
    location.transformation.rotation.z : discrete([
        (0.8, 0.0),
        (0.2, 0.20)
    ])
}
```

After we have specified all the probability distributions, we can generate as many variations as we desired:

```sh
textx generate <variation model> --target fpm-v2 --variations <number of variations> -o <output folder>
```

Each resulting concrete environment will follow the format `<name of floorplan model>_<seed number>.fpm` and can be found at the specified output folder. These models are ready to be transformed into 3D models and other artefacts as shown in the previous tutorial. At the moment the generator does not check for the soundness of the resulting floor plan, nor for uniqueness.
