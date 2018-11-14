from collections import defaultdict
import xml.etree.ElementTree as et
from collections import Counter


def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


def docs_from_file(path):
    with open(path, 'r') as file:
        file_xml = file.read()
        file_xml_string = '<ROOT> {} </ROOT>'.format(file_xml)
        try:
            root = et.fromstring(file_xml_string)
            docs_dict = etree_to_dict(root)
            return [Doc(doc) for doc in docs_dict['ROOT']['DOC']]
        except:
            return []


class Doc:
    def __init__(self, dict):
        self.docno = dict['DOCNO']
        try:
            if isinstance(dict['TEXT'], list):
                text = ' '.join(dict['TEXT'])
            else:
                text = dict['TEXT']
        except:
            print('There was a problem with doc: {}'.format(self.docno))
            text = ''

        text = text.replace("\n", "")
        self.tf = Counter(text.split(' '))

    def __repr__(self):
        return 'DocID: {}'.format(self.docno)
