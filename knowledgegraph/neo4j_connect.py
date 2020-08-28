# -*- coding: UTF-8 -*-
'''
Created on 2020/8/24 16:55
@File  : neo4j_connect.py
@author: ZL
@Desc  : 用于动态获取neo4j的数据
'''

from neo4j import GraphDatabase


class Neo4jConnect:
    def __init__(self):
        self.uri = "bolt://192.168.1.15:7687"
        self._driver = GraphDatabase.driver(self.uri, auth=("neo4j", "Ko1357955"))

    def get_item(self, flag_name):
        with self._driver.session() as session:
            item_data = session.run(
                "MATCH (i:Item{flag:$flagname})"
                "RETURN i.name as item",
                flagname=flag_name).data()
            return item_data

    def get_cause(self, flag_name):
        with self._driver.session() as session:
            cause_data = session.run(
                "MATCH (c:Cause{flag:$flagname})"
                "RETURN c.name as cause",
                flagname=flag_name).data()
            return cause_data

    def get_check(self, flag_name):
        with self._driver.session() as session:
            check_data = session.run(
                "MATCH (c:Check{flag:$flagname})"
                "RETURN c.name as check",
                flagname=flag_name).data()
            return check_data

    def get_symptom(self, flag_name):
        with self._driver.session() as session:
            symptom_data = session.run(
                "MATCH (s:Symptom{flag:$flagname})"
                "RETURN s.name as symptom",
                flagname=flag_name).data()
            return symptom_data

    def get_other_treatment(self, flag_name):
        with self._driver.session() as session:
            treatment_data = session.run(
                "MATCH (o:Othertreatment{flag:$flagname})"
                "RETURN o.name as treatment",
                flagname=flag_name).data()
            return treatment_data

    def match_item_check(self, flag_name):
        with self._driver.session() as session:
            item_check_data = session.run(
                "MATCH (i:Item{flag:$flagname})-[r:NEED_TO_CHECK]->(c:Check{flag:$flagname})"
                "RETURN i.name as item,c.name as check",
                flagname=flag_name).data()
            return item_check_data

    def match_item_cause(self, flag_name):
        with self._driver.session() as session:
            item_check_data = session.run(
                "MATCH (i:Item{flag:$flagname})-[r:PROBABLE_CAUSE]->(c:Cause{flag:$flagname})"
                "RETURN i.name as item,c.name as cause",
                flagname=flag_name).data()
            return item_check_data

    def match_item_other_treatment(self, flag_name):
        with self._driver.session() as session:
            item_treatment_data = session.run(
                "MATCH (i:Item{flag:$flagname})-[r:HAS_TREATMENT]->(o:Othertreatment{flag:$flagname})"
                "RETURN i.name as item,o.name as symptom",
                flagname=flag_name).data()
            return item_treatment_data

    def match_item_symptom(self, flag_name):
        with self._driver.session() as session:
            item_symptom_data = session.run(
                "MATCH (i:Item{flag:$flagname})-[r:RELATED_SYMPTOMS]->(s:Symptom{flag:$flagname})"
                "RETURN i.name as item,s.name as symptom",
                flagname=flag_name).data()
            return item_symptom_data

    def get_match(self, cypher_query):
        with self._driver.session() as session:
            result_data = session.run(cypher_query).data()
            return result_data


# if __name__ == '__main__':
#     # print(Neo4jConnect().get_item("andrology_v1"))
#     # print(Neo4jConnect().get_cause("andrology_v1"))
#     # print(Neo4jConnect().get_check("andrology_v1"))
#     # print(Neo4jConnect().get_symptom("andrology_v1"))
#     # print(Neo4jConnect().get_other_treatment("andrology_v1"))
#     # print(Neo4jConnect().match_item_other_treatment("andrology_v1"))
#     # print(Neo4jConnect().match_item_check("andrology_v1"))
#     # print(Neo4jConnect().match_item_cause("andrology_v1"))
#     # print(Neo4jConnect().match_item_symptom("andrology_v1"))
#     print(Neo4jConnect().get_match(
#         'MATCH (i:Item{flag:"andrology_v1"})-[r:RELATED_SYMPTOMS]->(s:Symptom{flag:"andrology_v1"})'
#         "RETURN i.name as item,s.name as symptom"))
