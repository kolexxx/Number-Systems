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

class Comp(Enum):
    """
    How a number is represented aside from the numbers base.
    """

    NONE = 0,
    """Sign and magnitude."""
    DRC = 1,
    """Diminshed radix complement."""
    RC = 2
    """Radix complement."""

class Number:

    MAX_DIGITS = -1
    """
    How many digits are allowed to represent a number.
    """

    def __init__(self, input, base: int, comp: Comp = Comp.NONE):

        self._base = base
        self._comp = comp
        
        if isinstance(input, str):
            self._digits_from_str(input)
        elif isinstance(input, int):
            self._digits_from_int(input)
        else:
            raise ValueError('Invalid input. It must be a string or an integer.')

    def convert_to(self, base: int, comp: Comp = Comp.NONE) -> None:
        """
        Returns a number with the same value, but
        in a different specified base and complement.
        """

        if (self._base, self._comp) == (base, comp):
            return
        
        if self._base == base:

            prev = self._comp
            self._comp = comp

            # A positive number is represented the same way
            # in all of our systems.
            if self._sign == 1 and self.leading_digit() == 0:
                return

            if prev == Comp.NONE:

                if self.leading_digit() != 0:
                    self._digits.append(0)
            
                # We are converting a negative number to a system 
                # of complements, so we should find it's complement.
                if self._sign == -1:
                    self._complement_self()
                    self._sign *= -1

                return
            
            # RC's negative numbers are 'larger' by 1 than DRC's.
            if prev == Comp.DRC and comp == Comp.RC:
                self += 1
                return
            
            # DRC's negative numbers are 'smaller' by 1 than RC's.
            if prev == Comp.RC and comp == Comp.DRC:
                self -= 1
                return

        # The most straight-forward way of conversion
        # is first converting the number to an unsigned
        # decimal number, then to our desired base and representation.
        value = int(self)
        self._base = base
        self._comp = comp
        self._digits_from_int(value)

    def complement(self) -> 'Number':
        """
        Returns the complement of this number.
        """
        
        comp = deepcopy(self)
        comp._complement_self()
        
        return comp

    def leading_digit(self) -> int:
        """
        Returns the leading digit of this number. Depending on if
        we're working with complements, it could 0 or the highest digit.
        """

        if self._comp == Comp.NONE:
            return 0
        
        # In systems of complements, numbers are negative if the most
        # significant digit is a negative one. The first (base // 2) digits
        # are positive, the rest are negative. Odd bases have a neutral digit
        # which is equal to (base // 2) and we can't simply determine the sign if it's
        # the most significant digit.
        mid_point = self._base // 2
        lowest_neg_digit = mid_point + 1 if self._base % 2 == 1 else mid_point

        # For numbers that have an odd base, we might have to check
        # more than one digit to determine if it's a negative number.
        # eg. 314, base 7 - positive.
        # eg. 352, base 7 - negative.
        # ..333..333, base 7 - undefined.
        for digit in reversed(self._digits):

            if digit >= lowest_neg_digit:
                return self._base - 1
            elif digit < mid_point:
                return 0
            
        return mid_point

    def strip(self) -> None:
        """
        Remove excess digits so this number is represented
        with the least amount of digits.
        """

        i = len(self._digits) - 1
        mid_point = self._base // 2
        lowest_neg_digit = mid_point + 1 if self._base % 2 == 1 else mid_point

        while i >= 1:

            if self._comp == Comp.NONE and self[i] == 0:
                self._digits.pop()
            elif self._comp != Comp.NONE and self[i] == self._base - 1 and self[i-1] >= lowest_neg_digit:
                self._digits.pop()
            elif self._comp != Comp.NONE and self[i] == 0 and self[i-1] < mid_point:
                self._digits.pop()
            else:
                break

            i -= 1

    def _digits_from_str(self, str: str) -> None:
        """
        Constructs the digits list from a string.
        """
        
        self._sign = -1 if str[0] == '-' else 1
        self._digits = [DIGIT_TO_INT[c.upper()] for c in reversed(str.strip(' -+'))]

        if self._sign == -1 and self._comp != Comp.NONE:
            self._complement_self()

    def _digits_from_int(self, int: int) -> None:
        """
        Constructs the digits list from an integer.
        """

        self._digits = []
        self._sign = 1

        if int < 0:
            self._sign = -1
            int *= -1          

        while True:
            self._digits.append(int % self._base)
            int //= self._base

            if int == 0:
                break

        if self._comp == Comp.NONE:
            return
        
        # Add a leading zero to make sure this number is positive.
        if self.leading_digit() != 0:
            self._digits.append(0)

        # We are dealing with a negative number, complement it.
        if self._sign == -1:
            self._sign = 1
            self._complement_self()           

    def _complement_self(self) -> None:
        """
        Complement this number in place.
        """

        if self._comp == Comp.NONE:
            self._sign *= -1
            return

        for i in range(len(self)):
            self[i] = self._base - 1 - self[i]
         
        if self._comp == Comp.RC:
            self += 1

    def __str__(self, limit: int = 0) -> str:

        if limit == 0:
            limit = len(self._digits)

        return ('-' if self._sign == -1 else '') + ''.join([INT_TO_DIGIT[self[i]] for i in range(limit - 1, -1, -1)])
    
    def __int__(self) -> int:

        multiplier = 1
        result = 0

        for digit in self._digits:
            result += digit * multiplier
            multiplier *= self._base

        # We are working with a negative number in
        # systems of complements.
        if self.leading_digit() == self._base - 1:
            result -= multiplier

            if self._comp == Comp.DRC:
                result += 1

        return result * self._sign

    def __iadd__(self, other):
        
        if isinstance(other, Number):

            other.convert_to(self._base, self._comp)

            if self._sign != other._sign:
                other._sign *= -1
                self -= other
                return self

            limit = Number.MAX_DIGITS if Number.MAX_DIGITS > 0 else max(len(self), len(other)) + 1
            result = [0] * limit
            carry = 0

            for i in range(limit):
                sum = self[i] + other[i] + carry
                result[i] = sum % self._base
                carry = sum // self._base

            self._digits = result
            self.strip()

            if self._comp == Comp.DRC and carry != 0:
                self += 1
        else:
            self += Number(other, self._base, self._comp)

        return self

    def __add__(self, other):

        result = deepcopy(self)
        result += other

        return result
    
    def __isub__(self, other):

        if isinstance(other, Number):
             
            other.convert_to(self._base, self._comp)

            # Subtraction in systems of complements is
            # just adding the subtrahend's complement.
            # If our numbers have the same sign after negation,
            # just add them together.
            if self._comp != Comp.NONE or self._sign != other._sign:
                self += -other
                return self

            other._sign *= -1
            x = self
            y = other

            # If the subtrahend's absolute value is bigger,
            # subtract normally but change the result's sign.
            if abs(int(x)) < abs(int(y)):
                self._sign *= -1
                x = other
                y = self

            limit = max(len(self), len(other))
            result = [0] * limit
            borrow = 0

            for i in range(limit):
                diff = x[i] - y[i] - borrow
                borrow = 1 if diff < 0 else 0
                result[i] = diff % self._base

            self._digits = result
            self.strip()
            
        else:
            self -= Number(other, self._base, self._comp)

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

        return self.complement()
    
    def __getitem__(self, index: int) -> int:

        if index >= len(self):
            return self.leading_digit()

        return self._digits[index]
    
    def __setitem__(self, index: int, value: int) -> None:
        self._digits[index] = value

    def __len__(self) -> int:
        return len(self._digits)