
import numpy as np 

results = np.loadtxt("findation_output.txt")







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
                    