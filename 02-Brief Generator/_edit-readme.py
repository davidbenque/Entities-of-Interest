# -*- coding: utf-8 -*-
# @Author: davidbenque
# @Date:   2018-06-15 14:14:44
# @Last Modified by:   davidbenque
# @Last Modified time: 2018-07-03 09:57:26

import pandas as pd

name_list = pd.read_csv('../01-Name Hunting/_selected_names.csv')

for index, row in name_list.iterrows():

    company_name = row["name"]
    company_path = "../03-Content/" + company_name
    readme_file_name = company_path + '/Readme.md'
    readme_file = open(readme_file_name, 'r')
    
    line_count = len(readme_file.readlines())
    print(line_count)

    if line_count == 12:
        print("doing this one")
        readme_file = open(readme_file_name, 'r')
        readme_file_contents = readme_file.read()
        new_file = open(readme_file_name, 'w')
        new_file.write(readme_file_contents)
        new_file.write("\nOpen for contributions. See [instructions](/Readme.md#contribute)")
        new_file.close()


# add content to the file 
    # readme_file_contents = readme_file.read()

    # header = "#### [Entities of Interest](/list.html)\n"

    # new_file = open(readme_file_name, 'w')
    # new_file.write(header)
    # new_file.write(readme_file_contents)
    # new_file.close()