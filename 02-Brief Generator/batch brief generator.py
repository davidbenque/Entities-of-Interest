# -*- coding: utf-8 -*-
# @Author: davidbenque
# @Date:   2018-03-29 11:14:25
# @Last modified by:   davidbenque
# @Last modified time: 2018-06-08 9:29:37

from py2neo import Graph
import itertools
import pandas as pd
import os

# login local ICIJ Neo4j database at http://localhost:7474

NEO4J_USER = "neo4j" # replace with your login
NEO4J_PASS = "panamo" # replace with your password

url = 'http://localhost:7474'
graph = Graph(url + '/db/data', username = NEO4J_USER, password = NEO4J_PASS)

name_list = pd.read_csv('../01-Name Hunting/_selected_names.csv')
shuffled_names = name_list.sample(frac=1).reset_index(drop=True)

#################
## Functions
#################

def parse_node(node):
    ''' returns a dict of properties for a node'''
    label = list(node.labels())[0] # assumes 1 label per node
    if label == "Officer":
        return {"name": node["name"], "countries": node["countries"]}
    elif label == "Intermediary":
        return {"name": node["name"], "address": node["address"], "countries": node["countries"]}
    elif label == "Address":
        return {"address": node["address"], "countries": node["countries"]}
    elif label == "Entity":
        return {"name": node["name"], "address": node["address"]}


# Generator check - see if there are any incoming/outgoing links to display

def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterable)



############
# Loop through all names in the list and generate a brief for each
############

for index, row in name_list.iterrows():

    company_name = row["name"]
    print("processing: ", company_name)

    if os.path.exists("../03-Content/" + company_name):
        path = "../03-Content/" + company_name
    else:
        os.mkdir("../03-Content/" + company_name)
        path = "../03-Content/" + company_name

    brief_file = open(path + '/Brief.md', 'w')
    content_file = open(path + '/Readme.md', 'w')


    # Get the node from the graph
    query = '''
        MATCH (a:Entity)
        WHERE a.name = {name}
        RETURN a
        '''

    entity = graph.run(query, name = company_name)
    entity.forward()
    start = entity.current()
    start_id = start["a"]["node_id"]
    entity_node = graph.find_one("Entity", "node_id", start_id)


########
# Brief 

    # Company Details
    brief_file.write("# " + start["a"]["name"] + "\n")

    basic_info = ["company_type", "status", "address"]

    for deet in basic_info:
        if entity_node[deet]:
            brief_file.write(deet.title() + ": " + entity_node[deet] + "\n")
    brief_file.write("\n")


    # Incoming links
    incoming_nodes = graph.match(end_node = entity_node)
    in_check = peek(incoming_nodes)

    if in_check is None:
        brief_file.write("" + "\n")
    else:
        brief_file.write("## Stakeholders" + "\n")
        first, nodelist_in = in_check
        for i in nodelist_in:
            link_type = i.type()
            if link_type.endswith("_OF"):
                link_type = link_type[:-3]
            brief_file.write(link_type + "\n")
            source_dict = parse_node(i.start_node())
            for key, i in source_dict.items():
                if i:
                    brief_file.write(i + "\n" )
            brief_file.write("" + "\n" + "\n")

    # Outgoing links

    outgoing_nodes = graph.match(start_node = entity_node)
    out_check = peek(outgoing_nodes)

    if out_check is None:
        brief_file.write("" + "\n")
    else:
        first, nodelist_out = out_check
        for i in nodelist_out:
            link_type = i.type()
            if link_type.endswith("_OF"):
                link_type = link_type[:-3]
            brief_file.write(link_type + "\n")

            source_dict = parse_node(i.end_node())
            for key, i in source_dict.items():
                if i:
                    brief_file.write(i + "\n")
            brief_file.write("" + "\n" + "\n")

    brief_file.close()


########
# Content Template
    content_file.write('<link rel="stylesheet" type="text/css" href="../../assets/style.css">\r')
    content_file.write("# " + start["a"]["name"] + "\n\n")
    content_file.write("[comment]: <> (Add/Remove information below as you want)\r[comment]: <> (Markdown cheatsheet: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)\r")
    content_file.write("[Brief](Brief.md)  \rby:  \rdate:  \r\r")
    content_file.write("---\r[comment]: <> (Add your content here)")

