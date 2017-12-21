from argparse import ArgumentParser

from stlobj import StlLoader, ObjLoader, ObjObject


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-f', '--from', required=True)
    parser.add_argument('-t', '--to', required=True)
    args = parser.parse_args()

    stl_path = getattr(args, 'from')
    obj_path = getattr(args, 'to')

    stl_loader = StlLoader()
    stl_loader.parse(stl_path)

    obj_loader = ObjLoader()

    for name in stl_loader.get_names():
        stl_obj = stl_loader.get_object(name)
        obj = ObjObject.from_stl_object(stl_obj)
        obj_loader.attach(obj)

    obj_loader.save(obj_path)
