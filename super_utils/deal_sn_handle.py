import hashlib, time, datetime
from device_server.utils.comment import b64_aes_dec, aes_enc_b64
from redis_manager import r_deal_sn

def get_md5(s):
    s = s.encode('utf8') if isinstance(s, unicode) else s
    m = hashlib.md5()
    # m.update(s)
    return m.hexdigest()

code_map = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
    'y', 'z', '0', '1', '2', '3', '4', '5',
    '6', '7', '8', '9', 'A', 'B', 'C', 'D',
    'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z'
)


def get_hash_key(long_url):
    hkeys = []
    hex = hashlib.md5(long_url).hexdigest()
    for i in xrange(0, 4):
        n = int(hex[i * 8:(i + 1) * 8], 16)
        v = []
        e = 0
        for j in xrange(0, 5):
            x = 0x0000003D & n
            e |= ((0x00000002 & n) >> 1) << j
            v.insert(0, code_map[x])
            n = n >> 6
        e |= n << 5
        v.insert(0, code_map[e & 0x0000003D])
        hkeys.append(''.join(v))
    return hkeys[0]


def product_sn(device_sn):
    time_str = str(int(time.time())) + str(datetime.datetime.now().microsecond)
    text = device_sn + 'seed' + time_str
    base = aes_enc_b64(text)
    hah = hashlib.sha1(base).hexdigest()
    return hah


def handel_sn(device_sn):
    deal_sn = product_sn(device_sn)
    short_sn = get_hash_key(deal_sn)

    url = 'http://www.qotaku.com' + '/'+short_sn

    # r_deal_sn.set(short_sn,deal_sn)

    dict = {}
    dict['url'] = url
    dict['deal_sn'] = deal_sn
    return dict



