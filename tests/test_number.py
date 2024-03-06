from src.number import *
import unittest

class TestNumber(unittest.TestCase):

    def test_conversions(self):

        num1 = Number(25, 2, Repr.SM)
        self.assertEqual(str(num1), '11001')

    def test_complement(self):
        
        num1 = Number('01101', 2, Repr.DRC)
        self.assertEqual(str(num1.complement()), '10010')

        num2 = Number('100', 2, Repr.RC)
        self.assertEqual(str(num2.complement()), '0100')

        num3 = Number('34', 10, Repr.DRC)
        self.assertEqual(str(num3.complement()), '65')

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
        self.assertEqual(str(add(num1, num2, 8, Repr.SM)), '41557')

        num3 = Number("324", 7, Repr.DRC)
        num4 = Number("365", 7, Repr.DRC)
        self.assertEqual(str(add(num3, num4, 7, Repr.DRC)), '23')

        num5 = Number('A32F', 16, Repr.RC)
        num6 = Number('476', 16, Repr.RC)
        self.assertEqual(str(add(num5, num6, 16, Repr.RC)), 'A7A5')

if __name__ == '__main__':
    unittest.main()