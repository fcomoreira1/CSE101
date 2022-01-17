import cmath
import math

def next_power_of_2(x):
    return 1 if x == 0 else 2**math.ceil(math.log2(x))

def fft(pol, deg, inverse) -> list:
    if deg == 1:
        return pol
    w = cmath.exp(2*cmath.pi*complex(0,1)/deg * (-1 if inverse else 1))
    p1, p2 = fft(pol[0::2], deg//2, inverse), fft(pol[1::2], deg//2, inverse)
    y = [0]*deg
    for i in range(deg//2):
        y[i] = (p1[i] + (w**i) * p2[i])/(2 if inverse else 1)
        y[i + deg//2] = (p1[i] - (w**i) * p2[i])/(2 if inverse else 1)
    return y

def cleancomplex(a):
    if a.real < 10**-5:
        a = complex(0, a.imag)
    if a.imag < 10**-5:
        a = complex(a.real, 0)
    return a

class Polynomial:
    """An object simulating a polynomial function.
    - coeffs: list of coefficients (in order of *increasing* term degree)
    """
    def __init__(self, coeffs):
        self.coeffs = coeffs
    def __repr__(self):
        return f'Polynomial({self.coeffs})'
    def __str__(self):
        terms = []
        for (i, c_i) in enumerate(self.coeffs):
            if c_i != 0:
                terms.append(f'{c_i}*x**{i}')
        return ' + '.join(terms)
    def __add__(self, other):
        sum_pol = []
        for i in range(max(len(self.coeffs), len(other.coeffs))):
            if i >= len(self.coeffs):
                a = 0
            else:
                a = self.coeffs[i]
            if i >= len(other.coeffs):
                b = 0
            else:
                b = other.coeffs[i]
            sum_pol.append(a+b)
        return Polynomial(sum_pol)

    def __mul__(self, other):
        deg = next_power_of_2(len(self.coeffs) + len(other.coeffs))
        pol1 = self.coeffs.copy()
        pol2 = other.coeffs.copy()
        while len(pol1) < deg: pol1.append(0)
        while len(pol2) < deg: pol2.append(0)

        cplx_rep_self = fft(pol1, deg, False)
        cplx_rep_other = fft(pol2, deg, False)

        mult_cplx_rep = [cplx_rep_self[i]*cplx_rep_other[i] for i in range(deg)]
        mult_pol = fft(mult_cplx_rep, deg, True)

        mult_pol_filtered = [cleancomplex(val) for val in mult_pol]
        return Polynomial(mult_pol_filtered)
            

