# -*- coding: utf-8 -*-
# @Author: davidbenque
# @Date:   2018-03-29 11:14:25
# @Last Modified by:   davidbenque
# @Last Modified time: 2018-06-04 19:52:19

from py2neo import Graph

# login local ICIJ Neo4j database at http://localhost:7474

NEO4J_USER = "neo4j" # replace with your login
NEO4J_PASS = "panamo" # replace with your password

url = 'http://localhost:7474'
graph = Graph(url + '/db/data', username = NEO4J_USER, password = NEO4J_PASS)

# Get the node from the graph
query = '''
    MATCH (a:Entity)
    RETURN a, rand() as r
    ORDER BY r
    LIMIT 10
    '''

entity = graph.run(query)
entity.forward()
start = entity.current()
start_id = start["a"]["node_id"]
entity_node = graph.find_one("Entity", "node_id", start_id)


basic_info = ["name", "company_type", "status", "address"]

for deet in basic_info:
    if entity_node[deet]:
        print(deet.title() + ": " + entity_node[deet]) 
