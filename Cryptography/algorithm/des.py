#!/usr/bin/python3
# Name: des.py
# Initial/Final Permutation Table

IPT = [58, 50, 42, 34, 26, 18, 10, 2,
       60, 52, 44, 36, 28, 20, 12, 4,
       62, 54, 46, 38, 30, 22, 14, 6,
       64, 56, 48, 40, 32, 24, 16, 8,
       57, 49, 41, 33, 25, 17, 9, 1,
       59, 51, 43, 35, 27, 19, 11, 3,
       61, 53, 45, 37, 29, 21, 13, 5,
       63, 55, 47, 39, 31, 23, 15, 7]

FPT = [40, 8, 48, 16, 56, 24, 64, 32,
       39, 7, 47, 15, 55, 23, 63, 31,
       38, 6, 46, 14, 54, 22, 62, 30,
       37, 5, 45, 13, 53, 21, 61, 29,
       36, 4, 44, 12, 52, 20, 60, 28,
       35, 3, 43, 11, 51, 19, 59, 27,
       34, 2, 42, 10, 50, 18, 58, 26,
       33, 1, 41, 9, 49, 17, 57, 25]

def plain2bitstring(plain: str):
    return "".join(format(ord(c), "0>8b") for c in plain)
  
def plain2bitarray(plain: str):
    bitstring = plain2bitstring(plain)
    encoded = bytearray([int(b) for b in bitstring])
    return encoded
  
def bitarray2plain(bitarray: bytearray):
    bitstring = bitarray2bitstring(bitarray)
    encoded = "".join([chr(int(bitstring[i*8:i*8+8], 2))
                       for i in range(len(bitstring)//8)])
    return encoded
  
def bitarray2bitstring(bitarray: bytearray):
    return "".join([str(b) for b in bitarray])
  
def permutation(block: bytearray, table: list[int], outlen: int):
    permutated = bytearray(outlen)
    for n in range(len(table)):
        m = table[n]-1
        permutated[n] = block[m]
    return permutated
  
plain = "DEScrypt"
key = "DREAMCRY"
bitarray = plain2bitarray(plain)
print(f"bitstring of '{plain}': {bitarray2bitstring(bitarray)}")

# Initial permutation
initial_permutated = permutation(bitarray, IPT, 64)
print(
    f"bitstring of initial_permutated: {bitarray2bitstring(initial_permutated)}")

# Final permutation
final_permutated = permutation(initial_permutated, FPT, 64)
print(f"bitstring of final_permutated: {bitarray2bitstring(final_permutated)}")

# plain == FP(IP(plain)) => FP = IP^{-1}
print(f"plaintext of final_permutated: {bitarray2plain(final_permutated)}")
