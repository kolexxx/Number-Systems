from enum import Enum
from copy import deepcopy

DIGIT_TO_INT = {chr(i + ord('0')) if i < 10 else chr(i - 10 + ord('A')) : i for i in range(36)}
"""
A dictionary mapping characters representing digits ('0' to '9' and 'A' to 'Z')
to their corresponding integer values from 0 to 35.
"""

INT_TO_DIGIT = {i : chr(i + ord('0')) if i < 10 else chr(i - 10 + ord('A')) for i in range(36)}
"""
A dictionary mapping integer values from 0 to 35 to 
their corresponding characters representing digits ('0' to '9' and 'A' to 'Z').
"""

class Repr(Enum):
    """
    How a number is represented aside from the numbers base.
    """

    SM = 0,
    """Sign and magnitude."""
    DRC = 1,
    """Diminshed radix complement."""
    RC = 2
    """Radix complement"""

class Number:

    def __init__(self, number, base: int, repr: Repr):

        self.base = base
        self.repr = repr

        if isinstance(number, str):
            self._digits_from_str(number)
        elif isinstance(number, int):
            self._digits_from_int(number)
        else:
            raise ValueError('Invalid type for number. It must be a string or an int.')

    def convert_to(self, base: int, repr: Repr) -> None:
        """
        Returns a number with the same value, but
        in a different specified base and representation.
        """

        if (self.base, self.repr) == (base, repr):
            return
        
        if self.base == base:

            prev = self.repr
            self.repr = repr

            # A positive number is represented the same way
            # in all of our systems.
            if self.sign == 1 and self.leading_digit() == 0:
                return
            
            # We are converting a negative number to a system 
            # of complements, so we should complement this number.
            if self.sign == -1 and prev == Repr.SM:

                if self.leading_digit() != 0:
                    self.digits.append(0)

                self._complement_self()
                self.sign *= -1
                return
            
            if prev == Repr.DRC and repr == Repr.RC:
                self += 1
                return
            
            if prev == Repr.RC and repr == Repr.DRC:
                self -= 1
                return

        # The most straight-forward way of conversion
        # is first converting the number to an unsigned
        # decimal number, then to our desired base and representation.
        value = int(self)
        self.base = base
        self.repr = repr
        self._digits_from_int(value)

    def complement(self) -> 'Number':
        """
        Returns the complement of this number.
        """

        if self.repr == Repr.SM:
            return
        
        comp = deepcopy(self)
        comp._complement_self()
        comp.sign *= -1
        
        return comp

    def leading_digit(self) -> int:
        """
        Returns the leading digit of this number. Depending on the
        number's system, it could 0 or the highest digit.
        """

        if self.repr == Repr.SM:
            return 0
        
        # In systems of complements, numbers are negative if the most
        # significant digit is a negative one. The first (base // 2) digits
        # are positive, the rest are negative. Odd bases have a neutral digit
        # which is equal to (base // 2) and we can't determine the sign if it's
        # the most significant digit.
        mid_point = self.base // 2
        lowest_neg_digit = mid_point + 1 if self.base % 2 == 1 else mid_point

        # For numbers that have an odd base, we might have to check
        # more than one digit to determine if it's a negative number.
        # eg. 314, base 7 - positive.
        # eg. 352, base 7 - negative.
        # ..333..333, base 7 - undefined.
        for digit in reversed(self.digits):

            if digit >= lowest_neg_digit:
                return self.base - 1
            elif digit < mid_point:
                return 0
            
        return mid_point

    def strip(self) -> None:
        """
        Remove excess digits so this number is represented
        with the least amount of digits.
        """

        i = len(self.digits) - 1
        mid_point = self.base // 2
        lowest_neg_digit = mid_point + 1 if self.base % 2 == 1 else mid_point

        while i >= 1:

            if self.repr == Repr.SM and self[i] == 0:
                self.digits.pop()
            elif self.repr != Repr.SM and self[i] == self.base - 1 and self[i-1] >= lowest_neg_digit:
                self.digits.pop()
            elif self.repr != Repr.SM and self[i] == 0 and self[i-1] < mid_point:
                self.digits.pop()
            else:
                break

            i -= 1

    def _digits_from_str(self, str: str) -> None:
        """
        Constructs the digits list from a string.
        """
        
        self.sign = -1 if str[0] == '-' else 1
        self.digits = [DIGIT_TO_INT[c.upper()] for c in reversed(str.strip(' -+'))]

        if self.sign == -1 and self.repr != Repr.SM:
            self._complement_self()

    def _digits_from_int(self, int: int) -> None:
        """
        Constructs the digits list from an integer.
        """

        if int == 0:
            self.sign = 1
            self.digits = [0]
            return
        
        self.sign = 1
        self.digits = []

        if int < 0:
            self.sign = -1
            int *= -1          

        while int != 0:
            self.digits.append(int % self.base)
            int //= self.base

        if self.repr == Repr.SM:
            return
        
        # Add a leading zero to make sure this number is positive.
        if self.leading_digit() != 0:
            self.digits.append(0)

        # We are dealing with a negative number, complement it.
        if self.sign == -1:
            self.sign = 1
            self._complement_self()           

    def _complement_self(self) -> None:
        """
        Complement this number in place.
        """

        if self.repr == Repr.SM:
            self.sign *= -1
            return

        for i in range(len(self.digits)):
            self[i] = self.base - 1 - self[i]
         
        if self.repr == Repr.RC:
            self += 1

    def __str__(self) -> str:
        return ('-' if self.sign == -1 else '') + ''.join([INT_TO_DIGIT[i] for i in reversed(self.digits)])
    
    def __int__(self) -> int:

        multiplier = 1
        result = 0

        for digit in self.digits:
            result += digit * multiplier
            multiplier *= self.base

        # We are working with a negative number in
        # systems of complements.
        if self.leading_digit() == self.base - 1:
            result -= multiplier

            if self.repr == Repr.DRC:
                result += 1

        return result * self.sign

    def __iadd__(self, other):
        
        if isinstance(other, Number):

            other.convert_to(self.base, self.repr)

            if self.sign != other.sign:
                other.sign *= -1
                self -= other
                return self

            limit = max(len(self.digits), len(other.digits)) + 1
            result = [0] * limit
            carry = 0

            for i in range(limit):
                sum = self[i] + other[i] + carry
                carry = sum // self.base
                result[i] = sum % self.base

            self.digits = result
            self.strip()

            if self.repr == Repr.DRC and carry != 0:
                self += 1
        else:
            self += Number(other, self.base, self.repr)

        return self

    def __add__(self, other):

        result = deepcopy(self)
        result += other

        return result
    
    def __isub__(self, other):

        if isinstance(other, Number):
             
            other.convert_to(self.base, self.repr)

            # Subtraction in systems of complements is
            # just adding the subtrahend's complement.
            # If our numbers have the same sign after negation,
            # just add them together.
            if self.repr != Repr.SM or self.sign != other.sign:
                self += -other
                return self

            other.sign *= -1
            x = self
            y = other

            # If the subtrahend's absolute value is bigger,
            # subtract
            if abs(int(x)) < abs(int(y)):
                self.sign *= -1
                x = other
                y = self

            limit = max(len(self.digits), len(other.digits))
            result = [0] * limit
            borrow = 0

            for i in range(limit):
                diff = x[i] - y[i] - borrow
                borrow = 1 if diff < 0 else 0
                result[i] = diff % self.base

            self.digits = result
            self.strip()
            
        else:
            self -= Number(other, self.base, self.repr)

        return self   

    def __sub__(self, other):

        result = deepcopy(self)
        result -= other

        return result
    
    def __eq__(self, other):
        
        return int(self) == int(other)
    
    def __ne__(self, other):
        
        return not self.__eq__(other)

    def __lt__(self, other):

        return int(self) < int(other)
    
    def __le__(self, other):

        return int(self) <= int(other)
    
    def __gt__(self, other):

        return int(self) > int(other)
    
    def __ge__(self, other):

        return int(self) >= int(other)

    def __neg__(self):

        self._complement_self()

        return self
    
    def __getitem__(self, index: int) -> int:

        if index >= len(self.digits):
            return self.leading_digit()

        return self.digits[index]
    
    def __setitem__(self, index: int, value: int) -> None:
        self.digits[index] = value