"""Minimal RGBA PNG decode/encode (no PIL on this machine)."""
import struct, zlib

def png_decode(raw):
    pos, idat = 8, b''
    while pos < len(raw):
        ln = struct.unpack('>I', raw[pos:pos + 4])[0]
        tag = raw[pos + 4:pos + 8]
        data = raw[pos + 8:pos + 8 + ln]
        if tag == b'IHDR':
            w, h, bd, ct, _, _, inter = struct.unpack('>IIBBBBB', data)
            assert bd == 8 and ct in (2, 6) and inter == 0
        elif tag == b'IDAT':
            idat += data
        elif tag == b'IEND':
            break
        pos += 12 + ln
    bpp = 4 if ct == 6 else 3
    dat = zlib.decompress(idat)
    stride = w * bpp
    out = bytearray(w * h * 4)
    prev = bytearray(stride)
    p = 0
    for y in range(h):
        ft = dat[p]; p += 1
        line = bytearray(dat[p:p + stride]); p += stride
        if ft == 1:
            for i in range(bpp, stride):
                line[i] = (line[i] + line[i - bpp]) & 255
        elif ft == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 255
        elif ft == 3:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 255
        elif ft == 4:
            for i in range(stride):
                a = line[i - bpp] if i >= bpp else 0
                c = prev[i - bpp] if i >= bpp else 0
                b = prev[i]
                pp = a + b - c
                pa, pb, pc = abs(pp - a), abs(pp - b), abs(pp - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 255
        for x in range(w):
            o = (y * w + x) * 4
            s = x * bpp
            out[o] = line[s]; out[o + 1] = line[s + 1]; out[o + 2] = line[s + 2]
            out[o + 3] = line[s + 3] if bpp == 4 else 255
        prev = line
    return w, h, out

def png_encode(w, h, data):
    raw = bytearray()
    for j in range(h):
        raw.append(0)
        raw += data[j * w * 4:(j + 1) * w * 4]
    def chunk(tag, payload):
        return (struct.pack('>I', len(payload)) + tag + payload +
                struct.pack('>I', zlib.crc32(tag + payload) & 0xffffffff))
    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(bytes(raw), 9))
            + chunk(b'IEND', b''))

