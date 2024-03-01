# import source.helper
import sys
sys.path.append( '.' )

import grammar as grammar
import core.constants as constants
 
def generate_follow(cfg):
    production_stack=[]
    follow_set={keys:[] for keys in cfg.keys()}
    follow_set["program"]=["$"]
    for terminal in cfg.keys():
        for production in cfg[terminal]:
            for i in range(len(production)):
                if i+1 < len(production) and production[i+1] in constants.terminals:
                    follow_set[terminal] += production[i+1]
                else:
                    if i+1 < len(production) and production[i+1] in cfg.keys():
                        production_stack.append(production[i+1])
                        for items in cfg[production[i+1]]:
                            follow_set[production[i+1]].append(grammar.FirstFollowPredict().firstSet(cfg, items))
    while production_stack:
        production=production_stack.pop()
        for i in range(len(production)):
            if i+1 < len(production) and production[i+1] in constants.terminals:
                follow_set[production] += production[i+1]
            else:
                if i+1 < len(production) and production[i+1] in cfg.keys():
                    production_stack.append(production[i+1])
                    for items in cfg[production[i+1]]:
                        follow_set[production[i+1]].append(grammar.FirstFollowPredict().firstSet(cfg, items))

    return follow_set


def syntax_analyzer(cfg, input_string):
    stack = ['$']
    current_token = input_string[0]
    follow_set = generate_follow(cfg)

    while stack:
        top = stack[-1]

        if top in cfg.keys():
            if current_token in follow_set[top]:
                stack.pop()
            else:
                return False
        elif top == current_token:
            stack.pop()
            current_token = input_string[input_string.index(current_token) + 1]
        else:
            return False

    return True

input_string = "..."
result = syntax_analyzer(grammar.Grammar.cfg, input_string)
print(result)

print(generate_follow(grammar.Grammar.cfg)) 