from argparse import ArgumentParser

from stlobj import StlLoader, ObjLoader, StlObject


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-f', '--from', required=True)
    parser.add_argument('-t', '--to', required=True)
    parser.add_argument('-b', '--binary', action='store_true')
    args = parser.parse_args()

    obj_path = getattr(args, 'from')
    stl_path = getattr(args, 'to')

    obj_loader = ObjLoader()
    obj_loader.parse(obj_path)

    stl_loader = StlLoader()

    for name in obj_loader.get_names():
        obj = obj_loader.get_object(name)
        stl_obj = StlObject.from_obj_object(obj)
        stl_loader.attach(stl_obj)

    stl_loader.save(stl_path, as_binary=args.binary)
