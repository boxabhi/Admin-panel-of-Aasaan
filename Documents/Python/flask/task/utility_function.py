from collections import Counter


# function for reversing a string!
def rev(str):
    return str[::-1]

def split_s(line,n):
    # Empty array for reverse
    ans = []
    line = line[::-1]
    split_list =([line[i:i+n] for i in range(0, len(line), n)])
    for i in range(len(split_list)):
        ans.append(rev(split_list[i]))
    reversed(ans)
    return ans


def count_words(str):
    # for splitting string 
    temp = str.split(', ')
    count_list ={}
    # Getting unique words
    key_list = list(Counter(temp).keys())
    # counting unique words
    value_list = list(Counter(temp).values())
    # Mapping words to count
    for i in range(len(key_list)):
        count_list[key_list[i]] = value_list[i]
    return count_list