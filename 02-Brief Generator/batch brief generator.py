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

# CSV with all the selected names
name_list = pd.read_csv('../01-Name Hunting/_selected_names.csv')

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


    s3_url = "http://eoi-graphs.s3-website-eu-west-1.amazonaws.com/"

    image_file_name = company_name.replace(" ","_") + ".png"
    image_url = s3_url + image_file_name


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

    # Header
    brief_file.write('#### [Entities of Interest](/list.html)\n<link rel="stylesheet" type="text/css" href="../../assets/style.css">\n\n')

    css = '<style>\nbody{background-image:' + 'url("{bg_url}")'.format(bg_url=image_url) + ';background-repeat: no-repeat;background-size: contain;}\n.markdown>p>span{background-color: white;}\n</style>\n\n'

    brief_file.write(css)

    # Company Details
    brief_file.write("# " + start["a"]["name"] + "\n")

    basic_info = ["company_type", "status", "address"]
    brief_file.write('<span>')
    for deet in basic_info:
        if entity_node[deet]:
            brief_file.write(deet.title() + ": " + entity_node[deet] + "\n")
    brief_file.write("</span>\n")


    # Graph Key

    graph_key = '''
    ---\n
    \n
    <div class="legend">
    Graph Key
    <hr>
    <span class="focus">• {name}</span>
    <span class="entity">• Entities</span>
    <span class="intermediary">• Intermediaries</span>
    <span class="officer">• Officers</span>
    <span class="address">• Addresses</span>
    </div><br>
    \n
    '''
    graph_key = graph_key.format(name=company_name)
    graph_key = graph_key.replace("    ","")
    brief_file.write(graph_key)

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
            brief_file.write("<span>" + link_type + "\n")
            source_dict = parse_node(i.start_node())
            for key, i in source_dict.items():
                if i:
                    brief_file.write(i + "\n" )
            brief_file.write("</span>" + "\n\n")

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
            brief_file.write("<span>" + link_type + "\n")

            source_dict = parse_node(i.end_node())
            for key, i in source_dict.items():
                if i:
                    brief_file.write(i + "\n")
            brief_file.write("</span>" + "\n" + "\n")

    brief_file.write('<br><br><a class="contribute_button" href="Readme.md">Contribute</a>')
    brief_file.close()


########
# Content Template
    # content_file = open(path + '/Readme.md', 'w')

    # content_file.write('<link rel="stylesheet" type="text/css" href="../../assets/style.css">\r')
    # content_file.write("# " + start["a"]["name"] + "\n\n")
    # content_file.write("[comment]: <> (Add/Remove information below as you want)\r[comment]: <> (Markdown cheatsheet: https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)\r")
    # content_file.write("[Brief](Brief.md)  \rby:  \rdate:  \r\r")
    # content_file.write("---\r[comment]: <> (Add your content here)")
    #
