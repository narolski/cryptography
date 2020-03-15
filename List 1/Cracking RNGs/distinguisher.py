from attacks import LCGAttacks

class LCGDistinguisher:
    """
    Distinguishes linear congruential generator based on pseudo-random values provided.
    """
    attacks = LCGAttacks()

    def __compute_lcg_parameters(self, generator_states : tuple) -> (int, int, int):
        """
        Computes the LCG parameters (multiplier, increment and modulus)
        using the provided outputs from a generator.
        :return: tuple (multiplier, increment, modulus) of computed values.
        """
        n = self.attacks.compute_modulus(generator_states)
        m = self.attacks.compute_multiplier(generator_states, n)
        c = self.attacks.compute_increment(generator_states, m, n)
        return m, c, n
    
    def __compute_expected_output(self, generator_states : tuple, multiplier : int, increment : int, modulus : int) -> int:
        """
        Computes the output that is expected at the next time step
        from the linear congruential generator.
        :return: expected LCG state
        """
        return self.attacks.compute_state(generator_states[-1], multiplier, increment, modulus)

    def is_lcg(self, generator_states : tuple, final_state : int) -> bool:
        """
        Determines whether the output from a generator
        is from a linear congruential generator or a random source,
        having tuple of states (s_0, s_n-1) and final state s_n.
        :return: boolean
        """
        m, c, n = self.__compute_lcg_parameters(generator_states)
        expected = self.__compute_expected_output(generator_states, m, c, n)
        return expected == final_state, expected