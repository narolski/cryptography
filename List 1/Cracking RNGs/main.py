from lcg import LinearCongruentialGenerator
from distinguisher import LCGDistinguisher

import secrets

dist = LCGDistinguisher()

# Verify values from LCG
generator = LinearCongruentialGenerator(7707)
values = tuple(generator.generate() for i in range(0, 11))

res, _ = dist.is_lcg(values[:-1], values[-1])
print("LCG: {}, value: {}".format(res, values[-1]))

# Verify values from Python's secrets
rand_values = tuple(secrets.randbits(20) for i in range(0, 11))

res, _ = dist.is_lcg(rand_values[:-1], rand_values[-1])
print("LCG: {}, value: {}".format(res, rand_values[-1]))