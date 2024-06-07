# FloorPlan DSL

The FloorPlan DSL is a model-driven approach to specify indoor environments. The language enables developers to model indoor environments by its components such as spaces, entryways, and other features such as windows and columns; allowing the re-creation of real world environments, or the creation of new ones. The models can get transformed into 3D meshes and occupancy grid maps, which can be used to simulate robot navigation tasks in most robot simulators. 

![image](images/office_no_background.png)

## Features

* **Create simulation environments**: The tooling supports the transformation of floor plan descriptions into 3D models in STL and Collada formats, which are stadard formats supported by numerous simulators.   
* **Direct simulation of navigation tasks**: The tooling also generates corresponding occupancy grid maps and configuration files for the direct simulation and execution of navigation related tasks. 
* **Create variation**: Through the Variation DSL, a companion language, variation points for all spatial relations can be specified with probability distributions. The tools generate new concrete floor plans by sampling the distributions.
* **Easy to extend**: The tool can also transform the floor plan description into composable models in json-ld format. These composable models enables the extension of the descriptions and the tooling. 

## Installation

It is strongly recommended to use Docker to install and use the FloorPlan DSL and other tools. 

### Installation through Docker

If not installed already, install docker as documented [here](https://docs.docker.com/engine/). From the root directory of this repository, build the docker image:

```
docker build . --tag floorplan:latest
```

This will build the container and assign the string `floorplan:latest` as a tag to run the correct container. To run the container execute the following command after replacing the correct paths inside the angle brackets: 

```
docker run -v $<local output folder>:/usr/src/app/output -v $<local input folder>:/usr/src/app/models -it floorplan:latest bash
```

Important *required* options of the command:
+ `-v $<local output folder>:/usr/src/app/output`: This will map a local folder of the computer with the output folder of the container, this allows the FloorPlan DSL tooling to write the artefacts directly in the local computer.
+  `-v $<local input folder>:/usr/src/app/models`: This will map a local folder of the computer with the input folder of the container, any models in the local input folder can be accessed by the FloorPlan DSL tooling.
+ `-it`: required to make the container interactive.
+ `bash`: required to make the container interactive. 

### Native installation

Install all the requirements:
* [Python 3](https://www.python.org/downloads/)
* [Blender](https://www.blender.org/download/) (v2.82a specifically, preferably installed with apt-get)
* [TextX](http://textx.github.io/textX/3.0/) 

Alternatively, you can install all requirements (except for blender) with `pip3 install -r requirements.txt`

After installing all the requirements, you can install the languages. Execute from the root directory of the repo: 

```
python3 setup.py install 
```

This will install the languages and generators. To confirm that the languages have been install, execute the commands: `textx list-languages` and `textx list-generators`. The name of the languages should appear in the output:

```
> textx list-languages
...
exsce-floorplan-dsl (*.floorplan)exsce-floorplan[0.0.1]                  A language to model indoor environments
exsce-variation-dsl (*.variation)exsce-floorplan[0.0.1]                  A language to variate models from ExSce
> textx list-generators
...
exsce-variation-dsl -> exsce-floorplan-dslexsce-floorplan[0.0.1]        Generate variations of indoor environments from .floorplan models
```

# Getting started

## Usage

This tool is currently in active development. To use the tool you can execute the following command: 

```
blender --background --python exsce_floorplan/exsce_floorplan.py --python-use-system-env -- <model_path>
```

Optionally, you can remove the `--background` flag to see directly the result opened in Blender.

***Note**: The `--` before `<model_path>` is intentional and important.*

***Note:** This tool has been tested on an ubuntu machine with Blender v2.82a* 

## Example

![3D asset generated from the environment description](images/hospital_no_brackground.png)

An example model for a building is available in [here](models/hospital.floorplan)

```
blender --background --python exsce_floorplan/exsce_floorplan.py --python-use-system-env -- ../models/examples/hospital.floorplan
```

The output of the tooling is available in the [output folder](output).

## Tutorial

Modelling an environment can be straight-forward with some background information on how the concepts are specified and related to each other. [This tutorial](docs/Tutorial.md) will explain the concepts of the language and how to position them in the environment. An overview of the concepts and their attributes is available [here](docs/concepts.md). A tutorial on the variation DSL is also available [here](docs/Variation.md).
# Acknowledgement

This work is part of a project that has received funding from the European Union's Horizon 2020 research and innovation programme SESAME under grant agreement No 101017258.

<p align="center">
    <img src="images/EU.jpg" alt="drawing" height="100"/>
    <img src="images/SESAME.jpg" alt="drawing" height="100"/>
</p>