# -*- coding: UTF-8 -*-
'''
Created on 2020/10/13 19:54
@File  : get_re_result.py
@author: ZL
@Desc  :
'''
import pandas as pd
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]


def get_synonymous_entity(input_file=rootPath + "\\testdata\\knowledgegraph\\relationship\\" + "resource.csv",
                          output_file=rootPath + "\\testdata\\knowledgegraph\\relationship\\" + "re_resource1.csv"):
    labels_data = pd.read_csv(input_file)

    entity_value_relationship = labels_data.entity_value_relationship.tolist()
    la_dialog_id = labels_data.dialog_id.tolist()
    la_file = labels_data.file.tolist()
    match_keys = {}

    for k, v in enumerate(la_dialog_id):
        key = la_file[k] + ":" + str(v)
        if key not in match_keys:
            match_keys[key] = []
        match_keys[key].append(entity_value_relationship[k])

    new_data_dict = {}
    for k, v in match_keys.items():
        temp = []
        for i in v:
            if "同义的实体" in i:
                try:
                    split_res = i.split("#")
                    assert split_res[1] == "同义的实体"
                    left = split_res[0]
                    right = split_res[2]
                    for j in v:
                        # if left in j and right in j:
                        #     continue
                        x = j.split("#")
                        if left in x and right not in x:
                            tmp = [right if i == left else i for i in x]
                            zx = "#".join(tmp)
                            fx = "#".join(list(reversed(tmp)))
                            if zx not in temp and fx not in temp:
                                temp.append(zx)
                        elif right in j and left not in j:
                            tmp = [left if i == right else i for i in x]
                            zx = "#".join(tmp)
                            fx = "#".join(list(reversed(tmp)))
                            if zx not in temp and fx not in temp:
                                temp.append(zx)
                except IndexError:
                    print(i)
        new_data_dict[k] = v + temp
    dialog_id = []
    file = []
    entity_value_relationship = []
    for k, v in new_data_dict.items():
        name, idx = k.split(":")
        entity_value_relationship.extend(v)
        try:
            dialog_id.extend([int(idx) for _ in range(len(v))])
        except:
            print(k)
        file.extend([name for _ in range(len(v))])

    pd.DataFrame({
        "dialog_id": dialog_id,
        "entity_value_relationship": entity_value_relationship,
        "file": file}
    ).to_csv(output_file, encoding="utf-8")


get_synonymous_entity()
