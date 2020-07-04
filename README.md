# stlobj

This library contains loaders to parse 3D objects stored in [STL](https://en.wikipedia.org/wiki/STL_(file_format)), [OBJ and MTL](https://en.wikipedia.org/wiki/Wavefront_.obj_file) formats. Also there are command line scripts that convert 3D objects from STL to OBJ and back.

## Installation

```
python setup.py install
```

## Converting

From STL to OBJ:

```
stl2obj -f file.stl -t file.obj
```

From OBJ to STL:

```
obj2stl -f file.obj -t file.stl
```

## Parsing

```python
from stlobj import StlLoader

loader = StlLoader()
loader.parse("file.stl")

names = loader.get_names()  # Names of objects defined in file.stl
obj = loader.get_object(names[0])

print(obj.triangles)  # List of triangles
print(obj.triangles[0].vertices)  # Vertices of a triangle
print(obj.triangles[0].normal)  # Normal vector of a triangle
```
