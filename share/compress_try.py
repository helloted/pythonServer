
import StringIO
import gzip
import base64
import zlib

def decode_gzip(com_str):
    data = bytes(com_str)
    compressedstream = StringIO.StringIO(str.encode(com_str))
    gzipper = gzip.GzipFile(fileobj=compressedstream)
    data = gzipper.read()
    print data

str_u = u'H4sIAAAAAAAAALVUTW/bMAz9Lz7nQJEU5eRmWzaw44DdhqEwlgwN0KZY1u5S9L/vUUqWD7Qohm1h\nZFk0+fREkXxuPqybVZBFs54f55vbebe+2zSrz89l3ayakHkiokBd6DkQ8TuiopNmjcoxxiV1V9+i\njlEja9CBKZIGvPf4kl3jOh3gShJgn30WkXCJci5RYY9ZSFqJsCYxjIS3ItS5L3U62sQj7CVp4hSt\nPyJIV3ixCnCy0EEYOFHUMXhSU6MuqiUb3sIAT/hrgD4Bh8W5J3akIF3B6/AGHO0tJFA0R54SAzwm\nZjng+MknzFG4xgA7k0Ub4LW0YCO8CoItExf2AQjZljZCU7jZAUP7Et+ljuoxzP9WTrfinFWstckE\nw5niTNd3hRgIDzW+r2v/B0dNHg/EBqlnE3gFv0N5M6Nek0uOyvUmEl/Y/AVirY1yp+1biFccemRE\nNj/ZYDUr/pjDGTbVOjnWlOcjULPnkR1yzZmVe8XKtcjz0bryTHX/GmW7qlZtPVJuw4TsjG7hWKnu\nkosOlZTcv8PoS1/gWrsnCeBBAd2otd4JS1CBy/k6CtU1agbrSKUb1Eqk389jfQdUGKHCDZ2DS+9o\nzcAO94DilHPkCM+yP11yAqscjUJTu+exk259tkXzsF9v9p+29+inIKM4dQwtdls03/forMboqv7H\nj08G39Zf5ySA/LF71+jly6K5nX9uPgLvcf+0gdNmv53vbnZP99fOzcsv/KzsDOwFAAA='

a = 'H4sIAAAAAAAAALVUyW4bMQz9lzn7QHGT7dusQI8FeiuKwIAdJEDioG7SS5B/76Nk1wtiBEVb0xqNOOTTE0Xytfm0bpbMs2a9el7d3K2264dNs/z6WtbNskkDT0SUqE0dJyL+QFR00kFN2cwW1F58Mx1NjTVpz2SkCe8dvgyhCZ32cCVJsB9iFpF0jnIqprDHLCRzMViTOEbGWxFqw5daHX3iEfaSNXM27w4I0hZerAKcQWgvDBwTDQye1NWpNfXs/TUM8IS/JugzcFiCe+ZAStIWvBZvwNHOUwZFD+QpM8AtM8seJ04+YTbhGgPsTG7ew2vhyUd4FQRfZC7sExAGX/gITeHmewztSnwXOmrEcPi3cryV4Kzic59cMIIpznR5V4iBcF/j+772f3DUHPFAbJB6PoFXijuUqxn1npxzVK43kfnM5i8Qa22UO51fQ7zg0CEjBo+T9V6z4o85nGBTrZNDTUU+AnWIPPJ9rgWzcq9YhRZ5PnpbnrnuX6PsF9Wq84hU2DAhOy0sAivXXYaiQyXl8G8xutIXuNbuURJ4UEI3mnsXhCWpwOV0bUJ1jZrB2qh0g1qJ9Pt5qO+ECiNUuKNzoPhRkLB2Rx27ZD9DNniW/emcE1gN5pSa2j0PnfQ+Zps1T7v1Zvfl/hH9FGTU52oZ50yz5vsOndUZXTX++PHRwG/F8y0gf2w/NHr7NmvuVj83n4H3vHvZwGmzu1893GxfHi+dm7dfaanF9OwFAAA='

pre = '31 -117 8 0 0 0 0 0 0 0 -115 -110 77 111 -126 64 16 -122 -17 -4 -118 55 105 122 106 41 -69 40 106 -72 1 -47 126 -128 74 116 -101 -90 -57 81 54 -126 124 104 22 56 -8 -17 -69 34 7 -101 104 -30 123 -102 -20 60 59 59 -17 -52 34 88 -50 -89 -2 -9 -81 -127 78 -63 116 33 86 94 -124 -40 91 -123 -104 123 81 -124 72 -128 -61 4 31 -16 30 -71 72 68 49 -40 -60 -31 108 -60 -58 92 -53 48 22 -121 55 -84 27 -43 -26 -25 -76 -117 -64 15 98 -109 105 -39 -93 -111 51 -32 -42 108 102 -120 93 113 77 48 -57 92 -53 -93 105 51 62 -122 -51 92 -57 113 25 55 66 -86 107 -78 -106 42 -111 -22 73 51 28 22 -58 -74 126 -33 -120 101 65 39 -86 44 13 100 -54 -123 -105 -108 89 -107 -43 -115 34 77 -124 -34 -22 115 -31 25 -26 -125 -22 -116 112 -8 -19 102 83 72 -52 -77 34 -121 -112 4 -40 -61 87 -35 111 103 -17 18 -10 -114 95 -80 54 29 -10 -116 -1 98 87 97 95 49 58 109 83 41 -15 -43 102 91 -119 31 -21 86 -59 -121 123 124 87 84 37 -30 -48 80 -95 -57 112 83 -61 73 87 -47 -41 99 81 -105 -109 59 -96 -61 122 51 1 -43 -23 53 -40 39 66 89 110 -88 -56 -88 -70 91 1 118 7 118 54 -123 84 89 73 -56 -11 30 82 80 67 53 -14 -74 -38 -73 -43 78 -33 -41 45 83 63 -76 15 82 59 66 -35 38 -108 -94 -111 -86 -84 -11 -38 -113 -76 -89 28 -79 -81 127 -53 89 127 -77 6 -92 -24 124 2 0 0'



def de_compress():
    do = zlib.decompressobj(16 + zlib.MAX_WBITS)
    new = base64.b64decode(a)


    d = do.decompress(new)
    print d

    # gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
    # gzip_data = gzip_compress.compress('hello') + gzip_compress.flush()
    # print gzip_data,type(gzip_data),len(gzip_data)
    #
    # print zlib.decompress(gzip_data, zlib.MAX_WBITS|16)


def new_de_code():
    gzip_compress = zlib.compressobj(9, zlib.DEFLATED, zlib.MAX_WBITS | 16)
    gzip_data = gzip_compress.compress('hello') + gzip_compress.flush()
    print gzip_data,type(gzip_data),len(gzip_data)
    print zlib.decompress(bytes(pre), zlib.MAX_WBITS|16)

if __name__ == '__main__':
    new_de_code()




