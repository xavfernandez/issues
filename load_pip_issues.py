from collections import Counter

import matplotlib.pyplot as plt

import utils


global MIN_CREATED_AT


def creation_week(item, min_created_at):
    return (item['created_at'] - min_created_at).days // 7


def close_week(item, min_created_at):
    if item['closed_at'] is None:
        return
    return (item['closed_at'] - min_created_at).days // 7


def output_close_speed_by_week(items, min_created_at):
    created_by_week = Counter(creation_week(item, min_created_at) for item in items)
    closed_by_week = Counter(close_week(item, min_created_at) for item in items)

    max_week = max(max(created_by_week.keys(), closed_by_week.keys()))
    still_opened = 0
    total_opened = 0
    total_closed = 0
    result = []
    for week in range(0, max_week + 1):
        total_opened += created_by_week.get(week, 0)
        total_closed += closed_by_week.get(week, 0)
        still_opened += created_by_week.get(week, 0) - closed_by_week.get(week, 0)
        result.append((week, total_opened, total_closed, still_opened))
    return result


def plot(items, item_type):
    result = output_close_speed_by_week(items, MIN_CREATED_AT)
    weeks = [i[0] for i in result]
    # total_opened = [i[1] for i in result]
    total_closed = [i[2] for i in result]
    still_opened = [i[3] for i in result]

    plt.figure()
    plt.xlabel('Weeks')
    plt.ylabel('Number of %s' % item_type)

    if False:
        plt.title('pip - Open vs closed %s' % item_type.capitalize())
        plt.bar(weeks, total_closed, color='b')
        plt.bar(weeks, still_opened, color='r', bottom=total_closed)
    else:
        plt.title('pip - Open %s' % item_type.capitalize())
        plt.bar(weeks, still_opened, color='r')
    plt.show()


if __name__ == '__main__':
    data = utils.load_data('./build/pip_issues.data')
    MIN_CREATED_AT = min(item['created_at'] for item in data)

    issues = list(filter(lambda item: 'pull_request' not in item, data))
    prs = list(filter(lambda item: 'pull_request' in item, data))
    plot(issues, 'issues')
    plot(prs, 'pull requests')
