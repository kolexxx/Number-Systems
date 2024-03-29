# Number-Systems
Python package to convert between different bases, work in methods of complements and show a step by step instruction to perfrom arithmetic. 

The intented use of this package is to aid students taking Digital Electronics or Computer Engineering courses by showing them how to perform arithmetic operations in different number systems.

# Example usage
```python
from numsys import *

x = Number(-45, 2) # Convert an integer to a given base.
print(x) # -101101

x.convert_to(2, Comp.RC) # Represent this number in two's complement
print(x) # 1010011

x.convert_to(16, Comp.DRC) # Represent this number in fifteen's complement.
print(x) # D2

y = Number('014', 16, Comp.DRC) # Number twenty in fifteen's complement

result = x + y
print(result) # E6
print(int(result)) # -25
```