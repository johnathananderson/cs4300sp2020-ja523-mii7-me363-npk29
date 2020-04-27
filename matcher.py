
import numpy as np 
import copy
import re
import ast
import json


def main_function(query, results):

    info_dict = {}
    object_list = []
    foundation_list  = []
    shade_list = []
    with open("results", 'r' , encoding="ISO-8859-1") as f:
        for line in f.readlines():
            object_list.append(ast.literal_eval(line))
    for lines in object_list:
        info_dict[lines['brand']] = {}
    #     if lines['name'] not in foundation_list:
    #         foundation_list.append(lines['name'])
    #     if lines['shade'] not in shade_list:
    #         shade_list.append(lines['shade'])
    # print(shade_list)

        # info_dict[lines['brand']].update({'name': []})

 
    for key in info_dict.keys():
        for lines in object_list:
            brand = lines['brand']
            if brand == key:
                name = lines['name']
                shade = lines['shade']
                thumbnail = lines['thumbnail']
                ingredients = lines['ingredients']

                info_dict[brand].update({name: {}})
                info_dict[brand][name].update({shade: {}})
                info_dict[brand][name][shade].update({'ingredients': ingredients})
                info_dict[brand][name][shade].update({'thumbnail': thumbnail})


        output_list = []
    for key in info_dict.keys():
        message_dict = {}
        message = key
        for ke in info_dict[key].keys():
            temp = message 
            temp2 = "".join((temp, " ", ke))
           
            for k in info_dict[key][ke].keys():
                temp3  = temp2
                temp4 = "".join((temp3, " ", k))
                message_dict['text'] =  temp4
                output_list.append(message_dict)
                message_dict = {}
           
    
            
    scores = edit_distance_search(query, output_list)

    return(scores[0])
   












    # with open("findation_output.txt", encoding="latin-1") as datafile:
    #    results = datafile.readlines()
    # # split_arrays = re.findall"[\u4e00-\u9fff]+", results)   
    # for items in results:
    #     item  = items.split(',')
    
      
    #     for it in item:
         
    #         breakup = it.split(',')
           
    #         for st in breakup:
                
    #             if '{'  in st:
    #                 st = st.replace("{", "")
    #             elif '}' in st:
    #                 st = st.replace('}', "")
    #             final = st.split(':')
    #             for i in range(len(final)):
    #                 item = final[i].strip('"')
    #                 if i == 0:
    #                     key = item
    #                     if i 
    #                     info_dict[key] = 
    #                 if i > 0 :
    #                     val = final[0]
    #                      info_dict[val] 
    #                 #  info_dict[item1] = 
          
                    
                  

                
                    
            
            
            





def insertion_cost(message, j):
    return 1

def deletion_cost(query, i):
    return 1

def substitution_cost(query, message, i, j):
    if query[i-1] == message[j-1]:
        return 0
    else:
        return 1
    
curr_insertion_function = insertion_cost
curr_deletion_function = deletion_cost
curr_substitution_function = substitution_cost

def edit_matrix(query, message):
    """ calculates the edit matrix
    
    Arguments
    =========
    
    query: query string,
        
    message: message string,
    
    m: length of query + 1,
    
    n: length of message + 1,
    
    Returns:
        edit matrix {(i,j): int}
    """
    
    m = len(query) + 1
    n = len(message) + 1

    chart = {(0, 0): 0}
    for i in range(1, m): 
        chart[i,0] = chart[i-1, 0] + curr_deletion_function(query, i) 
    for j in range(1, n): 
        chart[0,j] = chart[0, j-1] + curr_insertion_function(message, j)
    for i in range(1, m):
        for j in range(1, n):
            chart[i, j] = min(
                chart[i-1, j] + curr_deletion_function(query, i),
                chart[i, j-1] + curr_insertion_function(message, j),
                chart[i-1, j-1] + curr_substitution_function(query, message, i, j)
            )
    return chart

def edit_distance(query, message):
    """ Edit distance calculator
    
    Arguments
    =========
    
    query: query string,
        
    message: message string,
    
    Returns:
        edit cost (int)
    """
        
    query = query.lower()
    message = message.lower()
    value = edit_matrix(query, message)
    score = 0
    for keys in value.keys():
        if keys == (len(query), len(message)):
            score = value[keys]
        
    return(score)


def edit_distance_search(query, msgs):
    """ Edit distance search
    
    Arguments
    =========
    
    query: string,
        The query we are looking for.
        
    msgs: list of dicts,
        Each message in this list has a 'text' field with
        the raw document.
    
    Returns
    =======
    
    result: list of (score, message) tuples.
        The result list is sorted by score such that the closest match
        is the top result in the list.
    
    """
    result = []
    for items in msgs:
            for key in items.keys():
                if key == 'text':
                    sentence  = items[key]
                    score = edit_distance(query, sentence)
                    result.append((score, items))
    result.sort(key = lambda x: x[0])  

    return(result)
                    
