# Pedersen commitment scheme using pairings

from py_ecc.bn128 import (
    G1,         # Generator point in G1 (over FQ)
    G2,         # Generator point in G2 (over FQ2)
    multiply,   # Scalar multiplication of points
    pairing,    # Pairing function e: G2 x G1 -> GT
    add,        # Point addition
    is_on_curve,# Check if a point is on the curve
    b,          # Curve parameter 'b' for the curve over FQ
    b2,         # Curve parameter 'b' for the curve over FQ2
)

# Alice's secret values
a = 2          # Alice's secret scalar 'a'
b_value = 3    # Alice's secret scalar 'b'; renamed to 'b_value' to avoid conflict with curve parameter 'b'

# Trusted setup scalar 's'; chosen during the trusted setup phase
s = 4

# Compute g1_s = s * G1
# This simulates a parameter from the trusted setup in G1
g1_s = multiply(G1, s)

# Compute h1_s = s * G2
# This simulates a parameter from the trusted setup in G2
h1_s = multiply(G2, s)

# Alice creates a commitment to 'a' and 'b_value' using the parameters from the trusted setup
# Mathematical equation:
#   commitment = a * g1_s + b_value * G1
commitment = add(
    multiply(g1_s, a),    # a * g1_s
    multiply(G1, b_value) # b_value * G1
)

# Output G2 and commitment points for verification
print("G2:", G2)
print("Commitment:", commitment)

# Verify that G2 is a valid point on the curve over FQ2 (with parameter b2)
print("G2 valid:", is_on_curve(G2, b2))  # Should be True

# Verify that commitment is a valid point on the curve over FQ (with parameter b)
print("Commitment valid:", is_on_curve(commitment, b))  # Should be True

# ======================================================
# Verification using pairings
# ======================================================

# Our goal is to verify the following equation:
#   e(G2, commitment) == e(h1_s, G1)^a * e(G2, G1)^{b_value}
# This leverages the bilinearity property of pairings:
#   e(P + Q, R) = e(P, R) * e(Q, R)
#   e(c * P, Q) = e(P, Q)^c
#
# Breakdown of the left side:
#   left = e(G2, commitment)
#        = e(G2, a * g1_s + b_value * G1)
#        = e(G2, a * g1_s) * e(G2, b_value * G1)
#        = e(G2, g1_s)^a * e(G2, G1)^{b_value}
#
# Since g1_s = s * G1 and h1_s = s * G2, we have:
#   e(G2, g1_s) = e(G2, s * G1) = e(G2, G1)^s
#   e(h1_s, G1) = e(s * G2, G1) = e(G2, G1)^s
# Therefore:
#   e(G2, g1_s) = e(h1_s, G1)
#
# So, the equation becomes:
#   left = e(h1_s, G1)^a * e(G2, G1)^{b_value}
#
# We'll compute both sides and verify that they are equal.

# Left side: e(G2, commitment)
# Mathematical equation:
#   left = e(G2, commitment)
left = pairing(G2, commitment)

# Compute e(h1_s, G1) = e(s * G2, G1)
# Mathematical equation:
#   e_h1s_G1 = e(h1_s, G1) = e(s * G2, G1) = e(G2, G1)^s
e_h1s_G1 = pairing(h1_s, G1)

# Compute e(G2, G1) as the base pairing value
# Mathematical equation:
#   e_G2_G1 = e(G2, G1)
e_G2_G1 = pairing(G2, G1)

# Right side: e(h1_s, G1)^a * e(G2, G1)^{b_value}
# Mathematical equation:
#   right = e(h1_s, G1)^a * e(G2, G1)^{b_value}
right = (e_h1s_G1 ** a) * (e_G2_G1 ** b_value)

# Verify if left side equals right side
if left == right:
    print("Verification successful: left == right")
else:
    print("Verification failed: left != right")