from numsys.number import *
import unittest

class TestNumber(unittest.TestCase):

    def test_conversions(self):

        num1 = Number(25, 2, Repr.SM)
        self.assertEqual(str(num1), '11001')

    def test_complement(self):
        
        num1 = Number('01101', 2, Repr.DRC)
        self.assertEqual(str(-num1), '10010')

        num2 = Number('100', 2, Repr.RC)
        self.assertEqual(str(-num2), '0100')

        num3 = Number('34', 10, Repr.DRC)
        self.assertEqual(str(-num3), '65')

        num4 = Number('ADFC', 16, Repr.RC)
        self.assertEqual(str(-num4), '5204')

    def test_equal(self):

        num1 = Number('11101', 2, Repr.SM)
        num2 = Number('1D', 16, Repr.SM)
        self.assertEqual(num1, num2)

        num3 = Number('-1234', 10, Repr.SM)
        num4 = Number('8765', 10, Repr.DRC)
        self.assertEqual(num3, num4)

    def test_add(self):

        num1 = Number('26417', 8, Repr.SM)
        num2 = Number('13140', 8, Repr.SM)
        self.assertEqual(str(num1 + num2), '41557')

        num3 = Number("324", 7, Repr.DRC)
        num4 = Number("365", 7, Repr.DRC)
        self.assertEqual(str(num3 + num4), '23')

        num5 = Number('A32F', 16, Repr.RC)
        num6 = Number('476', 16, Repr.RC)
        self.assertEqual(str(num5 + num6), 'A7A5')

        num7 = Number('-6713', 9, Repr.SM)
        num8 = Number('-5128', 9 , Repr.SM)
        self.assertEqual(str(num7 + num8), '-12842')

        num9 = Number('12012', 3, Repr.SM)
        num10 = Number('-21102', 3, Repr.SM)
        self.assertEqual(str(num9 + num10), '-2020')

        num11 = Number('-3421', 5, Repr.SM)
        num12 = Number('4413', 5, Repr.SM)
        self.assertEqual(str(num11 + num12), '442')

    def test_sub(self):

        num1 = Number('124', 10, Repr.SM)
        num2 = Number('27', 10, Repr.SM)
        self.assertEqual(str(num1 - num2), '97')

        num3 = Number('-100', 2, Repr.SM)
        num4 = Number('10', 2, Repr.SM)
        self.assertEqual(str(num3 - num4), '-110')

        num5 = Number('8135', 16, Repr.RC)
        num6 = Number('FA3B', 16, Repr.RC)
        self.assertEqual(str(num5 - num6), '86FA')

        num7 = Number('364', 7, Repr.RC)
        num8 = Number('302', 7, Repr.RC)
        self.assertEqual(str(num7 - num8), '6062')

        num9 = Number('A32F', 16, Repr.DRC)
        num10 = Number('524', 16, Repr.DRC)
        self.assertEqual(str(num9 - num10), '9E0B')

        num11 = Number('22', 4, Repr.SM)
        num12 = Number('322', 4, Repr.SM)
        self.assertEqual(str(num11 - num12), '-300')

if __name__ == '__main__':
    unittest.main()