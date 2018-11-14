import pytest
import os
from docs import docs_from_file
from InvertedIndex import InvertedIndex
from BooleanRetrieval import BooleanRetrieval


@pytest.fixture
def index_and_docno_to_id():
    index, docno_to_id = None, None
    dcs = docs_from_file('tests/test_doc')
    (index, docno_to_id) = InvertedIndex(dcs, index, docno_to_id)
    return (index, docno_to_id)


def test_and_query_single_query_no_operator(index_and_docno_to_id):
    (index, docno_to_id) = index_and_docno_to_id[0], index_and_docno_to_id[1]
    query = '( mayor )'
    res = BooleanRetrieval(query, index)
    res = [docno_to_id[val] for val in res]
    assert set(['campaign']) == set(res)


def test_simple_and_query_between_one_doc(index_and_docno_to_id):
    (index, docno_to_id) = index_and_docno_to_id[0], index_and_docno_to_id[1]
    query = '( black AND  campaign )'
    res = BooleanRetrieval(query, index)
    res = [docno_to_id[val] for val in res]
    assert set(['campaign']) == set(res)


def test_simple_and_query_between_two_docs(index_and_docno_to_id):
    (index, docno_to_id) = index_and_docno_to_id[0], index_and_docno_to_id[1]
    query = '( black AND  white )'
    res = BooleanRetrieval(query, index)
    res = [docno_to_id[val] for val in res]
    assert set(['campaign', 'college']) == set(res)


def test_simple_nesting_of_ands_in_one_doc(index_and_docno_to_id):
    (index, docno_to_id) = index_and_docno_to_id[0], index_and_docno_to_id[1]
    query = '( ( black ) AND  ( white ) )'
    res = BooleanRetrieval(query, index)
    res = [docno_to_id[val] for val in res]
    assert set(['campaign', 'college']) == set(res)


def test_simple_nesting_of_ands_in_one_doc2(index_and_docno_to_id):
    (index, docno_to_id) = index_and_docno_to_id[0], index_and_docno_to_id[1]
    query = '( ( black ) AND  white )'
    res = BooleanRetrieval(query, index)
    res = [docno_to_id[val] for val in res]
    assert set(['campaign', 'college']) == set(res)


def test_simple_and_query_in_one_doc(index_and_docno_to_id):
    (index, docno_to_id) = index_and_docno_to_id[0], index_and_docno_to_id[1]
    query = '( mayor AND  white )'
    res = BooleanRetrieval(query, index)
    res = [docno_to_id[val] for val in res]
    assert set(['campaign']) == set(res)


def test_simple_or_query_in_one_doc(index_and_docno_to_id):
    (index, docno_to_id) = index_and_docno_to_id[0], index_and_docno_to_id[1]
    query = '( governor OR campaign )'
    res = BooleanRetrieval(query, index)
    res = [docno_to_id[val] for val in res]
    assert res == ['campaign']


def test_simple_or_query_multiple_docs(index_and_docno_to_id):
    (index, docno_to_id) = index_and_docno_to_id[0], index_and_docno_to_id[1]
    query = '( governor OR black )'
    res = BooleanRetrieval(query, index)
    res = [docno_to_id[val] for val in res]
    assert set(['campaign', 'college']) == set(res)


def test_simple_not_on_one_doc(index_and_docno_to_id):
    (index, docno_to_id) = index_and_docno_to_id[0], index_and_docno_to_id[1]
    query = '( ( governor NOT red ) )'
    res = BooleanRetrieval(query, index)
    print(res, docno_to_id)
    res = [docno_to_id[val] for val in res]
    assert set(['campaign']) == set(res)


def test_simple_not_on_one_doc_returns_none(index_and_docno_to_id):
    (index, docno_to_id) = index_and_docno_to_id[0], index_and_docno_to_id[1]
    query = '( ( governor NOT black ) )'
    res = BooleanRetrieval(query, index)
    print(res, docno_to_id)
    res = [docno_to_id[val] for val in res]
    assert set([]) == set(res)


def test_multiple_or_on_multiple_docs_nested_right(index_and_docno_to_id):
    (index, docno_to_id) = index_and_docno_to_id[0], index_and_docno_to_id[1]
    query = '( black OR ( governor OR spaceflight ) )'
    res = BooleanRetrieval(query, index)
    print(res, docno_to_id)
    res = [docno_to_id[val] for val in res]
    assert set(['campaign', 'college', 'new']) == set(res)


def test_multiple_or_on_multiple_docs_nested_left(index_and_docno_to_id):
    (index, docno_to_id) = index_and_docno_to_id[0], index_and_docno_to_id[1]
    query = '( ( governor OR spaceflight ) OR black )'
    res = BooleanRetrieval(query, index)
    print(res, docno_to_id)
    res = [docno_to_id[val] for val in res]
    assert res == ['campaign', 'college', 'new']


def test_multiple_mixed_and_or_on_multiple_docs_nested_left(index_and_docno_to_id):
    (index, docno_to_id) = index_and_docno_to_id[0], index_and_docno_to_id[1]
    query = '( ( black AND white ) OR new )'
    res = BooleanRetrieval(query, index)
    print(res, docno_to_id)
    res = [docno_to_id[val] for val in res]
    assert set(['campaign', 'college', 'new']) == set(res)


def test_multiple_mixed_and_or_on_multiple_docs_nested_right(index_and_docno_to_id):
    (index, docno_to_id) = index_and_docno_to_id[0], index_and_docno_to_id[1]
    query = '( black AND ( white OR new ) )'
    res = BooleanRetrieval(query, index)
    print(res, docno_to_id)
    res = [docno_to_id[val] for val in res]
    assert set(['campaign', 'college']) == set(res)


def test_multiple_mixed_and_or_on_multiple_docs_nested_both(index_and_docno_to_id):
    (index, docno_to_id) = index_and_docno_to_id[0], index_and_docno_to_id[1]
    query = '( ( black AND governor ) AND ( white OR space ) )'
    res = BooleanRetrieval(query, index)
    print(res, docno_to_id)
    res = [docno_to_id[val] for val in res]
    assert set(['campaign']) == set(res)
