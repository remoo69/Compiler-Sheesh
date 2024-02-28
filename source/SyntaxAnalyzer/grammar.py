import os
import sys

parent_directory=os.path.abspath(r"C:\Users\anton\Desktop\College Stuff Files\Compiler-Sheesh\source")
sys.path.append(parent_directory)
import core.constants as const

class FirstFollowPredict:
    def __init__(self):
        self.visited = set()  # To track visited non-terminals and avoid infinite loops

    def predict_set(self, cfg: dict):
        ps = {}
        for key in cfg.keys():
            ps[key] = self.compute_predict_set(cfg, key)
        return ps

    def compute_predict_set(self, cfg, non_terminal):
        if non_terminal in self.visited:
            return set()

        self.visited.add(non_terminal)

        predict_set = []

        for production in cfg[non_terminal]:
            predict_set.append(self.compute_predict_set_for_production(cfg, production, non_terminal))

        return predict_set

    def compute_predict_set_for_production(self, cfg, production, non_terminal):
        if not production:  # Empty production
            return self.calculate_follow_set(cfg, non_terminal)

        first_symbol = production[0]

        if first_symbol in cfg.keys():
            first_set_of_first_symbol = self.firstSet(cfg, first_symbol)
            predict_set = first_set_of_first_symbol
            if "null" in first_set_of_first_symbol:
                predict_set.append(self.follow(cfg, non_terminal))
        else:
            predict_set = {first_symbol}

        return predict_set
    
    def firstSet(self, cfg: dict, firstOf):
        fs = set()
        visited = set()  # To track visited non-terminals and avoid infinite loops
        self.computeFirstSet( cfg, firstOf, fs, visited)
        return list(fs)


    def computeFirstSet(self, cfg, non_terminal, first_set, visited):
        if non_terminal in const.terminals:
            first_set.add(non_terminal)
            return
        if str(non_terminal) in visited:  # Convert non-terminal to a hashable type
            return

        visited.add(str(non_terminal))  # Convert non-terminal to a hashable type

        for production in cfg[non_terminal]:
            if not production:  # Empty production
                continue

            ptr = 0
            while ptr < len(production):
                current_symbol = production[ptr]

                if current_symbol in const.terminals:
                    first_set.add(current_symbol)
                    break
                elif current_symbol in cfg.keys():
                    self.computeFirstSet(cfg, current_symbol, first_set, visited)
                    if '' not in first_set:
                        break
                    ptr += 1
                else:
                    ptr += 1
        if non_terminal in const.terminals:
            first_set.add(non_terminal)
            return
        if str(non_terminal) in visited:  # Convert non-terminal to a hashable type
            return

        visited.add(str(non_terminal))  # Convert non-terminal to a hashable type

        

    # def generateFollowSet(self, cfg: dict):
    #     fs = {}
    #     for key in cfg.keys():
    #         fs[key] = self.followSet(cfg, key)
    #     return fs
    def calculate_follow_set(self, cfg, symbol):
        follow_set = set()
        for non_terminal, productions in cfg.items():
            for production in productions:
                if symbol in production:
                    index = production.index(symbol)
                    if index < len(production) - 1:
                        follow_set |= self.firstSet(cfg, production[index + 1]) 
                        if 'ε' not in self.firstSet(cfg, production[index + 1]):
                            continue
                        if non_terminal != symbol:
                            follow_set |= self.calculate_follow_set(cfg, non_terminal)
                            break
        return follow_set

        # Example usage
        

        # self.follow_sets = {key: set() for key in cfg.keys()}

        # changed = True
        # while changed:
        #     changed = False
        #     for key in cfg.keys():
        #         for production in cfg[key]:
        #             for i, symbol in enumerate(production):
        #                 if symbol == followOf:
        #                     changed = changed or bool( self.updateFollowSet(cfg, key, production, i))

        # return list(self.follow_sets[followOf])

    # def updateFollowSet(self, cfg, non_terminal, production, index):
    #     changed = False
    #     for i in range(index + 1, len(production)):
    #         current_symbol = production[i]

    #         if current_symbol in const.terminals:
    #             changed = changed or bool( self.follow_sets[non_terminal].add(current_symbol))
    #             break
    #         elif current_symbol in cfg.keys():
    #             changed = changed or bool( self.follow_sets[non_terminal].update(self.firstSet(cfg, current_symbol)))
    #             if '' not in self.firstSet(cfg, current_symbol):
    #                 break
    #         else:
    #             break

    #     if index == len(production) - 1 or all(x in Grammar.cfg.keys() for x in production[index + 1:]):
    #         # Non-terminal is at the end or follows another non-terminal
    #         changed = changed or bool( self.follow_sets[non_terminal].update(self.follow_sets[production[index]]))

    #     return changed

class ParseNonTerminal:
    # Parser based on recursive descent. Takes a string of tokens and a grammar, returns a parse tree.
#     Recursive descent parsing is a top-down parsing technique used to analyze the structure of a given input based on a formal grammar. It starts from the top-level rule of the grammar and recursively applies production rules to break down the input into smaller components until it reaches the terminal symbols.
# Here are the steps involved in the recursive descent parsing algorithm:

# Define the grammar: Start by defining a formal grammar that describes the syntax of the language you want to parse. The grammar consists of a set of production rules that define how the language constructs can be formed.

# Implement the parser functions: Create a set of parsing functions, one for each non-terminal symbol in the grammar. Each parsing function corresponds to a production rule and is responsible for recognizing and parsing the corresponding language construct.

# Start with the top-level rule: Begin the parsing process by calling the parsing function for the top-level rule of the grammar. This function will recursively call other parsing functions to handle the sub-components of the input.
    def __init__(self, non_terminal, production, index):
        self.non_terminal = non_terminal
        self.production = production
        self.index = index

    def move(self):
        return self.production[self.index]
    
class MathParser():
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        return self.expression()

    def expression(self):
        return self.term() + self.expression_prime()

    def expression_prime(self):
        if self.tokens[self.index] in ["+", "-"]:
            operator = self.tokens[self.index]
            self.move()
            return [operator] + self.term() + self.expression_prime()
        else:
            return []

    def term(self):
        return self.factor() + self.term_prime()

    def term_prime(self):
        if self.tokens[self.index] in ["*", "/"]:
            operator = self.tokens[self.index]
            self.move()
            return [operator] + self.factor() + self.term_prime()
        else:
            return []

    def factor(self):
        if self.tokens[self.index] == "(":
            self.move()
            result = self.expression()
            if self.tokens[self.index] == ")":
                self.move()
                return result
            else:
                raise SyntaxError("Missing closing parenthesis")
        elif self.tokens[self.index].isdigit():
            result = self.tokens[self.index]
            self.move()
            return result
        else:
            raise SyntaxError("Invalid expression")

    def move(self):
        self.index += 1

    # def



class Grammar:
    cfg={}
    cfg["program"]	=	[["import","global_declaration","function_definition","sheesh_declaration","function_definition",""]]
    cfg["import"]	=	[["use","import_prog","import_next","#","more_import",""]]
    cfg["import"]	.append	([None])
    cfg["more_import"]	=	[["import",""]]
    cfg["more_import"]	.append	([None])
    cfg["import_prog"]	=	[["identifier","more_importprog",""]]
    cfg["more_importprog"]	=	[[",","import_prog",""]]
    cfg["more_importprog"]	.append	([None])
    cfg["import_next"]	=	[["from","identifier"]]
    cfg["import_next"]	.append	([None])
    cfg["global_declaration"]	=	[["global_statement","global_declaration",""]]
    cfg["global_declaration"]	.append	([None])
    cfg["global_statement"]	=	[["variable_declaration",""]]
    cfg["global_statement"]	.append	(["function_prototype",""])
    cfg["global_statement"]	.append	(["constant_declaration",""])
    cfg["global_statement"]	.append	(["sequence_declaration",""])
    cfg["function_prototype"]	=	[["yeet_type","identifier","(","parameter",")","#"]]
    cfg["parameter"]	=	[["data_type","identifier","more_param",""]]
    cfg["parameter"]	.append	(["blank"])
    cfg["parameter"]	.append	([None])
    cfg["more_param"]	=	[[",","data_type","identifier","more_param",""]]
    cfg["more_param"]	.append	([None])
    cfg["yeet_type"]	=	[["data_type",""]]
    cfg["yeet_type"]	.append	(["blank"])
    cfg["data_type"]	=	[["whole"]]
    cfg["data_type"]	.append	(["dec"])
    cfg["data_type"]	.append	(["text"])
    cfg["data_type"]	.append	(["sus"])
    cfg["data_type"]	.append	(["charr","text"])
    cfg["literal"]	=	[["text_literal"]]
    cfg["literal"]	.append	(["whole_literal"])
    cfg["literal"]	.append	(["dec_literal"])
    cfg["literal"]	.append	(["sus_literal"])
    cfg["literal"]	.append	(["charr_literal"])
    cfg["numeric_value"]	=	[["common_val",""]]
    cfg["numeric_value"]	.append	(["whole_literal"])
    cfg["numeric_value"]	.append	(["dec_literal"])
    cfg["numeric_value"]	.append	(["seq_use",""])
    cfg["sheesh_declaration"]	=	[["sheesh(){","statement","}"]]
    cfg["statement"]	=	[["single_statement","more_statement",""]]
    cfg["single_statement"]	=	[["variable_declaration",""]]
    cfg["single_statement"]	.append	(["sequence_declaration",""])
    cfg["single_statement"]	.append	(["function_invocation","#"])
    cfg["single_statement"]	.append	(["control_flow_statement",""])
    cfg["single_statement"]	.append	(["yeet_statement",""])
    cfg["single_statement"]	.append	(["io_statement",""])
    cfg["single_statement"]	.append	(["seq_use_assign",""])
    cfg["single_statement"]	.append	(["variable_reassign","#"])
    cfg["more_statement"]	=	[["statement",""]]
    cfg["more_statement"]	.append	([None])
    cfg["io_statement"]	=	[["pa_mine_statement",""]]
    cfg["io_statement"]	.append	(["up_statement",""])
    cfg["pa_mine_statement"]	=	[["pa_mine(","argument",")#"]]
    cfg["up_statement"]	=	[["up(","func_argument",")#"]]
    cfg["variable_declaration"]	=	[["data_type","vardec_tail","#"]]
    cfg["vardec_tail"]	=	[["identifier","variable_assign","more_vardec",""]]
    cfg["more_vardec"]	=	[[",","vardec_tail",""]]
    cfg["more_vardec"]	.append	([None])
    cfg["variable_assign"]	=	[[":=","assign_value",""]]
    cfg["variable_assign"]	.append	([None])
    cfg["variable_reassign"]	=	[["identifier","assign_op","assign_value",""]]
    cfg["common_val"]	=	[["identifier"]]
    cfg["common_val"]	.append	(["function_invocation",""])
    cfg["assign_value"]	=	[["common_val",""]]
    cfg["assign_value"]	.append	(["literal",""])
    cfg["assign_value"]	.append	(["expression",""])
    cfg["assign_value"]	.append	(["seq_use",""])
    cfg["charr_declaration"]	=	[["charr","text","identifier","=","assign_value","#"]]
    cfg["constant_declaration"]	=	[["const_var",""]]
    cfg["constant_declaration"]	.append	(["const_seq",""])
    cfg["const_seq"]	=	[["based","data_type","identifier","seq_one_dim","=","seq_init","#"]]
    cfg["const_var"]	=	[["based","data_type","const_tail","#"]]
    cfg["const_tail"]	=	[["identifier","=","assign_value","more_const",""]]
    cfg["more_const"]	=	[[",","const_tail",""]]
    cfg["more_const"]	.append	([None])
    cfg["assign_op"]	=	[[":="]]
    cfg["assign_op"]	.append	([":+="])
    cfg["assign_op"]	.append	(["-="])
    cfg["assign_op"]	.append	(["*="])
    cfg["assign_op"]	.append	(["/="])
    cfg["assign_op"]	.append	(["%="])
    cfg["function_invocation"]	=	[["identifier","(","func_argument",")"]]
    cfg["func_argument"]	=	[["argument",""]]
    cfg["func_argument"]	.append	([None])
    cfg["argument"]	=	[["args_value","more_args",""]]
    cfg["args_value"]	=	[["assign_value",""]]
    cfg["more_args"]	=	[[",","argument",""]]
    cfg["more_args"]	.append	([None])
    cfg["control_flow_statement"]	=	[["kung_statement","more_control_flow",""]]
    cfg["control_flow_statement"]	.append	(["choose_statement",""])
    cfg["control_flow_statement"]	.append	(["looping_statement",""])
    cfg["kung_statement"]	=	[["kung","(","condition",")","{","statement","}"]]
    cfg["ehkung_statement"]	=	[["ehkung","(","condition",")","{","statement","}"]]
    cfg["deins_statement"]	=	[["deins","{","statement","}"]]
    cfg["more_control_flow"]	=	[["ehkung_statement","more_control_flow",""]]
    cfg["more_control_flow"]	.append	(["deins_statement",""])
    cfg["more_control_flow"]	.append	([None])
    cfg["choose_statement"]	=	[["choose","(","identifier",")","{","when_statement","choose_default","}"]]
    cfg["when_statement"]	=	[["when","literal","::","statement_for_choose","more_when",""]]
    cfg["statement_for_choose"]	=	[["statement",""]]
    cfg["statement_for_choose"]	.append	(["felloff#"])
    cfg["more_when"]	=	[["when_statement",""]]
    cfg["more_when"]	.append	([None])
    cfg["choose_default"]	=	[["default","::","statement_for_choose",""]]
    cfg["choose_default"]	.append	([None])
    cfg["looping_statement"]	=	[["bet_statement",""]]
    cfg["looping_statement"]	.append	(["for_statement",""])
    cfg["habang_statement"]	=	[["bet","{","within_loop_statement","}","kung(","condition",")#"]]
    cfg["for_statement"]	=	[["for(","identifier","=","for_initial_val","to","end_val","step_statement",")","{","within_loop_statement","}"]]
    cfg["for_initial_val"]	=	[["whole_literal"]]
    cfg["for_initial_val"]	.append	(["common_val",""])
    cfg["for_initial_val"]	.append	(["arithmetic_expression",""])
    cfg["for_initial_val"]	.append	(["seq_use",""])
    cfg["step_statement"]	=	[["step","for_initial_val",""]]
    cfg["step_statement"]	.append	([None])
    cfg["within_loop_statement"]	=	[["kung_statement","loop_more_control_flow",""]]
    cfg["within_loop_statement"]	.append	(["ehkung_statement","loop_more_control_flow",""])
    cfg["within_loop_statement"]	.append	(["deins_statement",""])
    cfg["within_loop_statement"]	.append	([None])
    cfg["loop_kung"]	=	[["kung","(","condition",")","{","has_loop_control","}"]]
    cfg["loop_ehkung"]	=	[["ehkung","(","condition",")","{","has_loop_control","}"]]
    cfg["loop_deins"]	=	[["deins","{","has_loop_control","}"]]
    cfg["loop_more_control_flow"]	=	[["loop_ehkung","more_control_flow",""]]
    cfg["loop_more_control_flow"]	.append	(["loop_deins",""])
    cfg["loop_more_control_flow"]	.append	([None])
    cfg["has_loop_control"]	=	[["statement",""]]
    cfg["has_loop_control"]	.append	(["loop_control_statement","more_statement",""])
    cfg["loop_control_statement"]	=	[["felloff#"]]
    cfg["loop_control_statement"]	.append	(["pass#"])
    cfg["loop_control_statement"]	.append	([None])
    cfg["condition"]	=	[["relational_expression",""]]
    cfg["condition"]	.append	(["logical_expression",""])
    cfg["condition"]	.append	(["lit_literal"])
    cfg["condition"]	.append	(["common_val",""])
    cfg["condition"]	.append	(["function_invocation",""])
    cfg["sequence_declaration"]	=	[["data_type","identifier","seq_tail","#"]]
    cfg["seq_tail"]	=	[["seq_one_dim","seq_assign",""]]
    cfg["seq_tail"]	.append	(["multi_seq",""])
    cfg["seq_assign"]	=	[[":=","seq_init",""]]
    cfg["seq_assign"]	.append	([None])
    cfg["seq_init"]	=	[["{","seq_elem","}"]]
    cfg["seq_elem"]	=	[["seq_elem_value",""]]
    cfg["seq_elem"]	.append	(["seq_init","seq_two-d_init",""])
    cfg["seq_two-d_init"]	=	[[",","seq_init","seq_three-d_init",""]]
    cfg["seq_three-d_init"]	=	[[",","seq_init",""]]
    cfg["seq_two-d_init"]	.append	([None])
    cfg["seq_three-d_init"]	.append	([None])
    cfg["seq_elem_value"]	=	[["literal","next_elem_value",""]]
    cfg["next_elem_value"]	=	[[",","seq_elem_value",""]]
    cfg["next_elem_value"]	.append	([None])
    cfg["multi_seq"]	=	[["seq_one_dim","more_seq",""]]
    cfg["more_seq"]	=	[[",identifier","seq_one_dim","more_seq",""]]
    cfg["more_seq"]	.append	([None])
    cfg["seq_one_dim"]	=	[["index","seq_two_dim",""]]
    cfg["seq_two_dim"]	=	[["index","seq_three_dim",""]]
    cfg["seq_three_dim"]	=	[["index",""]]
    cfg["seq_two_dim"]	.append	([None])
    cfg["seq_three_dim"]	.append	([None])
    cfg["index"]	=	[["[","seq_index_val","]"]]
    cfg["seq_index_val"]	=	[["function_invocation",""]]
    cfg["seq_index_val"]	.append	(["identifier"])
    cfg["seq_index_val"]	.append	(["whole_literal"])
    cfg["seq_index_val"]	.append	(["arithmetic_expression",""])
    cfg["seq_use"]	=	[["identifier","seq_one_dim",""]]
    cfg["seq_use_assign"]	=	[["seq_use","assign_op","assign_value","#"]]
    cfg["expression"]	=	[["arithmetic_expression",""]]
    cfg["expression"]	.append	(["logical_expression",""])
    cfg["expression"]	.append	(["relational_expression",""])
    cfg["expression"]	.append	(["text_concat",""])
    cfg["arithmetic_expression"]	=	[["arithm_term","arithm_tail",""]]
    cfg["arithm_term"]	=	[["arithm_factor","arithm_term_tail",""]]
    cfg["arithm_factor"]	=	[["numerical_value",""]]
    cfg["arithm_factor"]	.append	(["(","arithmetic_expression",")"])
    cfg["arithm_tail"]	=	[["add_op","arithm_term","arithm_term_tail",""]]
    cfg["arithm_tail"]	.append	([None])
    cfg["arithm_term_tail"]	=	[["mult_op","arithm_factor","arithm_term_tail",""]]
    cfg["arithm_term_tail"]	.append	([None])
    cfg["add_op"]	=	[[":+"]]
    cfg["add_op"]	.append	([":-"])
    cfg["mult_op"]	=	[[":*"]]
    cfg["mult_op"]	.append	([":/"])
    cfg["mult_op"]	.append	([":%"])
    cfg["relational_expression"]	=	[["numeric_value","relop","numeric_value",""]]
    cfg["relational_expression"]	.append	(["charr_val","==","charr_val",""])
    cfg["charr_val"]	=	[["common_val",""]]
    cfg["charr_val"]	.append	(["charr_literal"])
    cfg["relop"]	=	[[":=="]]
    cfg["relop"]	.append	([""])
    cfg["relop"]	.append	(["="])
    cfg["relop"]	.append	([""])
    cfg["relop"]	.append	(["="])
    cfg["relop"]	.append	(["!="])
    cfg["logical_expression"]	=	[["logic_term","logic_tail",""]]
    cfg["logic_term"]	=	[["logic_factor","logic_term_tail",""]]
    cfg["logic_factor"]	=	[["logic_value",""]]
    cfg["logic_factor"]	.append	(["logical_not_expression",""])
    cfg["logic_factor"]	.append	(["(","logical_expression",")"])
    cfg["logic_tail"]	=	[["|","logic_term","logic_tail",""]]
    cfg["logic_tail"]	.append	([None])
    cfg["logic_term_tail"]	=	[["&","logic_factor","logic_term_tail",""]]
    cfg["logic_term_tail"]	.append	([None])
    cfg["logical_not_expression"]	=	[["logic_not","logic_not_tail",""]]
    cfg["logic_not_tail"]	=	[["logical_not_expression",""]]
    cfg["logic_not_tail"]	.append	(["identifier"])
    cfg["logic_not"]	=	[["!"]]
    cfg["logic_value"]	=	[["common_val",""]]
    cfg["logic_value"]	.append	(["sus_literal"])
    cfg["logic_value"]	.append	(["relational_expression",""])
    cfg["logic_value"]	.append	(["seq_use",""])
    cfg["logic_value"]	.append	(["logical_not_expression",""])
    cfg["text_concat"]	=	[["concat_val","concat_tail",""]]
    cfg["concat_tail"]	=	[["...","concat_val","more_concat",""]]
    cfg["more_concat"]	=	[["concat_tail",""]]
    cfg["more_concat"]	.append	([None])
    cfg["concat_val"]	=	[["text_literal"]]
    cfg["concat_val"]	.append	(["common_val",""])
    cfg["concat_val"]	.append	(["seq_use",""])
    cfg["function_definition"]	=	[["func_def","more_funcdef",""]]
    cfg["function_definition"]	.append	([None])
    cfg["func_def"]	=	[["yeet_type","identifier","(","parameter","){","statement","}"]]
    cfg["more_funcdef"]	=	[["function_definition",""]]
    cfg["more_funcdef"]	.append	([None])
    cfg["yeet_statement"]	=	[["yeet","return_value","#"]]
    cfg["yeet_statement"]	.append	([None])
    cfg["return_value"]	=	[["assign_value",""]]
    cfg["return_value"]	.append	([None])





# print(FirstFollow().firstSet(Grammar.cfg, "sheesh_declaration"))
# print(FirstFollowPredict.cfg))
print(FirstFollowPredict().firstSet(Grammar.cfg, 'program')     )
# print(Grammar.cfg)
