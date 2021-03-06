import unittest
import os, sys
sys.path.insert(1,os.path.abspath('..'))

import burnman
from burnman import minerals
from util import BurnManTest


class min1 (burnman.Mineral):
    def __init__(self):
        self.params = {
            'equation_of_state':'slb3',
            'V_0': 11.24e-6,
            'K_0': 161.0e9,
            'Kprime_0': 3.8,
            'G_0': 131.0e9,
            'Gprime_0': 2.1,
            'molar_mass': .0403,
            'n': 2,
            'Debye_0': 773.,
            'grueneisen_0': 1.5,
            'q_0': 1.5,
            'eta_s_0': 2.8 }


class min2 (min1):
    def __init__(self):
        min1.__init__(self)
        self.params['V_0'] = 10e-6


class test_model(BurnManTest):

    def model1(self):
        rock = min1()
        rock.set_method('slb3')
        p = [40e9]
        T = [2000]
        return burnman.Model(rock, p, T, burnman.averaging_schemes.VoigtReussHill())

    def model2(self):
        rock = min2()
        rock.set_method('slb3')
        p = [40e9]
        T = [2000]
        return burnman.Model(rock, p, T, burnman.averaging_schemes.VoigtReussHill())

    def model12(self):
        rock = burnman.Composite([0.2, 0.8], [min1(), min2()])
        rock.set_method('slb3')
        p = [40e9]
        T = [2000]
        return burnman.Model(rock, p, T, burnman.averaging_schemes.VoigtReussHill())

    def test_model1(self):
        m = self.model1()
        self.assertArraysAlmostEqual(m.K()/1e11, [2.80999713])
        self.assertArraysAlmostEqual(m.G()/1e11, [1.67031746])

    def test_vs1(self):
        m = self.model1()
        self.assertArraysAlmostEqual(m.v_s(), [6359.44860613])

    def test_vp1(self):
        m = self.model1()
        self.assertArraysAlmostEqual(m.v_p(), [11043.57489092])

    def test_vphi1(self):
        m = self.model1()
        self.assertArraysAlmostEqual(m.v_phi(), [8248.46031729])

    def test_heatstuff1(self):
        m = self.model1()
        self.assertArraysAlmostEqual(m.heat_capacity_p(), [52.32168504])
        self.assertArraysAlmostEqual(m.thermal_expansivity(), [2.40018801e-05])
        self.assertArraysAlmostEqual(m.heat_capacity_v(), [49.342414])

        # reproduce by hand:
        min = m.rock
        min.set_state(m.p[0], m.T[0])
        self.assertArraysAlmostEqual(m.thermal_expansivity(), [min.thermal_expansivity()])
        self.assertArraysAlmostEqual(m.heat_capacity_v(), [min.heat_capacity_v()])
        self.assertArraysAlmostEqual(m.heat_capacity_p(), [min.heat_capacity_p()])

    def test_heat2(self):
        m1 = self.model1()
        m2 = self.model2()
        m12 = self.model12()

        self.assertArraysAlmostEqual(m1.heat_capacity_v(), [49.342414])
        self.assertArraysAlmostEqual(m2.heat_capacity_v(), [49.34895224])
        self.assertArraysAlmostEqual(m12.heat_capacity_v(), [49.34764459])

        self.assertArraysAlmostEqual(m1.heat_capacity_p(), [52.32168504])
        self.assertArraysAlmostEqual(m2.heat_capacity_p(), [52.7768764])
        self.assertArraysAlmostEqual(m12.heat_capacity_p(), [52.68583813])

        self.assertArraysAlmostEqual(m1.thermal_expansivity(), [2.40018801e-5])
        self.assertArraysAlmostEqual(m2.thermal_expansivity(), [2.74743810e-5])
        self.assertArraysAlmostEqual(m12.thermal_expansivity(), [2.67155212e-5])

    def test_density(self):
        m1 = self.model1()
        m2 = self.model2()
        m12 = self.model12()

        self.assertArraysAlmostEqual(m1.density(), [4130.09554071])
        self.assertArraysAlmostEqual(m2.density(), [4619.86457261])
        self.assertArraysAlmostEqual(m12.density(), [4512.83334315])








if __name__ == '__main__':
    unittest.main()
