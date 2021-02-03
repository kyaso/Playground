w = 32
msk = 2**w - 1

def ROTR(x, n):
    return msk&((x>>n) | (x<<(w-n)))

def SHR(x, n):
    return x>>n

def Ch(x, y, z):
    return (x & y) ^ (msk&(~x) & z)

def Maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def bigSig0(x):
    return ROTR(x,2) ^ ROTR(x,13) ^ ROTR(x,22)

def bigSig1(x):
    return ROTR(x,6) ^ ROTR(x,11) ^ ROTR(x,25)

def smlSig0(x):
    return ROTR(x,7) ^ ROTR(x,18) ^ SHR(x,3)

def smlSig1(x):
    return ROTR(x,17) ^ ROTR(x,19) ^ SHR(x,10)

# --------------------------------------------------
def pad_msg(msg: list, block_len=512):
    """
    msg: Message expressed as list of bytes

    block_len: Message block length in bits

    Returns: The padded message (list of bytes)
    """
    # Determine length of message in bits
    l = len(msg) * 8

    # --- Determine k (number of zero bits in padding)
    # How many bits until next multiple of `block_len`
    tmp = block_len - l%block_len
    
    # If tmp < 65, we cannot fit the '1' and 64-bit length in the current padding.
    # --> Add more padding space by going to the next multiple until it eventually fits
    while tmp < 65:
        tmp += block_len
    
    # k is simply total padding minus bits for '1' and 64-bit length field
    k = tmp - 65

    # Start constructing left part ('1' + k*'0') of padding.
    # Appending k zero bits after the '1' is equivalent to shifting
    # it by k to the left.
    pad = 1<<k

    # Append length of message
    pad = pad<<64 | l

    # Get length of padding bytes
    pad_len_bits = 1+k+64
    pad_len = int(pad_len_bits / 8)

    # Now append bytes of padding to the msg list, by each time shifting left
    # and selecting the most-sig byte of pad.
    mask = 0xFF<<(pad_len_bits-8)
    for _ in range(0, pad_len):
        msg.append((pad&mask)>>(pad_len_bits-8))
        pad <<= 8
    
    return msg

def parse_msg(msg: list, block_len=512):
    """
    Parses a message.

    msg: List of message bytes.

    block_len: Length of message block in bits.

    Returns: Generator for retrieving a message block (list of `block_len`/32 32-bit words)
    """
    if (len(msg)*8)%block_len != 0:
        raise Exception("Message is not multiple of {} bits!".format(block_len))

    # Convert message to list of 32-bit words
    tmp = [msg[i]<<24 | msg[i+1]<<16 | msg[i+2]<<8 | msg[i+3]  for i in range(0, len(msg), 4)]

    # Build a generator that returns one message block at a time
    # message block = list of `block_len`/32 32-bit words
    words_per_block = int(block_len/32)
    for i in range(0, len(tmp), words_per_block):
        yield tmp[i:i+words_per_block]

def msg_schedule(msg: list):
    """
    msg: Message block (list of 16 32-bit words)

    Returns: Schedule for message `msg` (list of 64 32-bit words)
    """
    W = []

    # 0 <= t <= 15
    for t in range(0,16):
        W.append(msg[t])
    
    # 16 <= t <= 63
    for t in range(16, 64):
        val = msk&(smlSig1(W[t-2]) + W[t-7] + smlSig0(W[t-15]) + W[t-16])
        W.append(val)
    
    return W

def sha256(msg: list):
    """
    Compute the SHA-256 value of msg

    msg: The message as a list of bytes
    """
    # Constants
    K = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
         0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
         0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
         0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
         0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
         0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
         0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
         0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2]

    # Initial hash value
    H = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]
    
    # Pad message
    block_len = 512
    msg = pad_msg(msg)

    # Parse message
    msg_parsed = parse_msg(msg)

    # SHA loop
    # Iterator over message blocks
    for m in msg_parsed:
        # Prepare message schedule
        W = msg_schedule(m)

        # Initialize working vars
        a = H[0]
        b = H[1]
        c = H[2]
        d = H[3]
        e = H[4]
        f = H[5]
        g = H[6]
        h = H[7]
        
        # Inner loop
        for t in range(0,64):
            T1 = msk&(h + bigSig1(e) + Ch(e,f,g) + K[t] + W[t])
            T2 = msk&(bigSig0(a) + Maj(a,b,c))
            h = g
            g = f
            f = e
            e = msk&(d + T1)
            d = c
            c = b
            b = a
            a = msk&(T1 + T2)

        # Compute new hash value
        H[0] = msk&(a + H[0])
        H[1] = msk&(b + H[1])
        H[2] = msk&(c + H[2])
        H[3] = msk&(d + H[3])
        H[4] = msk&(e + H[4])
        H[5] = msk&(f + H[5])
        H[6] = msk&(g + H[6])
        H[7] = msk&(h + H[7])
    
    # Return final digest
    return (H[0]<<224 | H[1]<<192 | H[2]<<160 | H[3]<<128 | H[4]<<96 | H[5]<<64 | H[6]<<32 | H[7])