from enum import Enum

# A dictionary mapping characters representing digits ('0' to '9' and 'A' to 'Z')
# to their corresponding integer values from 0 to 35.
DIGIT_TO_INT = {chr(i + ord('0')) if i < 10 else chr(i - 10 + ord('A')) : i for i in range(36)}

# A dictionary mapping integer values from 0 to 35 to 
# their corresponding characters representing digits ('0' to '9' and 'A' to 'Z').
INT_TO_DIGIT = {i : chr(i + ord('0')) if i < 10 else chr(i - 10 + ord('A')) for i in range(36)}

class Repr(Enum):
    """
    How a number is represented aside from the numbers base.
    """

    SIGN_MAGNITUDE = 0,
    DIMINSHED_RADIX_COMPLEMENT = 1,
    RADIX_COMPLEMENT = 2

class Number:

    def __init__(self, number: str, base: int, repr: Repr):

        self.sign = -1 if number[0] == '-' else 1
        self.digits = [DIGIT_TO_INT[c] for c in reversed(number.strip(' -+'))]
        self.base = base
        self.repr = repr

    def convert_to(self, base: int, repr: Repr) -> 'Number':
        """
        Returns a number with the same value, but
        in a different specified base and representation.
        """

        if (self.base, self.repr) == (base, repr):
            return self
        
        magnitude = abs(int(self))
        negative = self.is_negative()
        number = Number("+", base, repr)

        while magnitude != 0:
            number.digits.append(magnitude % base)
            magnitude //= base

        if repr == Repr.SIGN_MAGNITUDE:
            number.sign = -1 if negative else 1
            return number

        number.digits.append(0)
        number.strip()

        return number if not negative else number.complement()
    
    def complement(self) -> 'Number':
        """
        Returns the complement of this number.
        """

        if self.repr == Repr.SIGN_MAGNITUDE:
            return
        
        comp = Number('+', self.base, self.repr)

        # Complement all of our digits. We do this by subtracting
        # the digit at position i from the highest digit.
        for digit in self.digits:
            comp.digits.append(comp.base - digit - 1)

        # Add 1 to get the right number in radix complement.
        if comp.repr == Repr.RADIX_COMPLEMENT:
            comp = add(comp, Number('01', comp.base, comp.repr), comp.base, comp.repr)
        
        return comp


    def is_negative(self) -> bool:

        if self.repr == Repr.SIGN_MAGNITUDE:
            return self.sign == -1
        
        # In systems of complements, numbers are negative if the most
        # significant digit is a negative one. The first (base // 2) digits
        # are positive, the rest are negative. Odd bases have a neutral digit
        # which is equal to (base // 2) and we can't determine the sign if it's
        # the most significant bit.
        mid_point = self.base // 2
        lowest_neg_digit = mid_point + 1 if self.base % 2 == 1 else mid_point

        # For numbers that have an odd base, we might have to check
        # more than one digit to determine if it's a negative number.
        # eg. 314, base 7 - positive.
        # eg. 352, base 7 - negative.
        # ..333..333, base 7 - undefined.
        for digit in reversed(self.digits):

            if digit >= lowest_neg_digit:
                return True
            elif digit < mid_point:
                return False

    def strip(self) -> None:
        """
        Remove excess digits so this number is represented
        with the least amount of digits.
        """

        i = len(self.digits) - 1
        mid_point = self.base // 2
        lowest_neg_digit = mid_point + 1 if self.base % 2 == 1 else mid_point

        while i >= 1:

            if self.repr == Repr.SIGN_MAGNITUDE and self[i] == 0:
                self.digits.pop()
            elif self.repr != Repr.SIGN_MAGNITUDE and self[i] == self.base - 1 and self[i-1] >= lowest_neg_digit:
                self.digits.pop()
            elif self.repr != Repr.SIGN_MAGNITUDE and self[i] == 0 and self[i-1] < mid_point:
                self.digits.pop()
            else:
                break

            i -= 1

    def __str__(self) -> str:
        return ('-' if self.sign == -1 else '') + ''.join([INT_TO_DIGIT[i] for i in reversed(self.digits)])
    
    def __int__(self) -> int:

        multiplier = 1
        result = 0

        for digit in self.digits:
            result += digit * multiplier
            multiplier *= self.base

        if self.repr == Repr.SIGN_MAGNITUDE:
            return result * self.sign

        if self.is_negative():
            result -= multiplier

            if self.repr == Repr.DIMINSHED_RADIX_COMPLEMENT:
                result += 1

        return result

    def __eq__(self, other):
        
        if isinstance(other, Number):
            return int(self) == int(other)
        
        return False
    
    def __ne__(self, other):
        
        return not self.__eq__(other)

    def __getitem__(self, index: int) -> int:

        # Determine the leading digits.
        if index >= len(self.digits):

            if self.repr == Repr.SIGN_MAGNITUDE:
                return 0
            
            # Negative numbers in system of complemenets have leading highest digits.
            return self.base - 1 if self.is_negative() else 0

        return self.digits[index]
    
    def __setitem__(self, index: int, value: int) -> None:
        self.digits[index] = value
    
def add(x: Number, y: Number, base: int, repr: Repr, limit: int = 1e9) -> Number:
    
    result = Number("+", base, repr)
    x = x.convert_to(base, repr)
    y = y.convert_to(base, repr)
    limit = min(limit, max(len(x.digits), len(y.digits)) + 1)
    carry = 0

    for i in range(limit):
        sum = x[i] + y[i] + carry
        carry = sum // base
        result.digits.append(sum % base)

    result.strip()

    if repr == Repr.DIMINSHED_RADIX_COMPLEMENT and carry != 0:
        result = add(result, Number('01', base, repr), base, repr, limit)

    return result


def sub(x: Number, y: Number, base: int, repr: Repr, limit: int = 1e9) -> Number:

    x = x.convert_to(base, repr)
    y = y.convert_to(base, repr)

    # Subtracting with a number in systems of complements is 
    # the same as adding it's complement.
    if repr != Repr.SIGN_MAGNITUDE:
        return add(x, y.complement(), base, repr, limit)
     
    result = Number('0', base, repr)
    limit = min(limit, max(len(x.digits), len(y.digits)))
    borrow = 0

    if int(y) > int(x):
        x, y = y, x
        result.sign = '-'

    for i in range(limit):
        diff = x[i] - y[i] - borrow
        borrow = 1 if diff < 0 else 0
        result.digits.append(diff % base)

    return result