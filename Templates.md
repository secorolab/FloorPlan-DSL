# Templates

### Space

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
        {wall thickness: 0.0 m}
        {wall height: 0.0 m}
        {features:
            <feature>
        }
```

### Shapes 

**Rectangle**
```
Rectangle width=0.0 m, length=0.0 m
```
**Polygon**
```
Polygon points:[
            <points>,
        ]
```
**Point**
```
(0.0 m, 0.0 m)
```

### Entryway

```
Entryway <name>: 
    in: <wall reference 1> {and <wall reference 2>}
    shape: <shape>
    pose:
        translation: x: 0.0 m, y: 0.0 m, z: 0.0 m
        rotation: 0.0 deg
```

### Window
```
Window <name>: 
    in: <wall reference 1> {and <wall reference 2>}
    shape: <shape>
    pose:
        translation: x: 0.0 m, y: 0.0 m, z: 0.0 m
        rotation: 0.0 deg
```

### Floor Features
**Column**
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
```
Divider <name>:
    shape: <shape>
    height: 0.0 m
    from: <frame>
    pose:
        translation: x:0.0 m, y:0.0 m
        rotation: 0.0 deg
```