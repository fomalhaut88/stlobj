import struct


class StlLoader:
    def __init__(self):
        self._objects = {}

    def parse(self, path):
        is_ascii = self.check_ascii(path)
        if is_ascii:
            self._parse_ascii(path)
        else:
            self._parse_binary(path)

    def save(self, path, as_binary=False):
        if as_binary:
            self.save_as_binary(path)
        else:
            self.save_as_ascii(path)

    def get_names(self):
        return list(self._objects.keys())

    def get_object(self, name):
        return self._objects[name]

    def attach(self, obj):
        self._objects[obj.name] = obj

    def check_ascii(self, path):
        with open(path, 'rb') as f:
            head = f.read(80)
        return head.startswith(b'solid')

    def join(self, loader):
        for obj in loader._objects.values():
            if obj.name not in self._objects:
                self._objects[obj.name] = obj
            else:
                self._objects[obj.name].triangles.extend(obj.triangles)

    def _parse_ascii(self, path):
        self._objects.clear()

        cur_obj = None
        cur_tgl = None
        with open(path) as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                if line.startswith('solid'):
                    name = line[6:]
                    cur_obj = StlObject(name)
                    self._objects[name] = cur_obj

                elif line.startswith('endsolid'):
                    cur_obj = None

                elif line.startswith('facet'):
                    cur_tgl = StlTriangle()
                    cur_tgl.normal = self._extract_vector(line)

                elif line.startswith('endfacet'):
                    cur_obj.triangles.append(cur_tgl)
                    cur_tgl = None

                elif line.startswith('vertex'):
                    vertex = self._extract_vector(line)
                    cur_tgl.vertices.append(vertex)

    def _parse_binary(self, path):
        obj = StlObject('')
        self._objects[''] = obj

        with open(path, 'rb') as f:
            f.read(80)

            # number
            number = struct.unpack('i', f.read(4))[0]

            # triangles
            for i in range(number):
                triangle = StlTriangle()

                triangle.normal = struct.unpack('3f', f.read(12))
                triangle.vertices.append(struct.unpack('3f', f.read(12)))
                triangle.vertices.append(struct.unpack('3f', f.read(12)))
                triangle.vertices.append(struct.unpack('3f', f.read(12)))

                obj.triangles.append(triangle)

                f.read(2)

    def save_as_ascii(self, path):
        with open(path, 'w') as f:
            for obj in self._objects.values():
                print("solid " + obj.name, file=f)

                for triangle in obj.triangles:
                    print("  facet normal " + self._vector_to_string(triangle.normal), file=f)
                    print("    outer loop", file=f)
                    for vertex in triangle.vertices:
                        print("      vertex " + self._vector_to_string(vertex), file=f)
                    print("    endloop", file=f)
                    print("  endfacet", file=f)

                print("endsolid " + obj.name, file=f)

    def save_as_binary(self, path):
        with open(path, 'wb') as f:
            f.write(b'\x00' * 80)

            number = sum(
                len(obj.triangles)
                for obj in self._objects.values()
            )
            f.write(struct.pack('i', number))

            for obj in self._objects.values():
                for triangle in obj.triangles:
                    f.write(struct.pack('3f', *triangle.normal))
                    f.write(struct.pack('3f', *triangle.vertices[0]))
                    f.write(struct.pack('3f', *triangle.vertices[1]))
                    f.write(struct.pack('3f', *triangle.vertices[2]))
                    f.write(b'\x00' * 2)

    @classmethod
    def _extract_vector(cls, line):
        return list(map(float, line.split()[-3:]))

    @classmethod
    def _vector_to_string(cls, vector):
        return " ".join(str(e) for e in vector)


class StlTriangle:
    def __init__(self):
        self.normal = None
        self.vertices = []


class StlObject:
    def __init__(self, name):
        self.name = name
        self.triangles = []

    @classmethod
    def from_obj_object(cls, obj):
        stl_object = cls(obj.name)

        for face in obj.f:
            ni = face[0][2] - 1
            v1i = face[0][0] - 1
            v2i = face[1][0] - 1
            v3i = face[2][0] - 1

            triangle = StlTriangle()
            triangle.normal = obj.vn[ni]
            triangle.vertices.append(obj.v[v1i])
            triangle.vertices.append(obj.v[v2i])
            triangle.vertices.append(obj.v[v3i])

            stl_object.triangles.append(triangle)

        return stl_object
