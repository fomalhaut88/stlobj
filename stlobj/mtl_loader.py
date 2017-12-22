class MtlLoader:
    def __init__(self):
        self._objects = {}

    def parse(self, path):
        with open(path) as f:
            cur_obj = None

            for line in f:
                if '#' in line:
                    line = line[:line.find('#')]

                line = line.strip()

                if not line:
                    continue

                if line.startswith('newmtl '):
                    name = line[7:].strip()
                    cur_obj = MtlObject(name)
                    self._objects[name] = cur_obj

                else:
                    cur_obj.consider(line)

    def get_names(self):
        return list(self._objects.keys())

    def get_object(self, name):
        return self._objects[name]


class MtlField:
    def __init__(self, key):
        self.key = key

    def guess(self, line):
        return line.startswith(self.key + ' ')

    def extract(self, line):
        s = line[len(self.key) + 1:]
        return self.parse(s)

    def parse(self, s):
        raise NotImplementedError()


class VectorField(MtlField):
    def parse(self, s):
        return list(map(float, s.split()))


class FloatField(MtlField):
    def parse(self, s):
        return float(s)


class IntegerField(MtlField):
    def parse(self, s):
        return int(s)


class StringField(MtlField):
    def parse(self, s):
        return s.strip()


class MtlObject:
    fields = [
        VectorField('Ka'),
        VectorField('Kd'),
        VectorField('Ks'),
        FloatField('Ns'),
        IntegerField('illum'),
        StringField('map_Ka'),
        StringField('map_Kd'),
        StringField('map_Ks'),
    ]

    def __init__(self, name):
        self.name = name
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def consider(self, line):
        for field in self.__class__.fields:
            if field.guess(line):
                self.data[field.key] = field.extract(line)
                return True
        return False
