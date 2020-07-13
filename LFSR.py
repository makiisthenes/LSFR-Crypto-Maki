# LSFR Simulation with 4 bits.
# Stream Cipher Random Bit Generation.
import math

# 1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1
# 1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1
# 1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1 B
# 3.402823669209385e+38 2^128 Possible Keys

# 1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1 B
# 68719476735  2^36 Possible Keys

# 1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1  1 1 1 1 B
# 1048575  2^20 Possible Keys

# 1 1 1 1  1 1 1 1  1 1 1 1 B
# 4095D 2^12 Possible Keys

# 1 1 1 1  1 1 1 1 B
# 255D 2^8 Possible Keys


def decimal2binary(decimal_value):
    output = "{0:b}".format(decimal_value)
    # Max Length 4 bits.
    if len(output) != 8:
        binary_padding = 8 - len(output)
        output = (binary_padding * '0')+ output
    return output

def int_split(output):
    bit1 = int(str(output[0]))
    bit2 = int(str(output[1]))
    bit3 = int(str(output[2]))
    bit4 = int(str(output[3]))
    bit5 = int(str(output[4]))
    bit6 = int(str(output[5]))
    bit7 = int(str(output[6]))
    bit8 = int(str(output[7]))
    bits = (bit1, bit2, bit3, bit4, bit5, bit6, bit7, bit8)
    return bits

def iterate(register):
    bit1 = register[0]
    bit2 = register[1]
    bit3 = register[2]
    bit4 = register[3]
    bit5 = register[4]
    bit6 = register[5]
    bit7 = register[6]
    bit8 = register[7]
    if (bit8 == 1 and bit7 == 0) or (bit8 == 0 and bit7 == 1):
        next_bit1 = 1
    else:
        next_bit1 = 0
    next_bit2 = bit1
    next_bit3 = bit2
    next_bit4 = bit3
    next_bit5 = bit4
    next_bit6 = bit5
    next_bit7 = bit6
    next_bit8 = bit7
    random_bit = bit8
    return next_bit1, next_bit2, next_bit3, next_bit4, next_bit5, next_bit6, next_bit7, next_bit8, random_bit

def int_concat(next_bit1, next_bit2, next_bit3, next_bit4, next_bit5, next_bit6, next_bit7, next_bit8, register):
    register = [next_bit1, next_bit2, next_bit3, next_bit4, next_bit5, next_bit6, next_bit7, next_bit8,]
    # full_bit = str(next_bit1) + str(next_bit2) + str(next_bit3) + str(next_bit4)
    # full_bit = int(full_bit)
    return register

def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def frombits(bits):
    chars = []
    for b in range(math.ceil(len(bits) / 8)):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

# Decryption Key is suppose to be generated from the Seed Value rather than using complete key [one time pad].
def decrypt(encrypt_bits, key):
    POSSIBLE_ROUNDS = len(encr_bits)
    key = tobits(key)
    cipher = ''
    for x in range(POSSIBLE_ROUNDS):
        cipher += str((int(key[x]) + int(encrypt_bits[x])) % 2)
    plain_text = frombits(cipher)
    return plain_text, cipher


ITERATION = 0
POSSIBLE_ROUNDS = (2**8)-1


print("This is an simulation for LFSR used in Stream Ciphers, given a seed can output 'random' bits.")
while True:
    plain_text = input("Enter some text to encrypt: ")
    encr_bits = tobits(plain_text)  # Encryption Bit List
    print("Length in bits of plaintext: " + str(len(encr_bits)))
    POSSIBLE_ROUNDS = len(encr_bits)
    seed = int(input("[Seed] Enter a integer number from 0 to 255:: "))
    output = decimal2binary(seed)
    print(output)
    next_bit1, next_bit2, next_bit3, next_bit4, next_bit5, next_bit6, next_bit7, next_bit8, = int_split(output)
    register = [next_bit1, next_bit2, next_bit3, next_bit4, next_bit5, next_bit6, next_bit7, next_bit8,]
    random_bits = []
    string = ''
    for x in range(POSSIBLE_ROUNDS):
        next_bit1, next_bit2, next_bit3, next_bit4, next_bit5, next_bit6, next_bit7, next_bit8, random_bit = iterate(register)
        random_bits.append(random_bit)
        string += str(random_bit)
        register = int_concat(next_bit1, next_bit2, next_bit3, next_bit4, next_bit5, next_bit6, next_bit7, next_bit8, register)
    print("Random Bits Generated")
    # print(random_bits)  # List
    print("Key Generated in bits: " + string)
    print("Key Generated: " + frombits(string))

    # Encrypting Bits with Bits Generated from seed.
    ciphertext = ''
    for x in range(len(random_bits)):
        ciphertext += str((random_bits[x] + encr_bits[x]) % 2)  # mod2 operation
    print("Ciphertext: " + ciphertext)
    print("Encrypted Message: " + frombits(ciphertext))
    key = input("To Decrypt " + frombits(ciphertext) + " enter key:: ")
    if key:
        output, cipher = decrypt(ciphertext, key)
        print("Original Bits was: " + cipher)
        print("Original Message was: " + output)
