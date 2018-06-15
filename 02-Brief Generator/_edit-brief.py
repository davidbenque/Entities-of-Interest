# -*- coding: utf-8 -*-
# @Author: davidbenque
# @Date:   2018-06-15 13:36:58
# @Last Modified by:   davidbenque
# @Last Modified time: 2018-06-15 14:12:31


## Batch add header link to stylesheet and graph image
## Don't run again! 

import pandas as pd

name_list = pd.read_csv('../01-Name Hunting/_selected_names.csv')

for index, row in name_list.iterrows():

    company_name = row["name"]

    company_path = "../03-Content/" + company_name
    brief_file_name = company_path + '/Brief.md'
    brief_file = open(brief_file_name, 'r')
    brief_file_contents = brief_file.read()

    s3_url = "http://eoi-graphs.s3-website-eu-west-1.amazonaws.com/"

    image_file_name = company_name.replace(" ","_") + ".png"
    image_url = s3_url + image_file_name

    header = '<link rel="stylesheet" type="text/css" href="../../assets/style.css">\n#### [Entities of Interest](/list.html)\n\n'

    footer = '''
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
    </div>
    \n
    <img src="{image_file}" alt="">\n
    '''
    footer = footer.format(name=company_name, image_file=image_url)
    footer = footer.replace("    ","")

    new_file = open(brief_file_name, 'w')
    new_file.write(header)
    new_file.write(brief_file_contents)
    new_file.write(footer)
    new_file.close()

