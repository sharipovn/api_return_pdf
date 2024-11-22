import hashlib


def convert_to_md5(string):
    input_bytes = string.encode('utf-8')
    md5_hash = hashlib.md5(input_bytes).hexdigest()
    print(md5_hash)
    return md5_hash

convert_to_md5('22.11.2024 10:591nuriddin')