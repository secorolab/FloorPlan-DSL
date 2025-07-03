---
title: FloorPlan DSL Concepts
nav_order: 2
layout: default
---

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
1. TOC
{:toc}
</details>

# Concepts of the FloorPlan DSL
{:.no_toc}

{: .note}
In the figures below, where frames are shown, the colors for the `x` and `y` axis are red and green, respectively.


## Space

Space concepts are the main concepts in a floor plan. They can be used to describe any room or hallway as long as it is bounded by walls. The concept is agnostic to the functionality of the space itself. i.e. you can model a reception, a hallway, a storage room, a sleeping room, a waiting area, and any other space with the same concept.

### Attributes

- `name`: name for the space, should be unique

- `shape`: A [shape](#shapes) that describes the boundaries of the space. The boundaries of the space will become the walls

- `location`: A pose description.

  - `wrt`: The frame of reference for the location, can be `world` to refer to the world frame or `<space>` to refer to the space frame of another space (i.e. the centre of a rectangle or circle), or `<space>.walls[<index>]` to refer to a wall of a space

  - `of`: The frame of the space that you are locating. All walls and features of the space will keep their pose with regards to this frame. The value can be `this` to refer to the space frame of this space (i.e. the space you are modelling), or `this.walls[<index>]` to refer to one of the walls

  - `translation`: The translation in the `x` and `y` axis

  - `rotation`: The rotation w.r.t. the `z` axis of the frame in `wrt`

  - `spaced` (optional, recommended): A flag to tell the interpreter that it must calculate the correct space between the two spaces to ensure no overlap

  - `not aligned` (optional): A flag to tell the interpreter to not perform the default behaviour of aligning two spaces when two wall frames are used

- `wall`:

  - `thickness` (optional): The wall thickness for the walls of the space, when the desired value is different than the default

  - `height` (optional): The wall height for the walls of the space, when the desired value is different than the default

- `features`: A set of [features](#floor-features)

### Conventions

#### Frames

##### Space

Each space has its origin frame in its center. The `x` axis is positive to the right side and the `y` axis towards the top.

Polygon coordinates are always defined with respect to the center of the space and considering the _inside_ of the room.

##### Walls

The wall frame is located on the wall edge _inside_ of the room. The thickness of the wall is applied in its `y` (positive) direction of the wall frame.

### Example

```
Space <name>:
        shape: <shape>
        location:
            wrt: <frame>
            of: <frame>
            translation: x: 0.0 m, y:0.0 m
            rotation: z: 0.0 deg
            {spaced}
            {not aligned}
        {wall:
            {thickness: 0.0 m}
            {height: 0.0 m}
        }
        {features:
            <feature>
        }
```

## Entryway

The entryway concept is used to model the space for doorways and other openings between rooms and the outside.

### Attributes

- `name`: name for the entryway, should be unique

- `shape`: [Shape](#Shapes) for the entryway

- `location`:

  - `in`: wall reference (`<space>.walls[<index>]`). The frame associated with this wall will be used as the reference frame for the location of the entryway. When an entryway is between two spaces, both walls have to be specified. The first frame remains as a reference frame

  - `translation`: The translation in the `x` and `z` axis. Translations in the y axis should be avoided for appropriate results. 

  - `rotation`: The rotation w.r.t. the `y` axis

### Conventions

#### Frames

Note that the frame of the entryway is at the center of its shape, which means a translation of `0,5 * height` is often required

### Example

```
Entryway <name>:
    shape: <shape>
    location:
        in: <wall reference 1> {and <wall reference 2>}
        translation: x: 0.0 m, y: 0.0 m, z: 0.0 m
        rotation: y: 0.0 deg
```

## Window

### Attributes

- `name`: name for the window, should be unique.

- `shape`: [Shape](#Shapes) for the window.

- `location`:

  - `in`: wall reference (`<space>.walls[<index>]`). The frame associated with this wall will be used as the reference frame for the location of the entryway. When an entryway is between two spaces, both walls have to be specified. The first frame remains as a reference frame

  - `translation`: The translation in the `x` and `z` axis. Translations in the y axis should be avoided for appropriate results

  - `rotation`: The rotation w.r.t. the `y` axis

### Example

```
Window <name>:
    shape: <shape>
    location:
        in: <wall reference 1> {and <wall reference 2>}
        translation: x: 0.0 m, y: 0.0 m, z: 0.0 m
        rotation: y: 0.0 deg
```

## Floor Features

Features are common in the floor of a floor plan

### Column

#### Attributes

- `name`: name for the column, should be unique

- `shape`: [Shape](#Shapes) for the column

- `height`: Height of the column, in metres

- `location`:

  - `wrt`: Frame of reference, it can be: space frame of the space (`this`) or wall reference (`this.walls[<index>]`)

  - `translation`: The translation in the `x` and `y` axis

  - `rotation`: The rotation w.r.t. the `z` axis

### Example

```
Column <name>:
    shape: <shape>
    height: 0.0 m
    location:
        from: <frame>
        translation: x:0.0 m, y:0.0 m
        rotation: z: 0.0 deg
```

### Divider

#### Attributes

- `name`: name for the divider, should be unique

- `shape`: [Shape](#Shapes) for the divider

- `height`: Height of the divider, in metres

- `location`:

  - `wrt`: Frame of reference, it can be: space frame of the space (`this`) or wall reference (`this.walls[<index>]`)

  - `translation`: The translation in the `x` and `y` axis

  - `rotation`: The rotation w.r.t. the `z` axis 

### Example

```
Divider <name>:
    shape: <shape>
    height: 2.0 m
    location:
        wrt: <frame>
        translation: x:0.0 m, y:0.0 m
        rotation: z: 1.0 deg
```

## Shapes

### Rectangle

#### Rectangle (for Space or Feature)

##### Attributes

- `width`: Float, in metres

- `length`: Float, in metres

##### Example


```
Rectangle width=0.0 m, length=0.0 m
```

#### Rectangle (for Entryway or Window)

##### Attributes

- `width`: Float, in metres

- `height`: Float, in metres

##### Example

```
Rectangle width=0.0 m, height=0.0 m
```

### Polygon

**Polygon (for Space or Feature)**

#### Attributes

- `points`: Set of Points, the points are specified w.r.t to the space frame of the polygon, which is aligned with the world frame (no rotation on any axis)

#### Example

```
Polygon points:[
            <points>,
        ]
```

### Point

#### Attributes

- `x`: Float, in metres

- `y`: Float, in metres

#### Example

```
(0.0 m, 0.0 m)
```

## Locations

The location of any space or feature is specified by a translation and rotation with regards to a frame of reference. There are multiple frames of references that can be chosen for this. Apart from the world frame, each space has N + 1 frames of references that can be selected, where N is the number of walls.

### Spaces

#### Frames

For each wall in the space, there is a frame located in the middle of the inner wall, with the x axis going along the wall and the y axis perpendicular to the wall. From the perspective of being inside the room looking into one of the walls: Positive values in the x axis are located from the centre to the right, and negative values in the opposite direction. Whereas the positive direction from the y axis moves away from you and the negative direction moves closer. The frame is located at floor level, meaning that for the z axis only positive values are above the floor.

![Frames available when modelling](../../images/updated_walls_with_frames.png)

The image above illustrates a room with all of its frames. Each wall has an index, so you can select the frame of reference by specifying the index of the desired wall: `<name of space>.walls[<index>]`. You can also select the center frame of the space by just referring to the name: `<name of space>`. You may also select the world frame with the `world` keyword.

A space requires two frames in order to specify a location: A reference frame where the translation and rotation are specified from, and the frame that will get translated and rotated.

##### Using the world frame

You can select the world frame as your frame of reference by using the keyword `world`. You may only use this frame for locating spaces. Any other feature or entryway must be specified by either the center frame or one of the walls. Should be noted that you can use the `this` keyword to reference a frame when you are inside the scope of the space that frame belongs to.

```
location:
    wrt: world
    of: this
    translation: x:3.0 m, y:4.0 m
    rotation: z: 45.0 deg
```

![Pose of a space with regards to the world frame](../../images/updated_wall_location.png)

##### Using two wall frames

You can also use two wall frames to define locations. When you model a location using two wall frames, the default behaviour is to do an extra 180 degree rotation of the space you are locating so that the two spaces are not overlapping. Depending on the two walls that are chosen, the results can be different, as illustrated in the two next examples

```
location:
    wrt: my_room.walls[1]
    of: second_room.walls[0]
    translation: x:-1.0 m, y:0.0 m
    rotation: z: 0.0 deg
    spaced
```

![Pose of two spaces when walls are used as reference frames](../../images/updated_walls_with_frames_01.png)

```
location:
    wrt: my_room.walls[1]
    of: second_room.walls[1]
    translation: x:0.0 m, y:0.0 m
    rotation: z: 0.0 deg
    spaced
```

![Pose of two spaces when another wall is used as a reference frame](../../images/walls_with_frames_02.png)

#### Flags

##### Spaced

The flag `spaced` is used to tell the interpreter to calculate the combined thickness of the two walls, and space the two rooms accordingly. When not present, the two rooms are not spaced correctly, as seen in the next figure.

![Two spaces not spaced correctly, as the `spaced` flag was not included](../../images/walls_not_spaced.png)

Similarly, the default alignment behaviour can be disabled by using the `not aligned` flag, so that the two rooms overlap.

#### Aligned

```
location:
    wrt: my_room.walls[1]
    of: second_room.walls[1]
    translation: x:0.0 m, y:0.0 m
    rotation: z: 0.0 deg
    not aligned
```

![Two spaces not aligned as the `not aligned` flag was used](../../images/walls_not_aligned.png)

### Features

The language enables the modelling of doorways, windows, columns, and dividers. Features such as columns or dividers are always defined within a space scope, so you can use the "this" keyword to refer to the walls inside the space.

```
Column wall_column:
    shape: Rectangle width=0.5 m, length=0.3 m
    height: 2.5 m
    location:
        wrt: this.walls[3]
        translation: x:7.0 m, y:0.0 m, z: 0.0 m
        rotation: z: 0.0 deg
```

### Openings

Entryways and windows are specified outside of the scope of the space, after all the spaces in the floorplan have been specified. These features create the openings in the walls required to connect two spaces or one space with the "outside".

```
Entryway doorway:
    shape: Rectangle width=1.0 m, height=1.8 m
    location:
        in: my_room.walls[0] and second_room.walls[1]
        translation: x: -1.0 m, y: 0.0 m, z: 0.0 m
        rotation: z: 0.0 deg
```

Whenever an entryway or window is located in a wall shared by two spaces, you must specify the two walls that will be opened by the entryway or window (`my_room.walls[0] and second_room.walls[1]`). However, The location is specified with regards to the first frame specified, in the example above it would be `my_room.walls[0]`.

