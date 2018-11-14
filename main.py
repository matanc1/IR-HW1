import os
import logging
import gc
from docs import docs_from_file
from InvertedIndex import InvertedIndex
from BooleanRetrieval import BooleanRetrieval

logging.basicConfig(format='%(asctime)s:%(message)s', level=logging.DEBUG)

data_path = '/data/HW1/AP_Coll_Parsed'
index, docno_to_id = None, None
files = [filename for filename in os.listdir(data_path) if filename.startswith('AP')]
print('There are {} files overall'.format(len(files)))
for idx, filename in enumerate(files):
    logging.debug('#{} = {}'.format(idx, filename))
    dcs = docs_from_file(os.path.join(data_path, filename))
    (index, docno_to_id) = InvertedIndex(dcs, index, docno_to_id)
    del dcs

queries_path = '/data/HW1/BooleanQueries.txt'
with open(queries_path, 'r') as queries:
    q = [s.replace('\n', '') for s in queries.readlines()]

with open('Part_2.txt', 'w') as f:
    for query in q:
        res = BooleanRetrieval(query, index)
        res = [docno_to_id[val] for val in res]
        f.write(','.join(res))
        f.write('\n')

with open('Part_3.txt', 'w') as f:
    ten_highest = 'Highest: {}'.format(
        str(list(map(lambda x: x[0], sorted(index.items(), key=lambda x: x[1]['df'], reverse=True)[0:10]))))
    ten_lowest = 'Lowest: {}'.format(
        str(list(map(lambda x: x[0], sorted(index.items(), key=lambda x: x[1]['df'], reverse=False)[0:10]))))
    f.write(ten_highest)
    f.write('\n')
    f.write(ten_lowest)
    f.write('\n')
