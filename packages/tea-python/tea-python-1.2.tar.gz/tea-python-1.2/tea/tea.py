"""
Copyright 2022-2022 The gumy Authors. All rights reserved.
tea 加密
Authors: gumy <ojbk@live.com>
"""

import struct


def encrypt(data: bytes, key: bytes):
    data_len = len(data)
    if data_len % 8 != 0:
        return None
    num = data_len >> 3
    encrypt_data = bytes()
    delta = 0x9e3779b9
    op = 0xffffffff

    for i in range(num):
        y, z = struct.unpack('2I', data[i * 8:(i + 1) * 8])
        a, b, c, d = struct.unpack('4I', key)
        s = 0

        for j in range(32):
            s += delta
            s &= op
            y += (op & (z << 4) + a) ^ (z + s) ^ (op & (z >> 5) + b)
            y &= op
            z += (op & (y << 4) + c) ^ (y + s) ^ (op & (y >> 5) + d)
            z &= op

        encrypt_data += struct.pack('2I', y, z)

    return encrypt_data


def decrypt(data: bytes, key: bytes):
    data_len = len(data)
    if data_len % 8 != 0:
        return None
    num = data_len >> 3
    origin_data = bytes()
    delta = 0x9e3779b9
    op = 0xffffffff

    for i in range(num):
        y, z = struct.unpack('2I', data[i * 8:(i + 1) * 8])
        a, b, c, d = struct.unpack('4I', key)
        s = (delta << 5) & op

        for j in range(32):
            z -= (op & (y << 4) + c) ^ (y + s) ^ (op & (y >> 5) + d)
            z &= op
            y -= (op & (z << 4) + a) ^ (z + s) ^ (op & (z >> 5) + b)
            y &= op
            s -= delta
            s &= op

        origin_data += struct.pack('2I', y, z)

    return origin_data
