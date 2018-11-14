import bisect


def InvertedIndex(docs, index=None, docno_to_id=None):
    if index is None and docno_to_id is None:
        index, docno_to_id = {}, {}
        curr_id = 0

    else:
        curr_id = max(docno_to_id.keys()) + 1

    for doc in docs:
        docno_to_id[curr_id] = doc.docno

        for term, cnt in doc.tf.items():
            term_dict = index.get(term, {'df': 0, 'posting_list': []})
            bisect.insort(term_dict['posting_list'], curr_id)
            term_dict['df'] += cnt
            index[term] = term_dict

        curr_id += 1

    return (index, docno_to_id)
