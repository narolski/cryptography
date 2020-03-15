from functools import reduce
from math import gcd

class LCGAttacks:
    """
    Attacks used to predict the outputs of linear congruential generator when used as a random number generator.
    """

    def compute_state(self, previous_state : int, multiplier : int, increment : int, modulus : int):
        """
        Returns the value that will be returned by the LCG,
        knowing its previous state, multiplier and modulus.
        :return: LCG state
        """
        return (previous_state * multiplier + increment) % modulus


    def compute_increment(self, states : tuple, multiplier : int, modulus : int):
        """
        Returns the unknown increment used by the LCG,
        knowing its multiplier, modulus and previous two states.
        As we know that s_1 = s_0 * m + c (mod n),
        the increment c = s_1 - s_0 * m (mod n).
        :return: increment
        """
        return (states[1] - states[0] * multiplier) % modulus


    def compute_multiplier(self, states: tuple, modulus : int):
        """
        Returns the unknown multplier used by the LCG,
        knowing only its modulus.
        As we know that:
        s_1 = s_0 * m + c (mod n), and
        s_2 = s_1 * m + c (mod n)
        we find the multiplier by solving:
        s_2 - s_1 = s_1 * m - s_0 * m (mod n)
        m = (s_2 - s_1) / (s_1 - s_0) (mod n)
        :return: multiplier
        """
        return (states[2] - states[1]) * self.modinv(states[1] - states[0], modulus) % modulus


    def compute_modulus(self, states : tuple):
        """
        Returns the unknown modulus used by the LCG,
        knowing only its modulus.
        As we know that:
        - It is highly probable that, having random
          multiplies of n, their GCD will be n
        - Having X = 0 (mod n) means, that X = k * n
          (that is, X != 0, but X = 0 (mod n))
        we find the modulus by introducing 
        a time sequence T(n) = S(n+1) - S(n),
        computing first four time steps:
        t_0 = s_1 - s_0
        t_1 = s_2 - s_1 = (s_1 * m + c) - (s_0 * m + c) = m * (s_1 - s_0) = m * t_0 (mod n)
        t_2 = s_3 - s_2 = (s_2 * m + c) - (s_1 * m + c) = m * (s_2 - s_1) = m * t_1 (mod n)
        and solving for zero:
        t_2 * t_0 - t_1 * t_1 = ([m * m * t_0] * t_0) - (m * t_0 * m * t_0) = 0 (mod n)
        :return: modulus
        """
        diffs = [s_1 - s_0 for s_0, s_1 in zip(states, states[1:])] # zips (s_0, s_1), (s_1, s_2), etc.
        zeroes = [t_2 * t_0 - t_1 * t_1 for t_0, t_1, t_2 in zip(diffs, diffs[1:], diffs[2:])]
        modulus = abs(reduce(gcd, zeroes))
        return modulus


    def modinv(self, b : int, n : int):
        """
        Implements the modular inverse.
        """
        g, x, _ = self.egcd(b, n)
        if g == 1: return x % n
        return 0

    
    def egcd(self, a : int, b : int):
        """
        Implements the extended euclidean algorithm used for finding the GCD of a, b.
        """
        if a == 0: return b, 0, 1
        g, x, y = self.egcd(b % a, a)
        return g, y - (b // a) * x, x
