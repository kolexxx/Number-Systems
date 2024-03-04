from src.number import *
import unittest

class TestNumber(unittest.TestCase):

    def test_complement(self):
        
        num1 = Number('01101', 2, Repr.DIMINSHED_RADIX_COMPLEMENT)
        self.assertEqual(str(num1.complement()), "10010")

        num2 = Number("100", 2, Repr.RADIX_COMPLEMENT)
        self.assertEqual(str(num2.complement()), "0100")

        num3 = Number("34", 10, Repr.DIMINSHED_RADIX_COMPLEMENT)
        self.assertEqual(str(num3.complement()), "65")

    def test_equal(self):

        num1 = Number("11101", 2, Repr.SIGN_MAGNITUDE)
        num2 = Number("1D", 16, Repr.SIGN_MAGNITUDE)
        self.assertEqual(num1, num2)

    def test_add(self):

        num1 = Number("314", 7, Repr.DIMINSHED_RADIX_COMPLEMENT)
        num2 = Number("352", 7, Repr.DIMINSHED_RADIX_COMPLEMENT)
        self.assertEqual(str(add(num1, num2, 7, Repr.DIMINSHED_RADIX_COMPLEMENT)), "6")

if __name__ == '__main__':
    unittest.main()