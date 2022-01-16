import re

MIN_ORD = ord("A")
ORD_SCALE = ord("Z") - MIN_ORD

# Rate of decline in how much each subsequent character can shift the output
# Example:
# - [round(0.9 ** i, 2) for i in range(10)]
# - [1.0, 0.9, 0.81, 0.73, 0.66, 0.59, 0.53, 0.48, 0.43, 0.39]
DECAY_RATE = 0.9

# This defines a function to take any English text as an input and deterministically output a psuedorandom real value from [0.0-1.0)
# Meant to favor simplicity over cryptographic correctness
# Longer text inputs will result in evenly distributed and finer grained values
# Only cares about A-Z characters, case insensitive
def text_to_float(text):
    norm_text = re.sub("[^A-Z]", "", text.upper())
    
    output = 0.0

    for index, char in enumerate(norm_text):
        # Base value is scaled from 0.0 (A) to 1.0 (Z)
        base_shift = float(ord(char) - MIN_ORD) / ORD_SCALE

        # Scaled value is shifted downward for characters later on in the text
        scaled_shift = base_shift * (DECAY_RATE ** index)

        # Then, we add this to the output and the use mod 1.0 to keep it within the output range
        # (Note that this means that for just 1 character, both A and Z will output 0.0)
        output = (output + scaled_shift) % 1.0
    
    return output