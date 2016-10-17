from collections import defaultdict
import zlib

import utils

K = 9
SAMPLE_SIZE = 2000


def iter_compress_data(data):
    for item in data[:SAMPLE_SIZE]:
        if 'pull_request' in item:
            continue
        text = "\n".join((item['title'], item['body_text'] or ''))
        number = item['number']
        if len(text) < K:
            print('Ignoring issue %s' % number)
            continue
        yield number, text.replace('\n', ' ')


def get_shingles(text):
    shingles = set()
    for i in range(0, len(text) - K + 1):
        #shingles.add(text[i:i + K])
        shingles.add(zlib.adler32(text[i:i + K].encode()) & 0xffffffff)
    return shingles


def similarity(shingle1, shingle2):
    return len(shingle1 & shingle2) / len(shingle1 | shingle2)


if __name__ == '__main__':
    data = utils.load_data('./build/pip_issues.data')
    shingles = defaultdict(set)
    for number, text in iter_compress_data(data):
        shingles[number] = get_shingles(text)
    similarities = {}
    for number1 in sorted(shingles):
        for number2 in sorted(shingles):
            if number2 <= number1:
                continue
            similarities[(number1, number2)] = similarity(shingles[number1], shingles[number2])
    ordered_similarities = sorted((s, n) for n, s in similarities.items())
    print(ordered_similarities[:10])
    import ipdb
    ipdb.set_trace()
