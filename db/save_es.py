from elasticsearch import Elasticsearch
import sys
import json

#esclient = Elasticsearch(['http://127.0.0.1:9200'])
esclient1 = Elasticsearch(['http://10.10.4.220:9200'])
#esclient1 = Elasticsearch(['http://127.0.0.1:9200'])

def es_save_data(index, type, doc):
    """
    :param doc: doc to be saved
    :return:
    """

    res = esclient1.index(index=index, doc_type=type, body=doc)
    print res


def es_delete_index(index):
    """
    :param index: es index to be deleted
    :return:
    """
    
    re = esclient.indices.delete(index)
    print re

def es_search(index, body):
    res = esclient.search(index=index, body=body)
    return res['hits']

def get_device(index, identity, ts):
    """
    @param index:
    @param identity:
    @param ts:
    @return:
    """
    body = {
        "query": {
            "constant_score": {
                "filter": {
                    "bool": {
                        "should": {
                            "term": {
                                "identity": identity
                            }
                        },
                        "should": {
                            "range": {
                                "ts": {
                                    "lt": ts + 70,
                                    "gt": ts - 60
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    res = es_search(index, body)

    tsarr = []
    for hit in res['hits']:
        # print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
        tsarr.append([hit["_source"]["ts"], hit["_source"]])

    ls = sorted(tsarr, lambda x,y: cmp(x[0], y[0]))
    if len(ls) > 0:
        return ls[0][1]

def get_identity(index, ts):

    body = {
        "query": {
            "constant_score": {
                "filter": {
                    "range": {
                        "ts": {
                            "gt": ts,
                        }
                    }
                }
            }
        }
    }

    res = es_search(index, body)
    return res['hits']

    '''

    identities = []
    for hit in res['hits']:
        identity = hit["_source"]["identity"]
        time = hit["_source"]["ts"]
        #if time > ts - 5:
        identities.append([identity, time])
    return identities
    '''

def run():

    index = "conn_test3-2017.05.14"         # test
    path_index = "conn_path-2017.05.14"     # test
    path_type = "path"

        #1494777595
    #ts = 1494777596
    #ts = 2000000000
    #ts = 1494777600   n
    #ts = 1494777664
    #ts = 1494777665     #lt 70

    ts = 1494777535     #gt 60

    hits = get_identity(index, ts)

    for i in hits:
        data = i["_source"]

        #identity = hit["_source"]["identity"]
        #time = hit["_source"]["ts"]

        index1 = "conn_test1-2017.05.14"
        index2 = "conn_test1-2017.05.14"
        t1 = get_device(index1, data["identity"], data["ts"])
        t2 = get_device(index2, data["identity"], data["ts"])

        if t1 is not None and t2 is not None:
            data["path"] = ["device1", "device2", "server"]
            data["messages"] = [{"device1":t1}, {"device2":t2}]

        json_str = json.dumps(data)
        es_save_data(path_index, path_type, json_str)

    return

def main(argv):
    """
    :param argv:
    :return:
    """

    #indexs = ["daad_waf_event-2016.11.*"]

    #for index in indexs:
    #    es_delete_index(index)

    #es_delete_index("ip2identity")
    
    index = "ip2identity"
    type = "ip2identity"
    
    with open('ip2iden') as fr:
        for i in fr:
            j = i.strip().split(" ")
            doc = {'ip': j[0], 'identity': j[1]}
            json_str = json.dumps(doc)
            es_save_data(index, type, json_str)

    #run()

if __name__ == '__main__':
    main(sys.argv[1:])
