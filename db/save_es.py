from elasticsearch import Elasticsearch
import sys
import json

esclient = Elasticsearch(['http://10.10.4.220:9200'])

def es_save_data(index, type, doc):
    """
    :param doc: doc to be saved
    :return:
    """

    res = esclient.index(index=index, doc_type=type, body=doc)
    print res


def es_delete_index(index):
    """
    :param index: es index to be deleted
    :return:
    """
    
    re = esclient.indices.delete(index)
    print re

def main(argv):
    """
    :param argv:
    :return:
    """

    indexs = ["daad_waf_event-2016.11.*"]

    #for index in indexs:
    #    es_delete_index(index)

    index = "ip2identity"
    type = "ip2identity"

    with open('ip2iden') as fr:
        for i in fr:
            j = i.strip().split(" ")
            doc = {'ip': j[0], 'identity': j[1]}
            json_str = json.dumps(doc)
            es_save_data(index, type, json_str)


if __name__ == '__main__':
    main(sys.argv[1:])