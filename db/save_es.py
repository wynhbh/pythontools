from elasticsearch import Elasticsearch
import sys

esclient = Elasticsearch(['http://10.10.4.224:9200'])

def save_es(events):
    """
    :param events: event examples to be saved
    :return:
    """

    for event in events:
        event.duration = event.endtime - event.starttime
        doc = event.tojson()
        res = esclient.index(index="guowang-fw-event-" + event.date.replace('-', '.'), doc_type='fw-event-c2c',
                             id=event.sda_id, body=doc)
        print res


def es_delete_index(index):
    """
    :param index: es index to be deleted
    :return:
    """
    #sr = esclient.search(index)
    #print index, sr
    
    re = esclient.indices.delete(index)
    print re

def main(argv):
    """
    :param argv:
    :return:
    """


    #index = "guowang-waf-event-*"
    #es_delete_index(index)
    
    """
    indexs = ["guowang-ids-event-*",
              "guowang-fw-event-*",
              "guowang-fw-event-*",
              "guowang-fw-knowledge",
              "guowang-ids-event-*",
              "guowang-ids-event-*",
              "guowang-ids-knowledge",
              "guowang-traffic-event-*",
              "guowang-waf-event-*",
              "guowang-waf-knowledge"]


    indexs = ["daad_ids_event-2016.07.*",
                "daad_ids_event-2016.08.*",
                "daad_ids_event-2016.09.*",
                "daad_ids_event-2016.10.*",
                "daad_ids_event-2016.11.*",
                "daad_ids_event-2016.12.*"]

    """

    indexs = ["daad_waf_event-2016.11.*"]

    for index in indexs:
        es_delete_index(index)


if __name__ == '__main__':
    main(sys.argv[1:])