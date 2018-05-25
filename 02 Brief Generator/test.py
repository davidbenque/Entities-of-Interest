# -*- coding: utf-8 -*-
# @Author: davidbenque
# @Date:   2018-03-29 11:14:25
# @Last Modified by:   davidbenque
# @Last Modified time: 2018-05-25 08:51:43

from py2neo import Graph

NEO4J_USER = "neo4j"
NEO4J_PASS = "panamo"

url = 'http://localhost:7474'
graph = Graph(url + '/db/data', username = NEO4J_USER, password = NEO4J_PASS)

def parse_node(node):
    label = list(node.labels())[0]
    if label == "Officer":
        return node["name"], node["countries"]
    elif label == "Intermediary":
        return node["name"], node["address"], node["countries"]
    elif label == "Address":
        return node["address"], node["countries"]
    elif label == "Entity":
        return node["name"], node["address"]

''' Index building example - non-internal properties for each node label
CALL apoc.index.addAllNodes('offshore',{
  Officer: ["name","countries"],
  Intermediary:  ["name","address","countries"],
  Address: ["address","countries"],
  Entity: ["name", "address", "service_provider", "former_name", "company_type","countries"]})
  '''

query = '''
    MATCH (a:Entity)-[]-()
    RETURN a, rand() as r
    ORDER BY r
        LIMIT 25
    '''

entities = graph.run(query)
entities.forward()
start = entities.current()
start_id = start["a"]["node_id"]

def check_prop(node, prop):
  return node["a"][prop] if node["a"][prop] else "unknown"

print(start["a"]["name"])
print("Type: " + check_prop(start, "company_type"))
print("Status: " + check_prop(start, "status"))
print("Address: " + check_prop(start, "address"))

start_node = graph.find_one("Entity", "node_id", start_id)

# Incoming links 
print("--- Stakeholders ---")
for i in graph.match(end_node = start_node):
    link_type = i.type()
    if link_type.endswith("_OF"):
        link_type = link_type[:-3]
    print(link_type)

    for i in parse_node(i.start_node()):
        if i:
            print(i)
    print("")

# Example Queries

'''
MATCH (o:Officer) WHERE o.name CONTAINS 'Trump'
MATCH path = (o)-[]->(:Entity)
      <-[]-(:Officer)-[]->(:Entity)
RETURN path LIMIT 100
'''

