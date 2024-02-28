EMPTY_CHAIN = None
END_MARKER = '\0'

def compute_sets(rules):
    first_sets = {}
    follow_sets = {}
    predict_sets = {}

    for rule in rules:
        left = rule['left']
        first_sets[left] = []
        follow_sets[left] = []

    first_sets = make_first_sets()
    follow_sets = make_follow_sets()
    predict_sets = make_predict_sets()

    return  first_sets, follow_sets, predict_sets

def union(arr1, arr2):
    return list(set(arr1 + arr2))

def is_nonterminal(item, first_sets):
    return item in first_sets

def collect_set(initial_set, items, additional_set, first_sets):
    set_result = initial_set

    for index, item in enumerate(items):
        if is_nonterminal(item, first_sets):
            set_result = union(set_result, [set_item for set_item in first_sets[item] if set_item != EMPTY_CHAIN])

            if EMPTY_CHAIN in first_sets[item]:
                set_result = union(set_result, additional_set)
        else:
            set_result = union(set_result, [item])

    return set_result

def make_first_sets(rules, first_sets):
    is_set_changed = True

    while is_set_changed:
        is_set_changed = False

        for rule in rules:
            left, right = rule['left'], rule['right']
            first_sets[left]=right
            set_result = first_sets[left]
            set_result = union(set_result, collect_set(set_result, right, [EMPTY_CHAIN], first_sets))

            if len(first_sets[left]) != len(set_result):
                first_sets[left] = set_result
                is_set_changed = True

    return first_sets

def make_follow_sets(rules, follow_sets):
    follow_sets[rules[0]['left']].append(END_MARKER)
    is_set_changed = True

    while is_set_changed:
        is_set_changed = False

        for rule in rules:
            left, right = rule['left'], rule['right']

            for index, item in enumerate(right):
                if not is_nonterminal(item):
                    continue

                set_result = follow_sets[item]
                set_result = union(
                    set_result,
                    collect_set(set_result, right[index + 1:], follow_sets[left]) if index + 1 < len(right) else follow_sets[left]
                )

                if len(follow_sets[item]) != len(set_result):
                    follow_sets[item] = set_result
                    is_set_changed = True

    return follow_sets

def make_predict_sets(rules, follow_sets, predict_sets):
    for rule_index, rule in enumerate(rules):
        left, right = rule['left'], rule['right']
        first_item = right[0]
        set_result = []

        if is_nonterminal(first_item):
            set_result = union(set_result, collect_set(set_result, right, follow_sets[left]))
        elif first_item == EMPTY_CHAIN:
            set_result = follow_sets[left][:]
        else:
            set_result.append(first_item)

        predict_sets[rule_index + 1] = set_result

    return predict_sets

    

productions = [
    {"left": "program", "right": ["import", "global_declaration", "function_definition", "sheesh_declaration", "function_definition"]},
    {"left": "import", "right": ["use", "import_prog", "import_next", "#", "more_import"]},
    {"left": "import", "right": [None]},
    {"left": "more_import", "right": ["import"]},
    {"left": "more_import", "right": [None]},
    {"left": "import_prog", "right": ["identifier", "more_importprog"]},
    {"left": "more_importprog", "right": [",", "import_prog"]},
    {"left": "more_importprog", "right": [None]},
    {"left": "import_next", "right": ["from", "identifier"]},
    {"left": "import_next", "right": [None]},
    {"left": "global_declaration", "right": ["global_statement", "global_declaration"]},
    {"left": "global_declaration", "right": [None]},
    {"left": "global_statement", "right": ["variable_declaration"]},
    {"left": "global_statement", "right": ["function_prototype"]},
    {"left": "global_statement", "right": ["constant_declaration"]},
    {"left": "global_statement", "right": ["sequence_declaration"]},
    {"left": "function_prototype", "right": ["yeet_type", "identifier", "(", "parameter", ")", "#"]},
    {"left": "parameter", "right": ["data_type", "identifier", "more_param"]},
    {"left": "parameter", "right": ["blank"]},
    {"left": "parameter", "right": [None]},
    {"left": "more_param", "right": [",", "data_type", "identifier", "more_param"]},
    {"left": "more_param", "right": [None]},
    {"left": "yeet_type", "right": ["data_type"]},
    {"left": "yeet_type", "right": ["blank"]},
    {"left": "data_type", "right": ["whole"]},
    {"left": "data_type", "right": ["dec"]},
    {"left": "data_type", "right": ["text"]},
    {"left": "data_type", "right": ["sus"]},
    {"left": "data_type", "right": ["charr", "text"]},
    {"left": "literal", "right": ["text_literal"]},
    {"left": "literal", "right": ["whole_literal"]},
    {"left": "literal", "right": ["dec_literal"]},
    {"left": "literal", "right": ["sus_literal"]},
    {"left": "literal", "right": ["charr_literal"]},
    {"left": "numeric_value", "right": ["common_val"]},
    {"left": "numeric_value", "right": ["whole_literal"]},
    {"left": "numeric_value", "right": ["dec_literal"]},
    {"left": "numeric_value", "right": ["seq_use"]},
    {"left": "sheesh_declaration", "right": ["sheesh","(",")","{", "statement", "}"]},
    {"left": "statement", "right": ["single_statement", "more_statement"]},
    {"left": "single_statement", "right": ["variable_declaration"]},
    {"left": "single_statement", "right": ["sequence_declaration"]},
    {"left": "single_statement", "right": ["function_invocation", "#"]},
    {"left": "single_statement", "right": ["control_flow_statement"]},
    {"left": "single_statement", "right": ["yeet_statement"]},
    {"left": "single_statement", "right": ["io_statement"]},
    {"left": "single_statement", "right": ["seq_use_assign"]},
    {"left": "single_statement", "right": ["variable_reassign", "#"]},
    {"left": "more_statement", "right": ["statement"]},
    {"left": "more_statement", "right": [None]},
    {"left": "io_statement", "right": ["pa_mine_statement"]},
    {"left": "io_statement", "right": ["up_statement"]},
    {"left": "pa_mine_statement", "right": ["pa_mine","(", "argument", ")", "#"]},
    {"left": "up_statement", "right": ["up","(", "func_argument", ")", "#"]},
    {"left": "variable_declaration", "right": ["data_type", "vardec_tail", "#"]},
    {"left": "vardec_tail", "right": ["identifier", "variable_assign", "more_vardec"]},
    {"left": "more_vardec", "right": [",", "vardec_tail"]},
    {"left": "more_vardec", "right": [None]},
    {"left": "variable_assign", "right": ["=", "assign_value"]},
    {"left": "variable_assign", "right": [None]},
    {"left": "variable_reassign", "right": ["identifier", "assign_op", "assign_value"]},
    {"left": "common_val", "right": ["identifier"]},
    {"left": "common_val", "right": ["function_invocation"]},
    {"left": "assign_value", "right": ["common_val"]},
    {"left": "assign_value", "right": ["literal"]},
    {"left": "assign_value", "right": ["expression"]},
    {"left": "assign_value", "right": ["seq_use"]},
    {"left": "charr_declaration", "right": ["charr", "text", "identifier", "=", "assign_value", "#"]},
    {"left": "constant_declaration", "right": ["const_var"]},
    {"left": "constant_declaration", "right": ["const_seq"]},
    {"left": "const_seq", "right": ["based", "data_type", "identifier", "seq_one_dim", "=", "seq_init", "#"]},
    {"left": "const_var", "right": ["based", "data_type", "const_tail", "#"]},
    {"left": "const_tail", "right": ["identifier", "=", "assign_value", "more_const"]},
    {"left": "more_const", "right": [",", "const_tail"]},
    {"left": "more_const", "right": [None]},
    {"left": "assign_op", "right": ["="]},
    {"left": "assign_op", "right": ["+="]},
    {"left": "assign_op", "right": ["-="]},
    {"left": "assign_op", "right": ["*="]},
    {"left": "assign_op", "right": ["/="]},
    {"left": "assign_op", "right": ["%="]},
    {"left": "function_invocation", "right": ["identifier", "(", "func_argument", ")"]},
    {"left": "func_argument", "right": ["argument"]},
    {"left": "func_argument", "right": [None]},
    {"left": "argument", "right": ["args_value", "more_args"]},
    {"left": "args_value", "right": ["assign_value"]},
    {"left": "more_args", "right": [",", "argument"]},
    {"left": "more_args", "right": [None]},
    {"left": "control_flow_statement", "right": ["kung_statement", "more_control_flow"]},
    {"left": "control_flow_statement", "right": ["choose_statement"]},
    {"left": "control_flow_statement", "right": ["looping_statement"]},
    {"left": "kung_statement", "right": ["kung", "(", "condition", ")", "{", "statement", "}"]},
    {"left": "ehkung_statement", "right": ["ehkung", "(", "condition", ")", "{", "statement", "}"]},
    {"left": "deins_statement", "right": ["deins", "{", "statement", "}"]},
    {"left": "more_control_flow", "right": ["ehkung_statement", "more_control_flow"]},
    {"left": "more_control_flow", "right": ["deins_statement"]},
    {"left": "more_control_flow", "right": [None]},
    {"left": "choose_statement", "right": ["choose", "(", "identifier", ")", "{", "when_statement", "choose_default", "}"]},
    {"left": "when_statement", "right": ["when", "literal", "::", "statement_for_choose", "more_when"]},
    {"left": "statement_for_choose", "right": ["statement"]},
    {"left": "statement_for_choose", "right": ["felloff", "#"]},
    {"left": "more_when", "right": ["when_statement"]},
    {"left": "more_when", "right": [None]},
    {"left": "choose_default", "right": ["default", "::", "statement_for_choose"]},
    {"left": "choose_default", "right": [None]},
    {"left": "looping_statement", "right": ["bet_statement"]},
    {"left": "looping_statement", "right": ["for_statement"]},
    {"left": "habang_statement", "right": ["bet", "{", "within_loop_statement", "}", "kung", "(", "condition", ")", "#"]},
    {"left": "for_statement", "right": ["for", "(", "identifier", "=", "for_initial_val", "to", "end_val", "step_statement", ")", "{", "within_loop_statement", "}"]},
    {"left": "for_initial_val", "right": ["whole_literal"]},
    {"left": "for_initial_val", "right": ["common_val"]},
    {"left": "for_initial_val", "right": ["arithmetic_expression"]},
    {"left": "for_initial_val", "right": ["seq_use"]},
    {"left": "step_statement", "right": ["step", "for_initial_val"]},
    {"left": "step_statement", "right": [None]},
    {"left": "within_loop_statement", "right": ["kung_statement", "loop_more_control_flow"]},
    {"left": "within_loop_statement", "right": ["ehkung_statement", "loop_more_control_flow"]},
    {"left": "within_loop_statement", "right": ["deins_statement"]},
    {"left": "within_loop_statement", "right": [None]},
    {"left": "loop_kung", "right": ["kung", "(", "condition", ")", "{", "has_loop_control", "}"]},
    {"left": "loop_ehkung", "right": ["ehkung", "(", "condition", ")", "{", "has_loop_control", "}"]},
    {"left": "loop_deins", "right": ["deins", "{", "has_loop_control", "}"]},
    {"left": "loop_more_control_flow", "right": ["loop_ehkung", "more_control_flow"]},
    {"left": "loop_more_control_flow", "right": ["loop_deins"]},
    {"left": "loop_more_control_flow", "right": [None]},
    {"left": "has_loop_control", "right": ["statement"]},
    {"left": "has_loop_control", "right": ["loop_control_statement", "more_statement"]},
    {"left": "loop_control_statement", "right": ["felloff", "#"]},
    {"left": "loop_control_statement", "right": ["pass", "#"]},
    {"left": "loop_control_statement", "right": [None]},
    {"left": "condition", "right": ["relational_expression"]},
    {"left": "condition", "right": ["logical_expression"]},
    {"left": "condition", "right": ["lit_literal"]},
    {"left": "condition", "right": ["common_val"]},
    {"left": "condition", "right": ["function_invocation"]},
    {"left": "sequence_declaration", "right": ["data_type", "identifier", "seq_tail", "#"]},
    {"left": "seq_tail", "right": ["seq_one_dim", "seq_assign"]},
    {"left": "seq_tail", "right": ["multi_seq"]},
    {"left": "seq_assign", "right": ["=", "seq_init"]},
    {"left": "seq_assign", "right": [None]},
    {"left": "seq_init", "right": ["{", "seq_elem", "}"]},
    {"left": "seq_elem", "right": ["seq_elem_value"]},
    {"left": "seq_elem", "right": ["seq_init", "seq_two-d_init"]},
    {"left": "seq_two-d_init", "right": [",", "seq_init", "seq_three-d_init"]},
    {"left": "seq_three-d_init", "right": [",", "seq_init"]},
    {"left": "seq_two-d_init", "right": [None]},
    {"left": "seq_three-d_init", "right": [None]},
    {"left": "seq_elem_value", "right": ["literal", "next_elem_value"]},
    {"left": "next_elem_value", "right": [",", "seq_elem_value"]},
    {"left": "next_elem_value", "right": [None]},
    {"left": "multi_seq", "right": ["seq_one_dim", "more_seq"]},
    {"left": "more_seq", "right": [",", "identifier", "seq_one_dim", "more_seq"]},
    {"left": "more_seq", "right": [None]},
    {"left": "seq_one_dim", "right": ["index", "seq_two_dim"]},
    {"left": "seq_two_dim", "right": ["index", "seq_three_dim"]},
    {"left": "seq_three_dim", "right": ["index"]},
    {"left": "seq_two_dim", "right": [None]},
    {"left": "seq_three_dim", "right": [None]},
    {"left": "index", "right": ["[", "seq_index_val", "]"]},
    {"left": "seq_index_val", "right": ["function_invocation"]},
    {"left": "seq_index_val", "right": ["identifier"]},
    {"left": "seq_index_val", "right": ["whole_literal"]},
    {"left": "seq_index_val", "right": ["arithmetic_expression"]},
    {"left": "seq_use", "right": ["identifier", "seq_one_dim"]},
    {"left": "seq_use_assign", "right": ["seq_use", "assign_op", "assign_value", "#"]},
    {"left": "expression", "right": ["arithmetic_expression"]},
    {"left": "expression", "right": ["logical_expression"]},
    {"left": "expression", "right": ["relational_expression"]},
    {"left": "expression", "right": ["text_concat"]},
    {"left": "arithmetic_expression", "right": ["arithm_term", "arithm_tail"]},
    {"left": "arithm_term", "right": ["arithm_factor", "arithm_term_tail"]},
    {"left": "arithm_factor", "right": ["numerical_value"]},
    {"left": "arithm_factor", "right": ["(", "arithmetic_expression", ")"]},
    {"left": "arithm_tail", "right": ["add_op", "arithm_term", "arithm_term_tail"]},
    {"left": "arithm_tail", "right": [None]},
    {"left": "arithm_term_tail", "right": ["mult_op", "arithm_factor", "arithm_term_tail"]},
    {"left": "arithm_term_tail", "right": [None]},
    {"left": "add_op", "right": ["+", "-"]},
    {"left": "mult_op", "right": ["*", "/", "%"]},
    {"left": "relational_expression", "right": ["numeric_value", "relop", "numeric_value"]},
    {"left": "relational_expression", "right": ["charr_val", "==", "charr_val"]},
    {"left": "charr_val", "right": ["common_val"]},
    {"left": "charr_val", "right": ["charr_literal"]},
    {"left": "relop", "right": ["==", ">", ">=", "<", "<=", "!="]},
    {"left": "logical_expression", "right": ["logic_term", "logic_tail"]},
    {"left": "logic_term", "right": ["logic_factor", "logic_term_tail"]},
    {"left": "logic_factor", "right": ["logic_value"]},
    {"left": "logic_factor", "right": ["logical_not_expression"]},
    {"left": "logic_factor", "right": ["(", "logical_expression", ")"]},
    {"left": "logic_tail", "right": ["|", "logic_term", "logic_tail"]},
    {"left": "logic_tail", "right": [None]},
    {"left": "logic_term_tail", "right": ["&", "logic_factor", "logic_term_tail"]},
    {"left": "logic_term_tail", "right": [None]},
    {"left": "logical_not_expression", "right": ["logic_not", "logic_not_tail"]},
    {"left": "logic_not_tail", "right": ["logical_not_expression"]},
    {"left": "logic_not_tail", "right": ["identifier"]},
    {"left": "logic_not", "right": ["!"]},
    {"left": "logic_value", "right": ["common_val"]},
    {"left": "logic_value", "right": ["sus_literal"]},
    {"left": "logic_value", "right": ["relational_expression"]},
    {"left": "logic_value", "right": ["seq_use"]},
    {"left": "logic_value", "right": ["logical_not_expression"]},
    {"left": "text_concat", "right": ["concat_val", "concat_tail"]},
    {"left": "concat_tail", "right": ["...", "concat_val", "more_concat"]},
    {"left": "more_concat", "right": ["concat_tail"]},
    {"left": "more_concat", "right": [None]},
    {"left": "concat_val", "right": ["text_literal"]},
    {"left": "concat_val", "right": ["common_val"]},
    {"left": "concat_val", "right": ["seq_use"]},
    {"left": "function_definition", "right": ["func_def", "more_funcdef"]},
    {"left": "function_definition", "right": [None]},
    {"left": "func_def", "right": ["yeet_type", "identifier", "(", "parameter", ")", "{", "statement", "}"]},
    {"left": "more_funcdef", "right": ["function_definition"]},
    {"left": "more_funcdef", "right": [None]},
    {"left": "yeet_statement", "right": ["yeet", "return_value", "#"]},
    {"left": "yeet_statement", "right": [None]},
    {"left": "return_value", "right": ["assign_value"]},
    {"left": "return_value", "right": [None]}
]

fs = {}  # Define the variable "fs" before using it
fs = make_first_sets(productions, fs)

print(fs)

