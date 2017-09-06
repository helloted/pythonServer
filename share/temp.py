
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

if __name__ == '__main__':
    # decode_gzip(a)
    do = zlib.decompressobj(16 + zlib.MAX_WBITS)
    new = str(str_u)
    new = base64.b64decode(a)
    d = do.decompress(new)
    print d
