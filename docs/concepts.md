# Concepts

## Space

Space concepts are the main concepts in a floor plan. They can be used to describe any room or hallway as long as it is bounded by walls. The concept is agnostic to the functionality of the space itself. i.e. you can model a reception, a hallway, a storage room, a sleeping room, a waiting area, and any other space with the same concept.

*Attributes*:
* name: name for the space, should be unique.
* shape: A shape that describes the boundaries of the space. The boundaries of the space will become the walls.
* location: A location description:
    * from: The frame of reference for the location, can be `world` to refer to the world frame or `<space>` to refer to the space frame of another space (i.e. the centre of a rectangle or circle), or `<space>.walls[<index>]` to refer to a wall of a space.
    * to: The frame of the space that you are locating. All walls and features of the space will keep their pose with regards to this frame. The value can be `this` to refer to the space frame of this space (i.e. the space you are modelling), or `this.walls[<index>]` to refer to one of the walls
    * pose: A pose description. it contains a translation in the `x` and `y` axis, and a rotation w.r.t. the `z` axis.
    * spaced (optional, recommended): A flag to tell the interpreter that it must calculate the correct space between the two spaces to ensure no overlap.
    * not aligned (optional): A flag to tell the interpreter to not perform the default behaviour of aligning two spaces when two wall frames are used.
* wall thickness (optional): The wall thickness for the walls of the space, when the desired value is different than the default.
* wall height (optional): The wall height for the walls of the space, when the desired value is different than the default.
* features: A set of features.
```
Space <name>:
        shape: <shape>
        location:
            from: <frame>
            to: <frame>
            pose:
                translation: x: 0.0 m, y:0.0 m
                rotation: 0.0 deg 
            {spaced}
            {not aligned}
        {wall thickness: 0.0 m}
        {wall height: 0.0 m}
        {features:
            <feature>
        }
```

## Shapes 

**Rectangle (for Space or Feature)**

*Attributes:*
* width: Float, in metres
* length: Float, in metres

```
Rectangle width=0.0 m, length=0.0 m
```

**Rectangle (for Entryway or Window)**

*Attributes:*
* width: Float, in metres
* height: Float, in metres

```
Rectangle width=0.0 m, height=0.0 m
```

**Polygon (for Space or Feature)**

*Attributes*:
* points: Set of Points, the points are specified w.r.t to the space frame of the polygon, which is aligned with the world frame (no rotation on any axis).  

```
Polygon points:[
            <points>,
        ]
```
**Point**

*Attributes*:
* x: Float, in metres
* y: Float, in metres
```
(0.0 m, 0.0 m)
```

## Entryway
The entryway concept is used to model the space for doorways and other openings between rooms and the outside. 

*Attributes*:
* Name: name for the entryway, should be unique.
* in: wall reference (`<space>.walls[<index>]`). The frame associated with this wall will be used as the reference frame for the location of the entryway. When an entryway is between two spaces, both walls have to be specified. The first frame remains as a reference frame.
* shape: Shape for the entryway. 
* pose: A pose description. it contains a translation in the `x` and `z` axis, and a rotation w.r.t. the `y` axis. Translations in the y axis should be avoided for appropriate results.

```
Entryway <name>: 
    in: <wall reference 1> {and <wall reference 2>}
    shape: <shape>
    pose:
        translation: x: 0.0 m, y: 0.0 m, z: 0.0 m
        rotation: 0.0 deg
```

## Window

*Attributes*:
* Name: name for the window, should be unique.
* in: wall reference (`<space>.walls[<index>]`). The frame associated with this wall will be used as the reference frame for the location of the window. When a window is between two spaces, both walls have to be specified. The first frame remains as a reference frame.
* shape: Shape for the window. 
* pose: A pose description. it contains a translation in the `x` and `z` axis, and a rotation w.r.t. the `y` axis. Translations in the y axis should be avoided for appropriate results.

```
Window <name>: 
    in: <wall reference 1> {and <wall reference 2>}
    shape: <shape>
    pose:
        translation: x: 0.0 m, y: 0.0 m, z: 0.0 m
        rotation: 0.0 deg
```

## Floor Features
Features are common in the floor of a floor plan.

**Column**

*Attributes*:
* Name: name for the column, should be unique.
* shape: Shape for the column.
* height: Height of the column, in metres.
* from: Frame of reference, it can be: space frame of the space (`this`) or wall reference (`this.walls[<index>]`)
* pose: A pose description. it contains a translation in the `x` and `y` axis, and a rotation w.r.t. the `z` axis.

```
Column <name>:
    shape: <shape>
    height: 0.0 m
    from: <frame>
    pose:
        translation: x:0.0 m, y:0.0 m
        rotation: 0.0 deg
```
**Divider**

*Attributes*:
* Name: name for the divider, should be unique.
* shape: Shape for the divider.
* height: Height of the divider, in metres.
* from: Frame of reference, it can be: space frame of the space (`this`) or wall reference (`this.walls[<index>]`)
* pose: A pose description. it contains a translation in the `x` and `y` axis, and a rotation w.r.t. the `z` axis.
```
Divider <name>:
    shape: <shape>
    height: 0.0 m
    from: <frame>
    pose:
        translation: x:0.0 m, y:0.0 m
        rotation: 0.0 deg
```