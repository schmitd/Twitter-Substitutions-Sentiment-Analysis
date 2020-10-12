def replace_str_index(text,index,replacement):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])
    
'''generates a list of entered string with astrisks substited all possible ways'''
def gen_substitutions(input):
    substitutions_set = set()
    for i in range(len(input)):
        if input[i] == '*':
            continue
        substitution = replace_str_index(input, i, '*')
        print(substitution)
        substitutions_set.add(substitution)
        sub_subs = gen_substitutions(substitution)
        substitutions_set |= sub_subs
    return substitutions_set
