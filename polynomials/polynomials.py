import enum
from numbers import Number, Integral


class Polynomial:

    def __init__(self, coefs):
        self.coefficients = coefs

    def degree(self):
        return len(self.coefficients) - 1

    def __str__(self):
        coefs = self.coefficients
        terms = []

        if coefs[0]:
            terms.append(str(coefs[0]))
        if self.degree() and coefs[1]:
            terms.append(f"{'' if coefs[1] == 1 else coefs[1]}x")

        terms += [f"{'' if c == 1 else c}x^{d}"
                  for d, c in enumerate(coefs[2:], start=2) if c]

        return " + ".join(reversed(terms)) or "0"

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.coefficients) + ")"

    def __eq__(self, other):

        return isinstance(other, Polynomial) and\
             self.coefficients == other.coefficients

    def __add__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a + b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + other.coefficients[common:]

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] + other,)
                              + self.coefficients[1:])

        else:
            return NotImplemented

    def __neg__(self):
        return Polynomial(tuple(-c for c in self.coefficients))

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):

        if isinstance(other, Polynomial):
            coefs = [0 for i in range(self.degree() + other.degree() + 1)]
            for i, c in enumerate(self.coefficients):
                for j, d in enumerate(other.coefficients):
                    coefs[i + j] += c * d

            return Polynomial(tuple(coefs))

        elif isinstance(other, Number):
            if other:
                return Polynomial(tuple(c * other for c in self.coefficients))
            else:
                return Polynomial((0,))
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self * other

    def __pow__(self, other):

        if isinstance(other, Integral) and other > 0:
            p = Polynomial(self.coefficients)
            for i in range(other - 1):
                p = p * self
            return p

        else:
            return NotImplemented

    def __call__(self, x):
        return sum(c * x ** i for i, c in enumerate(self.coefficients))

    def dx(self):
        if self.degree():
            return Polynomial(tuple(i * c for i, c in enumerate(self.coefficients[1:], start=1)))
        else:
            return Polynomial((0,))

def derivative(p):
    """Returns the derivative of a polynomial."""
    return p.dx()
