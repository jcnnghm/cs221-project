import json

if __name__ == '__main__':
    test_movie_ids = json.load(open('data/test.json'))
    data = json.load(open('data/features.json'))

    data_to_submit = {}
    for movie_id in test_movie_ids:
        data_to_submit[movie_id] = data[str(movie_id)]

    with open('data/data.json', 'w') as outfile:
        outfile.write(json.dumps(data_to_submit, indent=4, encoding="utf-8"))