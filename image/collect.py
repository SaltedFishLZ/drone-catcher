#!/usr/bin/python3

import re
import os
import sys
import copy
import shutil
import subprocess


def trans_lines(
    old_lines,
    modify_rules,
    ):

    new_lines = []

    # first, get some common information
    if ("folder" in modify_rules):
        folder = modify_rules["folder"]
    else:
        folder = "drone"
    if ("filename" in modify_rules):
        filename = modify_rules["filename"]
    else:
        filename = "default.jpg"
    path = os.path.join(folder, filename)
        
    
    # second, modify information
    for old_line in old_lines:
        # modify lines by rules
        if ("<folder>" in  old_line):
            new_line = "<folder>{}</folder>\n".format(folder)
        elif ("<filename>" in old_line):
            new_line = "<filename>{}</filename>\n".format(filename)
        elif ("<path>" in old_line):
            new_line = "<path>{}</path>\n".format(path)
        elif ("<database>" in old_line):
            new_line = "<database>DroneCatcher</database>\n"
        elif ("<name>test_drone</name>" in old_line):
            new_line = "<name>drone</name>\n"
        else:
            new_line = copy.deepcopy(old_line)

        new_lines.append(new_line)
    
    return(copy.deepcopy(new_lines))


def copy_raw_data(task_dict):

    source_path = task_dict["source_path"]
    format_image = task_dict["format_image"]
    format_label = task_dict["format_label"]
    old_id = task_dict["old_id"]
    offset = task_dict["offset"]

    old_image = format_image.format(old_id)
    old_label = format_label.format(old_id)
    old_image = os.path.join(source_path, old_image)
    old_label = os.path.join(source_path, old_label)

    new_id = offset + old_id
    new_image = "{}.jpg".format(new_id)
    new_label = "{}.xml".format(new_id)
    new_image = os.path.join("drone", new_image)
    new_label = os.path.join("drone", new_label)

    # copy image file
    shutil.copyfile(old_image, new_image)

    # generate modifification rules
    modify_rules = {"filename": "{}.xml".format(new_id)}
    
    # modify label data
    fin = open(old_label, "r")
    fout = open(new_label, "w")
    
    old_lines = fin.readlines()
    new_lines = trans_lines(old_lines, modify_rules)
    fout.writelines(new_lines)

    fin.close()
    fout.close()



if __name__ == "__main__":
    
    # ---------------
    # generate tasks
    # ---------------
    task_queue = []
    task_dict = dict()
    count = 0
    total = count
    # for bbs 20180602
    for i in range(144):
        task_dict["source_path"] = os.path.join("bbs", "20180602")
        task_dict["format_image"] = "bbs ({}).jpg"
        task_dict["format_label"] = "bbs ({}).xml"
        task_dict["old_id"] = i + 1
        task_dict["offset"] = total-1

        task_queue.append(copy.deepcopy(task_dict))
        count += 1
    # for bbs 20180603
    total = count
    for i in range(100):
        task_dict["source_path"] = os.path.join("bbs", "20180603")
        task_dict["format_image"] = "bbs ({}).jpg"
        task_dict["format_label"] = "bbs ({}).xml"
        task_dict["old_id"] = i + 1
        task_dict["offset"] = total-1

        task_queue.append(copy.deepcopy(task_dict))
        count += 1
    # for logitech_c992 20180523
    total = count
    for i in range(224):
        task_dict["source_path"] = os.path.join("logitech_c992", "20180523")
        task_dict["format_image"] = "logitech ({}).jpg"
        task_dict["format_label"] = "logitech ({}).xml"
        task_dict["old_id"] = i + 1
        task_dict["offset"] = total-1

        task_queue.append(copy.deepcopy(task_dict))
        count += 1
    # for logitech_c992 20180525
    total = count
    for i in range(299):
        task_dict["source_path"] = os.path.join("logitech_c992", "20180525")
        task_dict["format_image"] = "logitech ({}).jpg"
        task_dict["format_label"] = "logitech ({}).xml"
        task_dict["old_id"] = i + 1
        task_dict["offset"] = total-1

        task_queue.append(copy.deepcopy(task_dict))
        count += 1        
    # for internet 20180524
    total = count
    for i in range(242):
        task_dict["source_path"] = os.path.join("internet", "20180524")
        task_dict["format_image"] = "bing ({}).jpg"
        task_dict["format_label"] = "bing ({}).xml"
        task_dict["old_id"] = i + 1
        task_dict["offset"] = total-1

        task_queue.append(copy.deepcopy(task_dict))
        count += 1



    for task_dict in task_queue:
        copy_raw_data(task_dict)
