import source.core.constants as const

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
            return self.follow(cfg, non_terminal)

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
        self.computeFirstSet(cfg, firstOf, fs, visited)
        return list(fs)

    def computeFirstSet(self, cfg, non_terminal, first_set, visited):
        if non_terminal in const.terminals:
            first_set.add(non_terminal)
            return
        if str(non_terminal) in visited:  # Convert non-terminal to a hashable type
            return

        visited.add(str(non_terminal))  # Convert non-terminal to a hashable type

        def computeFirstSet(self, cfg, non_terminal, first_set, visited):
            if non_terminal in const.terminals:
                first_set.add(non_terminal)
                return
            if str(non_terminal) in visited:  # Convert non-terminal to a hashable type
                return

            visited.add(str(non_terminal))  # Convert non-terminal to a hashable type

            for production in cfg[non_terminal]:
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

    # def generateFollowSet(self, cfg: dict):
    #     fs = {}
    #     for key in cfg.keys():
    #         fs[key] = self.followSet(cfg, key)
    #     return fs
    def follow(self, cfg, non_terminal):
        pass

    def generateFollowSet(self, cfg: dict):
        self.follow_sets = {key: set() for key in cfg.keys()}

        changed = True
        while changed:
            changed = False
            for key in cfg.keys():
                for production in cfg[key]:
                    for i, symbol in enumerate(production):
                        if symbol in cfg.keys():
                            if i < len(production) - 1:
                                next_symbol = production[i + 1]
                                if next_symbol in cfg.keys():
                                    changed = changed or bool(self.follow_sets[symbol].update(self.firstSet(cfg, next_symbol)))
                                    if '' in self.firstSet(cfg, next_symbol):
                                        changed = changed or bool(self.follow_sets[symbol].update(self.follow_sets[key]))
                                else:
                                    changed = changed or bool(self.follow_sets[symbol].add(next_symbol))
                            else:
                                changed = changed or bool(self.follow_sets[symbol].update(self.follow_sets[key]))

                    if i == len(production) - 1 and '' in self.firstSet(cfg, symbol):
                        changed = changed or bool(self.follow_sets[symbol].update(self.follow_sets[key]))

        for key in cfg.keys():
            self.follow_sets[key].add('$')

        return self.follow_sets
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




class Grammar:
    cfg={}
    cfg["program"]	=	[["import","global_declaration","function_definition","sheesh_declaration","function_definition",]]
    cfg["import"]	=	[["use","import_prog","import_next","#","more_import",]]
    cfg["import"].append	(["null"])
    cfg["import_prog"]	=	[["Identifier","more_importprog",]]
    cfg["more_importprog"]	=	[[",","import_prog",]]
    cfg["more_importprog"]	.append	(["null"])
    cfg["import_next"]	=	[["from","Identifier"]]
    cfg["import_next"]	.append	(["null"])
    cfg["more_import"]	=	[["import",]]
    cfg["more_import"]	.append	(["null"])
    cfg["global_declaration"]	=	[["global_statement","more_globaldec",]]
    cfg["global_declaration"]	.append	(["null"])
    cfg["global_statement"]	=	[["variable_declaration",]]
    cfg["global_statement"]	.append	(["function_prototype",])
    cfg["more_globaldec"]	=	[["global_declaration",]]
    cfg["more_globaldec"]	.append	(["null"])
    cfg["function_prototype"]	=	[["bruh_type","Identifier","(","parameter",")","#"]]
    cfg["parameter"]	=	[["data_type","Identifier","more_param",]]
    cfg["parameter"]	.append	(["blank"])
    cfg["parameter"]	.append	(["null"])
    cfg["more_param"]	=	[[",","data_type","Identifier","more_param",]]
    cfg["more_param"]	.append	(["null"])
    cfg["bruh_type"]	=	[["data_type",]]
    cfg["bruh_type"]	.append	(["blank"])
    cfg["data_type"]	=	[["whole"]]
    cfg["data_type"]	.append	(["dec"])
    cfg["data_type"]	.append	(["text"])
    cfg["data_type"]	.append	(["lit"])
    cfg["literal"]	=	[["text_literal"]]
    cfg["literal"]	.append	(["whole_literal"])
    cfg["literal"]	.append	(["dec_literal"])
    cfg["literal"]	.append	(["lit_literal"])
    cfg["numeric_value"]	=	[["Identifier"]]
    cfg["numeric_value"]	.append	(["whole_literal"])
    cfg["numeric_value"]	.append	(["dec_literal"])
    cfg["numeric_value"]	.append	(["function_invocation",])
    cfg["numeric_value"]	.append	(["seq_use",])
    cfg["sheesh_declaration"]	=	[["sheesh", "(", ")", "{","statement","}"]]
    cfg["statement"]	=	[["single_statement","more_statement",]]
    cfg["single_statement"]	=	[["variable_declaration",]]
    cfg["single_statement"]	.append	(["function_invocation","#"])
    cfg["single_statement"]	.append	(["control_flow_statement",])
    cfg["single_statement"]	.append	(["bruh_statement",])
    cfg["single_statement"]	.append	(["io_statement",])
    cfg["single_statement"]	.append	(["seq_use_assign",])
    cfg["single_statement"].append(["variable_reassign","#"])
    cfg["more_statement"] = [["statement",]]
    cfg["more_statement"].append(["null"])
    cfg["io_statement"] = [["kuha_statement",]]
    cfg["io_statement"].append(["bigay_statement",])
    cfg["kuha_statement"] = [["kuha","(","argument",")","#"]]
    cfg["bigay_statement"] = [["bigay", "(","argument","more_argument",")","#"]]
    cfg["variable_declaration"] = [["data_type","vardec_tail","#"]]
    cfg["variable_declaration"].append(["sequence_declaration",])
    cfg["variable_declaration"].append(["constant_declaration",])
    cfg["vardec_tail"] = [["Identifier","variable_assign","more_vardec",]]
    cfg["more_vardec"] = [[",","vardec_tail",]]
    cfg["more_vardec"].append(["null"])
    cfg["variable_assign"] = [["assign_op","assign_value",]]
    cfg["variable_assign"].append(["null"])
    cfg["variable_reassign"] = [["Identifier","assign_op","assign_value",]]
    cfg["assign_value"] = [["function_invocation",]]
    cfg["assign_value"].append(["Identifier"])
    cfg["assign_value"].append(["literal",])
    cfg["assign_value"].append(["expression",])
    cfg["assign_value"].append(["seq_use",])
    cfg["constant_declaration"] = [["steady","data_type","const_tail","#"]]
    cfg["const_tail"] = [["Identifier","assign_op","assign_value","more_const",]]
    cfg["more_const"] = [[",","const_tail",]]
    cfg["more_const"].append(["null"])
    cfg["assign_op"] = [["="]]
    cfg["assign_op"].append(["+="])
    cfg["assign_op"].append(["-="])
    cfg["assign_op"].append(["*="])
    cfg["assign_op"].append(["/="])
    cfg["assign_op"].append(["%="])
    cfg["function_invocation"] = [["Identifier","(","func_argument",")"]]
    cfg["func_argument"] = [["argument",]]
    cfg["func_argument"].append(["null"])
    cfg["argument"] = [["args_value","more_args",]]
    cfg["args_value"] = [["Identifier"]]
    cfg["args_value"].append(["literal",])
    cfg["args_value"].append(["expression",])
    cfg["args_value"].append(["function_invocation",])
    cfg["args_value"].append(["seq_use",])
    cfg["more_args"] = [[",","argument",]]
    cfg["more_args"].append(["null"])
    cfg["control_flow_statement"] = [["kung_statement","more_control_flow",]]
    cfg["control_flow_statement"].append(["choose_statement",])
    cfg["control_flow_statement"].append(["looping_statement",])
    cfg["kung_statement"] = [["kung","(","condition",")","{","statement","}"]]
    cfg["ehkung_statement"] = [["ehkung","(","condition",")","{","statement","}"]]
    cfg["deins_statement"] = [["deins","{","statement","}"]]
    cfg["more_control_flow"] = [["ehkung_statement","more_control_flow",]]
    cfg["more_control_flow"].append(["deins_statement",])
    cfg["more_control_flow"].append(["null"])
    cfg["choose_statement"] = [["choose","(","Identifier",")","{","when_statement","choose_default","}"]]
    cfg["when_statement"] = [["when","literal","::","statement","more_when",]]
    cfg["more_when"] = [["when_statement",]]
    cfg["more_when"].append(["null"])
    cfg["choose_default"] = [["default","::","statement",]]
    cfg["choose_default"].append(["null"])
    cfg["looping_statement"] = [["habang_statement",]]
    cfg["looping_statement"].append(["for_statement",])
    cfg["habang_statement"] = [["habang","{","within_loop_statement","}","kung","(","condition",")","#"]]
    cfg["for_statement"] = [["for", "(","Identifier","to","for_expr_value","step_statement",")","{","within_loop_statement","}"]]
    cfg["for_expr_value"] = [["whole_literal"]]
    cfg["for_expr_value"].append(["function_invocation",])
    cfg["for_expr_value"].append(["Identifier"])
    cfg["for_expr_value"].append(["arithmetic_expression",])
    cfg["for_expr_value"].append(["seq_use",])
    cfg["step_statement"] = [["step","for_expr_value",]]
    cfg["step_statement"].append(["null"])
    cfg["within_loop_statement"] = [["kung_statement","loop_more_control_flow",]]
    cfg["within_loop_statement"].append(["ehkung_statement","loop_more_control_flow",])
    cfg["within_loop_statement"].append(["deins_statement",])
    cfg["within_loop_statement"].append(["null"])
    cfg["loop_kung"] = [["kung","(","condition",")","{","has_loop_control","}"]]
    cfg["loop_ehkung"] = [["ehkung","(","condition",")","{","has_loop_control","}"]]
    cfg["loop_deins"] = [["deins","{","has_loop_control","}"]]
    cfg["loop_more_control_flow"] = [["loop_ehkung","more_control_flow",]]
    cfg["loop_more_control_flow"].append(["loop_deins",])
    cfg["loop_more_control_flow"].append(["null"])
    cfg["has_loop_control"] = [["statement",]]
    cfg["has_loop_control"].append(["loop_control_statement","more_statement",])
    cfg["loop_control_statement"] = [["termins","#"]]
    cfg["loop_control_statement"].append(["gg", "#"])
    cfg["loop_control_statement"].append(["null"])
    cfg["condition"] = [["relational_expression",]]
    cfg["condition"].append(["logical_expression",])
    cfg["condition"].append(["lit_literal"])
    cfg["condition"].append(["Identifier"])
    cfg["condition"].append(["function_invocation",])
    cfg["condition"].append(["seq_use",])
    cfg["sequence_declaration"] = [["data_type","Identifier","seq_tail","#"]]
    cfg["seq_tail"] = [["seq_one_dim","seq_assign",]]
    cfg["seq_tail"].append(["multi_seq",])
    cfg["seq_assign"] = [["=","seq_init",]]
    cfg["seq_assign"].append(["null"])
    cfg["seq_init"] = [["{","seq_elem","}"]]
    cfg["seq_elem"] = [["seq_elem_value",]]
    cfg["seq_elem"].append(["seq_init","seq_two-d_init",])
    cfg["seq_two-d_init"] = [[",","seq_init","seq_three-d_init",]]
    cfg["seq_three-d_init"] = [[",","seq_init",]]
    cfg["seq_two-d_init"].append(["null"])
    cfg["seq_three-d_init"].append(["null"])
    cfg["seq_elem_value"] = [["literal","next_elem_value",]]
    cfg["next_elem_value"] = [[",","seq_elem_value",]]
    cfg["next_elem_value"].append(["null"])
    cfg["multi_seq"] = [["seq_one_dim","more_seq",]]
    cfg["more_seq"] = [[",","Identifier","seq_one_dim","more_seq",]]
    cfg["more_seq"].append(["null"])
    cfg["seq_one_dim"] = [["index","seq_two_dim",]]
    cfg["seq_two_dim"] = [["index","seq_three_dim",]]
    cfg["seq_three_dim"] = [["index",]]
    cfg["seq_two_dim"].append(["null"])
    cfg["seq_three_dim"].append(["null"])
    cfg["index"] = [["[","seq_index_val","]"]]
    cfg["seq_index_val"] = [["function_invocation","index_arithm_expression",]]
    cfg["seq_index_val"].append(["Identifier","index_arithm_expression",])
    cfg["seq_index_val"].append(["whole_literal","index_arithm_expression",])
    cfg["seq_use"] = [["Identifier","seq_one_dim",]]
    cfg["seq_use_assign"] = [["seq_use","assign_op","assign_value","#"]]
    cfg["index_arithm_expression"] = [["arithm_op","seq_index_val",]]
    cfg["index_arithm_expression"].append(["null"])
    cfg["expression"] = [["arithmetic_expression",]]
    cfg["expression"].append(["logical_expression",])
    cfg["expression"].append(["relational_expression",])
    cfg["expression"].append(["text_concat",])
    cfg["arithmetic_expression"] = [["numeric_value","arithm_tail",]]
    cfg["arithm_tail"] = [["arithm_op","numeric_value","more_arithm",]]
    cfg["more_arithm"] = [["arithm_tail",]]
    cfg["more_arithm"].append(["null"])
    cfg["arithm_op"] = [["+"]]
    cfg["arithm_op"].append(["-"])
    cfg["arithm_op"].append(["*"])
    cfg["arithm_op"].append(["/"])
    cfg["arithm_op"].append(["%"])
    cfg["relational_expression"] = [["numeric_value","relop","numeric_value",]]
    cfg["relop"] = [["=="]]
    cfg["relop"].append([])
    cfg["relop"].append(["="])
    cfg["relop"].append([])
    cfg["relop"].append(["="])
    cfg["relop"].append(["!="])
    cfg["logical_expression"] = [["logic_value","logicexpr_tail",]]
    cfg["logicexpr_tail"] = [["logic_op","logic_value",]] #"more_logicexpr",
    cfg["logical_expression"].append(["logical_not_expression",])
    cfg["more_logical_expr"] = [["logicexpr_tail",]]
    cfg["more_logical_expr"].append(["null"])
    cfg["logical_not_expression"] = [["logic_not","more_logic_not","Identifier"]]
    cfg["more_logic_not"] = [["logic_not","more_logic_not",]]
    cfg["more_logic_not"].append(["null"])
    cfg["logic_not"] = [["!"]]
    cfg["logic_op"] = [["&"]]
    cfg["logic_op"].append(["|"])
    cfg["logic_value"] = [["Identifier"]]
    cfg["logic_value"].append(["lit_literal"])
    cfg["logic_value"].append(["relational_expression",])
    cfg["logic_value"].append(["logical_not_expression",])
    cfg["text_concat"] = [["concat_val","concat_tail",]]
    cfg["concat_tail"] = [["...","concat_val","more_concat",]]
    cfg["more_concat"] = [["concat_tail",]]
    cfg["more_concat"].append(["null"])
    cfg["concat_val"] = [["text_literal"]]
    cfg["concat_val"].append(["function_invocation",])
    cfg["concat_val"].append(["Identifier"])
    cfg["concat_val"].append(["seq_use",])
    cfg["function_definition"] = [["func_def","more_funcdef",]]
    cfg["function_definition"].append(["null"])
    cfg["func_def"] = [["bruh_type","Identifier","(","parameter","){","statement","}"]]
    cfg["more_funcdef"] = [["function_definition",]]
    cfg["more_funcdef"].append(["null"])
    cfg["bruh_statement"] = [["bruh","return_value","#"]]
    cfg["bruh_statement"].append(["null"])
    cfg["return_value"] = [["assign_value",]]
    cfg["return_value"].append(["null"])




# print(FirstFollow().firstSet(Grammar.cfg, "sheesh_declaration"))
# print(FirstFollowPredict().predict_set(Grammar.cfg))
