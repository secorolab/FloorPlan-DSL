# Floor Plan DSL

Floor Plan DSL is a model-driven approach to describe indoor environments. The model-driven tool interprets the models to generate 3D environments for simulation, as well as other useful artifacts. 

# Usage

This tool is currently in active development. To use the tool you can execute the following command:

```
blender --background --python exsce_floorplan/exsce_floorplan.py --python-use-system-env -- <model_path>
```

Optionally, you can remove the `--background` flag to see directly the result in Blender.

# Example

![3D asset generated from the environment description](images/example.png)

An example model for a building is available in [here](models/hospital.floorplan)

The output of the tooling is available in the [output folder](output).


# Credits

Initial project layout generated with `textx startproject`.