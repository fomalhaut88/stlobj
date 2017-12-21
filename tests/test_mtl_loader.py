import unittest

from stlobj import MtlLoader


class TestMtlLoader(unittest.TestCase):
    def test_mtl_loader(self):
        mtl_loader = MtlLoader()
        mtl_loader.parse('data/example.mtl')

        names = mtl_loader.get_names()
        self.assertSetEqual(set(names), {"m1", "m2"})

        m1 = mtl_loader.get_object("m1")
        self.assertEqual(m1.name, "m1")
        self.assertListEqual(m1['Ka'], [1.0, 0.5, 0.0])
        self.assertListEqual(m1['Kd'], [1.0, 1.0, 0.0])
        self.assertListEqual(m1['Ks'], [0.0, 0.0, 1.0])
        self.assertEqual(m1['Ns'], 20.0)

        m2 = mtl_loader.get_object("m2")
        self.assertEqual(m2.name, "m2")
        self.assertEqual(m2['map_Ka'], "tex_a.jpg")
        self.assertEqual(m2['map_Kd'], "tex_d.jpg")
        self.assertEqual(m2['map_Ks'], "tex_s.jpg")
        self.assertEqual(m2['Ns'], 20.0)
