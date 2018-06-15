from pathlib import Path
import os
import pandas as pd

name_list = pd.read_csv('../01-Name Hunting/_selected_names.csv')



# for index, row in name_list.iterrows():

#     company_name = row["name"]
#     graph_file = Path("../03-Content/" + company_name + "/graph.html")

#     if graph_file.exists():
#         new_name = company_name.replace(" ", "_")
#         os.rename(graph_file, '../Bokeh-Briefs/' + new_name + ".html")
#     else: 
#         next(name_list.iterrows())
#         continue

for index, row in name_list.iterrows():

    company_name = row["name"]
    graph_file = Path("../03-Content/" + company_name + "/graph.html")

    if graph_file.exists():
        os.remove(graph_file)
    else: 
        next(name_list.iterrows())
        continue