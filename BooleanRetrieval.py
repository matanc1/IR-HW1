from query_parser import query_ast, tokenize, BoolExpr, TermExpr


def results_merge(ids1, ids2, operator):
    if operator == 'AND':
        return [id for id in ids1 if id in ids2]
    elif operator == 'OR':
        return list(set(ids1).union(set(ids2)))
    elif operator == 'NOT':
        return [id for id in ids1 if id not in ids2]
    else:
        raise Exception('Not a valid operator')


def ast_eval(root, index):
    if isinstance(root, BoolExpr):
        return results_merge(ast_eval(root.left, index), ast_eval(root.right, index), root.operator)
    elif isinstance(root, TermExpr):
        return index.get(root.term, {}).get('posting_list', [])

    else:
        raise Exception('Something went wrong')


def BooleanRetrieval(query, index):
    query_tokens = list(tokenize(query))
    ast = query_ast(query_tokens)
    res = ast_eval(ast, index)
    return res
