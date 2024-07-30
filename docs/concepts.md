# Concepts of the FloorPlan DSL (v2)

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

- `features`: A set of features

```floorplan
Space <name>:
        shape: <shape>
        location:
            wrt: <frame>
            of: <frame>
            translation: x: 0.0 m, y:0.0 m
            rotation: 0.0 deg
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

  - `translation`: The translation in the `x` and `z` axis. Translations in the y axis should be avoided for appropriate results

  - `rotation`: The rotation w.r.t. the `y` axis

```floorplan
Entryway <name>:
    shape: <shape>
    location:
        in: <wall reference 1> {and <wall reference 2>}
        translation: x: 0.0 m, y: 0.0 m, z: 0.0 m
        rotation: 0.0 deg
```

## Window

### Attributes

- `name`: name for the window, should be unique.

- `shape`: [Shape](#Shapes) for the window.

- `location`:

  - `in`: wall reference (`<space>.walls[<index>]`). The frame associated with this wall will be used as the reference frame for the location of the entryway. When an entryway is between two spaces, both walls have to be specified. The first frame remains as a reference frame

  - `translation`: The translation in the `x` and `z` axis. Translations in the y axis should be avoided for appropriate results

  - `rotation`: The rotation w.r.t. the `y` axis

```floorplan
Window <name>:
    shape: <shape>
    location:
        in: <wall reference 1> {and <wall reference 2>}
        translation: x: 0.0 m, y: 0.0 m, z: 0.0 m
        rotation: 0.0 deg
```

## Floor Features

Features are common in the floor of a floor plan

**Column**

### Attributes

- `name`: name for the column, should be unique

- `shape`: [Shape](#Shapes) for the column

- `height`: Height of the column, in metres

- `location`:

  - `wrt`: Frame of reference, it can be: space frame of the space (`this`) or wall reference (`this.walls[<index>]`)

  - `translation`: The translation in the `x` and `y` axis

  - `rotation`: The rotation w.r.t. the `z` axis

```floorplan
Column <name>:
    shape: <shape>
    height: 0.0 m
    location:
        from: <frame>
        translation: x:0.0 m, y:0.0 m
        rotation: 0.0 deg
```

**Divider**

### Attributes

- `name`: name for the divider, should be unique

- `shape`: [Shape](#Shapes) for the divider

- `height`: Height of the divider, in metres

- `location`:

  - `wrt`: Frame of reference, it can be: space frame of the space (`this`) or wall reference (`this.walls[<index>]`)

  - `translation`: The translation in the `x` and `y` axis

  - `rotation`: The rotation w.r.t. the `z` axis

```floorplan
Divider <name>:
    shape: <shape>
    height: 0.0 m
    location:
        wrt: <frame>
        translation: x:0.0 m, y:0.0 m
        rotation: 0.0 deg
```

## Shapes

### Rectangle

**Rectangle (for Space or Feature)**

#### Attributes

- `width`: Float, in metres

- `length`: Float, in metres

```floorplan
Rectangle width=0.0 m, length=0.0 m
```

**Rectangle (for Entryway or Window)**

#### Attributes

- `width`: Float, in metres

- `height`: Float, in metres

```floorplan
Rectangle width=0.0 m, height=0.0 m
```

### Polygon

**Polygon (for Space or Feature)**

#### Attributes

- `points`: Set of Points, the points are specified w.r.t to the space frame of the polygon, which is aligned with the world frame (no rotation on any axis)

```floorplan
Polygon points:[
            <points>,
        ]
```

### Point

#### Attributes

- `x`: Float, in metres

- `y`: Float, in metres

```floorplan
(0.0 m, 0.0 m)
```
