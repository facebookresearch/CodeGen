# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import javalang
from javalang.tokenizer import Position, Identifier

from codegen_sources.preprocessing.obfuscation.obfuscated_names_generator import (
    ObfuscatedNameType,
    ObfuscatedNamesGenerator,
)

EXCLUDED_TOKENS = {"main"}


def obfuscate(java_program):
    tokens = list(javalang.tokenizer.tokenize(java_program))
    declarations, declarations_per_vartype, calls_to_replace = get_variable_usages(
        java_program
    )
    names_generator = ObfuscatedNamesGenerator()

    # Finding the right tokens for declarations first
    for token_name, dec_list in declarations.items():
        for dec_info in dec_list:
            dec_position = dec_info["position"]

            # TODO could make it O(log(n)) with binary search for find first token
            for i, tok in enumerate([t for t in tokens if t.position >= dec_position]):
                if tok.value == token_name:
                    tok.value = names_generator.get_new_name(
                        token_name, dec_info["var_type"]
                    )
                    # TODO: check type for variable definitions?
                    dec_info["new_name"] = tok.value
                    break

    calls_to_replace_index = 0
    for current_tok_index, tok in enumerate(tokens):
        if calls_to_replace_index < len(calls_to_replace):
            # handle special calls or references to replace
            current_call_to_replace = calls_to_replace[calls_to_replace_index]
            assert current_call_to_replace["var_type"] in ObfuscatedNameType
            relevant_declarations = declarations_per_vartype[
                current_call_to_replace["var_type"]
            ][current_call_to_replace["name"]]
            assert (
                len(relevant_declarations) > 0
            ), "No relevant declarations in special token to replace. It should have been filtered out"
            if tok.position >= current_call_to_replace["position"]:
                calls_to_replace_index += 1
                for advanced_tok_index in range(current_tok_index, len(tokens)):
                    if (
                        tokens[advanced_tok_index].value
                        == current_call_to_replace["name"]
                    ):
                        if (
                            current_call_to_replace["var_type"]
                            == ObfuscatedNameType.FUNCTION
                        ):
                            if current_call_to_replace["qualifier"] is None:
                                # if there is no qualifier, the method is called directly
                                is_replace_candidate = (
                                    advanced_tok_index == 0
                                    or tokens[advanced_tok_index - 1].value != "."
                                )
                            else:
                                # if there is a qualifier, the qualifier should be before the function call
                                qualifier_split = current_call_to_replace[
                                    "qualifier"
                                ].split(".")
                                is_replace_candidate = advanced_tok_index > 2 * len(
                                    qualifier_split
                                )
                                for i, qual in enumerate(qualifier_split[::-1]):
                                    is_replace_candidate = (
                                        is_replace_candidate
                                        and tokens[
                                            advanced_tok_index - (2 * i + 1)
                                        ].value
                                        == "."
                                        and tokens[
                                            advanced_tok_index - (2 * i + 2)
                                        ].value
                                        == qual
                                    )
                            if is_replace_candidate:
                                tokens[
                                    advanced_tok_index
                                ].value = relevant_declarations[0]["new_name"]

        # handle other tokens using the declarations
        if isinstance(tok, Identifier) and tok.value in declarations:
            token_declarations = declarations[tok.value]
            tok_position = tok.position
            previous_declarations = [
                dec
                for dec in token_declarations
                if dec["position"] < tok_position and "new_name" in dec
            ]
            if (
                current_tok_index >= 2
                and tokens[current_tok_index - 1].value == "."
                and tokens[current_tok_index - 2].value == "this"
            ):
                previous_declarations = [
                    dec for dec in previous_declarations if dec["is_field"]
                ]
                if len(previous_declarations) == 0:
                    # fields can be declared after in the file an inherited class
                    previous_declarations = [
                        dec for dec in token_declarations if dec["is_field"]
                    ]

            relevant_declaration = None
            if len(previous_declarations) == 0:
                class_declarations = declarations_per_vartype[ObfuscatedNameType.CLASS][
                    tok.value
                ]
                if len(class_declarations) > 0:
                    relevant_declaration = class_declarations[0]
                else:
                    func_declarations = declarations_per_vartype[
                        ObfuscatedNameType.FUNCTION
                    ][tok.value]
                    if len(func_declarations) > 0:
                        relevant_declaration = func_declarations[0]
            else:
                relevant_declaration = previous_declarations[-1]
            if relevant_declaration is not None:
                tok.value = relevant_declaration["new_name"]

    res_lines = [[]]
    prev_line = 0
    for tok in tokens:
        if tok.position.line > prev_line:
            res_lines.append([])
            prev_line = tok.position.line
        res_lines[-1].append(tok.value)

    return (
        "\n".join([" ".join(line) for line in res_lines]),
        names_generator.get_dictionary(),
    )


def is_position_greater(position1, position2):
    return position1.line > position2.line or (
        position1.line == position2.line and position1.position > position2.position
    )


def is_position_equal(position1, position2):
    return position1.line == position2.line and position1.position == position2.position


def is_position_greater_or_equal(position1, position2):
    return is_position_greater(position1, position2) or is_position_equal(
        position1, position2
    )


def get_variable_usages(java_program):
    declarations = {}
    calls_to_replace = []
    ast = javalang.parse.parse(java_program)

    previous_position = Position(0, 0)
    for path, node in ast:
        # Declarations
        if (
            isinstance(node, javalang.tree.ClassDeclaration)
            or isinstance(node, javalang.tree.InterfaceDeclaration)
            or isinstance(node, javalang.tree.EnumDeclaration)
        ):
            declarations, previous_position = add_declaration_node(
                node.name,
                node.position,
                ObfuscatedNameType.CLASS,
                declarations,
                previous_position,
            )
        if isinstance(node, javalang.tree.MethodDeclaration):
            declarations, previous_position = add_declaration_node(
                node.name,
                node.position,
                ObfuscatedNameType.FUNCTION,
                declarations,
                previous_position,
            )
        if (
            isinstance(node, javalang.tree.LocalVariableDeclaration)
            or isinstance(node, javalang.tree.VariableDeclaration)
            or isinstance(node, javalang.tree.FieldDeclaration)
        ):
            for name in [d.name for d in node.declarators]:
                declarations, previous_position = add_declaration_node(
                    name,
                    node.position,
                    ObfuscatedNameType.VARIABLE,
                    declarations,
                    previous_position,
                    decl_type=node.type.name,
                    is_field=isinstance(node, javalang.tree.FieldDeclaration),
                )
        if isinstance(node, javalang.tree.FormalParameter) or isinstance(
            node, javalang.tree.EnumConstantDeclaration
        ):
            declarations, previous_position = add_declaration_node(
                node.name,
                node.position,
                ObfuscatedNameType.VARIABLE,
                declarations,
                previous_position,
            )

        if isinstance(node, javalang.tree.MethodInvocation):
            calls_to_replace, previous_position = add_node_to_replace(
                node.member,
                node.position,
                ObfuscatedNameType.FUNCTION,
                calls_to_replace,
                previous_position,
                qualifier=node.qualifier,
            )
        if isinstance(node.position, Position):
            previous_position = node.position

    for i in range(len(calls_to_replace) - 1):
        assert calls_to_replace[i]["position"] <= calls_to_replace[i + 1]["position"]
    declarations_per_vartype = {}
    for vartype in ObfuscatedNameType:
        declarations_per_vartype[vartype] = {
            k: [dec for dec in v if dec["var_type"] == vartype]
            for k, v in declarations.items()
        }
    calls_to_replace = [
        call
        for call in calls_to_replace
        if len(declarations_per_vartype[call["var_type"]].get(call["name"], [])) > 0
    ]
    return declarations, declarations_per_vartype, calls_to_replace


def add_declaration_node(
    name,
    position,
    var_type,
    declarations,
    previous_position,
    decl_type=None,
    is_field=False,
):
    if position is None:
        new_positions = Position(previous_position.line, previous_position.column + 1)
        position = previous_position
    else:
        new_positions = position
    if name in EXCLUDED_TOKENS:
        return declarations, position

    declarations[name] = declarations.get(name, []) + [
        {
            "position": new_positions,
            "var_type": var_type,
            "decl_type": decl_type,
            "is_field": is_field,
        }
    ]
    return declarations, position


def add_node_to_replace(
    name, position, var_type, to_replace, previous_position, qualifier=None
):
    if position is None:
        new_positions = Position(previous_position.line, previous_position.column + 1)
        position = previous_position
    else:
        new_positions = position

    if name in EXCLUDED_TOKENS:
        return to_replace, position
    to_replace.append(
        {
            "name": name,
            "position": new_positions,
            "var_type": var_type,
            "qualifier": qualifier,
        }
    )
    return to_replace, position
