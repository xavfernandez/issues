from collections import defaultdict
import itertools
import json
import zlib

import utils

K = 9
SAMPLE_SIZE = 5000


def iter_compress_data(data):
    for item in data[:SAMPLE_SIZE]:
        if 'pull_request' in item:
            continue
        text = "\n".join((item['title'], item['body_text'] or ''))
        number = item['number']
        if len(text) < K:
            print('Ignoring issue %s' % number)
            continue
        yield number, text.replace('\n', ' '), item['closed_at'] is None


def get_shingles(text):
    shingles = set()
    for i in range(0, len(text) - K + 1):
        # shingles.add(text[i:i + K])
        shingles.add(zlib.adler32(text[i:i + K].encode()) & 0xffffffff)
    return shingles


def similarity(shingle1, shingle2):
    return len(shingle1 & shingle2) / len(shingle1 | shingle2)


def compute_similarities(issue_data_filename):
    data = utils.load_data(issue_data_filename)
    shingles = defaultdict(set)
    opened_issues = {}
    for number, text, opened in iter_compress_data(data):
        shingles[number] = get_shingles(text)
        opened_issues[number] = opened
    similarities = defaultdict(dict)
    for number1, number2 in itertools.combinations(shingles, 2):
        if not (opened_issues[number1] or opened_issues[number2]):
            # Don't compute similarities if both are closed
            continue
        similarities[min(number1, number2)][max(number1, number2)] = similarity(shingles[number1], shingles[number2])

    with open('build/similarities.data', 'w') as s:
        json.dump(similarities, s)


def get_similar_issues(symmetric, issue, threshold=0.10):
    similar_issues = sorted([
        (s, n)
        for n, s in symmetric[issue].items()
        if s > threshold
    ], reverse=True)
    return similar_issues

if __name__ == '__main__':
    with open('build/similarities.data') as s:
        similarities = json.load(s)

    symmetric = defaultdict(dict)
    for number1 in similarities:
        for number2 in similarities[number1]:
            symmetric[number1][number2] = similarities[number1][number2]
            symmetric[number2][number1] = similarities[number1][number2]
    get_similar_issues(symmetric, '1234')
    import ipdb
    ipdb.set_trace()
