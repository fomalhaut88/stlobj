from copy import deepcopy

import numpy as np


class ObjLoader:
    def __init__(self):
        self._mtllib = None
        self._objects = {}

    def attach(self, obj, ignore_empty=False):
        if not ignore_empty or obj.f:
            self._objects[obj.name] = obj

    def parse(self, path):
        cur_obj = ObjObject('')

        with open(path) as fin:
            v_shift_cur = 0
            vt_shift_cur = 0
            vn_shift_cur = 0
            vp_shift_cur = 0

            v_shift = 0
            vt_shift = 0
            vn_shift = 0
            vp_shift = 0

            for line in fin:
                if '#' in line:
                    line = line[:line.find('#')]

                line = line.strip()

                if not line:
                    continue

                if line.startswith('mtllib '):
                    self._mtllib = line[7:].strip()

                elif line.startswith("o "):
                    name = line[2:]

                    self.attach(cur_obj, ignore_empty=True)
                    cur_obj = ObjObject(name)

                    v_shift += v_shift_cur
                    vt_shift += vt_shift_cur
                    vn_shift += vn_shift_cur
                    vp_shift += vp_shift_cur
                    v_shift_cur = 0
                    vt_shift_cur = 0
                    vn_shift_cur = 0
                    vp_shift_cur = 0

                elif line.startswith("v "):
                    vec = self._extract_vector(line[2:], slice_=3)
                    cur_obj.v.append(vec)
                    v_shift_cur += 1

                elif line.startswith("vt "):
                    vec = self._extract_vector(line[3:], slice_=3)
                    cur_obj.vt.append(vec)
                    vt_shift_cur += 1

                elif line.startswith("vn "):
                    vec = self._extract_vector(line[3:], slice_=3)
                    cur_obj.vn.append(vec)
                    vn_shift_cur += 1

                elif line.startswith("vp "):
                    vec = self._extract_vector(line[3:])
                    cur_obj.vp.append(vec)
                    vp_shift_cur += 1

                elif line.startswith("f "):
                    faces = self._parse_face(line[2:])
                    for face in faces:
                        face = self._shift_face(face, -v_shift, -vt_shift, -vn_shift, -vp_shift)
                        cur_obj.f.append(face)

                elif line.startswith("s "):
                    if line[2:].strip() != 'off':
                        cur_obj.s = int(line[2:])

                elif line.startswith("usemtl "):
                    cur_obj.mtl = line[7:].strip()

        self.attach(cur_obj, ignore_empty=True)

    def save(self, path):
        with open(path, 'w') as out:
            v_shift = 0
            vt_shift = 0
            vn_shift = 0
            vp_shift = 0

            for obj in self._objects.values():
                # object's name
                print("o " + obj.name, file=out)

                # vertices
                for vertex in obj.v:
                    print("v " + self._vector_to_strig(vertex), file=out)

                # texcoords
                for texcoord in obj.vt:
                    print("vt " + self._vector_to_strig(texcoord), file=out)

                # normals
                for normal in obj.vn:
                    print("vn " + self._vector_to_strig(normal), file=out)

                # params
                for param in obj.vp:
                    print("vp " + self._vector_to_strig(param), file=out)

                # mtl
                if obj.mtl is not None:
                    print("usemtl " + obj.mtl, file=out)

                # s
                if obj.s is not None:
                    print("s " + str(obj.s), file=out)
                else:
                    print("s off", file=out)

                # f
                for face in obj.f:
                    face = self._shift_face(face, v_shift, vt_shift, vn_shift, vp_shift)
                    print("f " + self._face_to_string(face), file=out)

                print(file=out)

                v_shift += len(obj.v)
                vt_shift += len(obj.vt)
                vn_shift += len(obj.vn)
                vp_shift += len(obj.vp)

    def get_names(self):
        return list(self._objects.keys())

    def get_object(self, name):
        return self._objects[name]

    @property
    def mtllib(self):
        return self._mtllib

    @classmethod
    def _vector_to_strig(cls, vec):
        return ' '.join(str(e) for e in vec)

    @classmethod
    def _face_to_string(cls, face):
        a = []
        for e in face:
            s = '/'.join(map(cls._stringify, e))
            while s.endswith('/'):
                s = s[:-1]
            a.append(s)
        return ' '.join(a)

    @classmethod
    def _shift_face(cls, face, v_shift, vt_shift, vn_shift, vp_shift):
        face = deepcopy(face)
        for e in face:
            if e[0] is not None:
                e[0] += v_shift
            if e[1] is not None:
                e[1] += vt_shift
            if e[2] is not None:
                e[2] += vn_shift
            if e[3] is not None:
                e[3] += vp_shift
        return face

    @classmethod
    def _stringify(cls, e):
        if e is None:
            return ''
        else:
            return str(e)

    @classmethod
    def _extract_vector(cls, line, slice_=None):
        items = line.split()
        if slice_ is not None:
            items = items[-slice_:]
        return list(map(float, items))

    @classmethod
    def _parse_face(cls, face_str):
        # "1/2/3 4/5/6" -> ['1/2/3', '4/5/6']
        items = face_str.strip().split()

        # ['1/2/3', '4/5/6'] -> [[1, 2, 3], [4, 5, 6]]
        face = []
        for item in items:
            indices = list(map(
                lambda e: int(e) if e else None,
                item.split('/')
            ))
            while len(indices) < 4:
                indices.append(None)
            face.append(indices)

        # [a, b, c, d, e] -> [[a, b, c], [a, c, d], [a, d, e]]
        faces = []
        for i in range(len(face) - 2):
            faces.append([
                face[0],
                face[i + 1],
                face[i + 2]
            ])

        return faces



class ObjObject:
    def __init__(self, name):
        self.name = name
        self.mtl = None
        self.s = None
        self.v = []
        self.vt = []
        self.vn = []
        self.vp = []
        self.f = []

    def has_normals(self):
        return bool(self.vn)

    def calc_normals(self):
        for _ in range(len(self.v)):
            self.vn.append(np.zeros(3))

        for face in self.f:
            i1 = face[0][0] - 1
            i2 = face[1][0] - 1
            i3 = face[2][0] - 1

            v1 = np.array(self.v[i1])
            v2 = np.array(self.v[i2])
            v3 = np.array(self.v[i3])

            n = np.cross(v2 - v1, v3 - v1)

            self.vn[i1] += n
            self.vn[i2] += n
            self.vn[i3] += n

        for i in range(len(self.vn)):
            self.vn[i] = list(self.vn[i] / np.linalg.norm(self.vn[i]))

        for face in self.f:
            face[0][2] = face[0][0]
            face[1][2] = face[1][0]
            face[2][2] = face[2][0]

    @classmethod
    def from_stl_object(cls, obj):
        obj_object = cls(obj.name)

        for triangle in obj.triangles:
            n = triangle.normal
            v1 = triangle.vertices[0]
            v2 = triangle.vertices[1]
            v3 = triangle.vertices[2]

            ni = cls._ensure_index(n, obj_object.vn)
            v1i = cls._ensure_index(v1, obj_object.v)
            v2i = cls._ensure_index(v2, obj_object.v)
            v3i = cls._ensure_index(v3, obj_object.v)

            face = [
                [v1i + 1, None, ni + 1, None],
                [v2i + 1, None, ni + 1, None],
                [v3i + 1, None, ni + 1, None],
            ]
            obj_object.f.append(face)

        return obj_object

    @classmethod
    def _ensure_index(cls, elem, lst):
        try:
            return lst.index(elem)
        except ValueError:
            lst.append(elem)
            return len(lst) - 1
