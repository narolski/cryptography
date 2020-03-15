class LinearCongruentialGenerator:
    """
    Linear congruential generator used to yield a sequence of pseudo-random numbers.
    """
    m = 672257317069504227  # multiplier
    c = 7382843889490547368 # increment
    n = 9223372036854775783 # modulus

    def __init__(self, seed):
        self.state = seed

    def generate(self):
        self.state = (self.state * self.m + self.c) % self.n
        return self.state