import re

def pull_data(html,start_term, end_term, string_split_start = 0, string_split_end = None):
    pull1 = re.search(start_term + '(.*)' + end_term, html)
    try:
        pull2 = pull1.group(1)
        split = pull2.split(' ')
        if string_split_end is None:
            string_split_end = len(split)
        pull3 = split[string_split_start:string_split_end]
        join = " ".join(pull3)
        return(join)
    except:
        return(None)
