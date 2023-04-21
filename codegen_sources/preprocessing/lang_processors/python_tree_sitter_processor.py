# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import re
import uuid
import logging
import itertools
import dataclasses
import typing as tp
from pathlib import Path
from io import BytesIO
import tokenize
import tree_sitter as ts
from codegen_sources.model.src.data.dictionary import (
    ENDBLOCK,
    ENDCLASS,
    ENDFUNC,
)
from codegen_sources.preprocessing.obfuscation import utils_deobfuscation
from codegen_sources.preprocessing.obfuscation.bobskater_obfuscator import (
    obfuscateString,
)
from codegen_sources.preprocessing.obfuscation.utils_deobfuscation import dico_to_string
from . import tree_sitter_processor as tsp
from .python_processor import is_python_2
from .utils import obfuscation_tokens

INDENT = "INDENT"
DEDENT = "DEDENT"
logger = logging.getLogger(__name__)


class PythonTreeSitterProcessor(tsp.TreeSitterLangProcessor):
    def __init__(self, root_folder: Path = tsp.TREE_SITTER_ROOT) -> None:
        spetoken2char = {
            "STOKEN00": "#",
            "STOKEN1": "\\n",
            "STOKEN2": '"""',
            "STOKEN3": "'''",
        }
        char2spetoken = {value: " " + key + " " for key, value in spetoken2char.items()}
        super().__init__(
            ast_nodes_type_string=[
                "string",
                "docstring",
                "comment",
                "string_literal",
                "character_literal",
            ],
            stokens_to_chars=spetoken2char,
            chars_to_stokens=char2spetoken,
            root_folder=root_folder,
            new_line_sensitive=True,
        )

    @property
    def language(self) -> str:
        return "python"  # legacy PythonProcessor uses "py"

    def detokenize_code(self, code: tp.Union[str, tp.List[str]]) -> str:
        # replace recreate lines with \n and appropriate indent / dedent
        # removing indent/ dedent tokens
        # current known issues:
        # - a comment inside a type node would be included in the type
        assert isinstance(code, (str, list))
        if isinstance(code, list):
            code = " ".join(code)
        code = code.replace("ENDCOM", tsp.NEWLINE_TOK)
        code = code.replace(ENDBLOCK, "").replace(ENDFUNC, "").replace(ENDCLASS, "")
        code = code.replace("▁", "SPACETOKEN")
        lines = code.split(tsp.NEWLINE_TOK)
        tabs = ""
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith(INDENT + " "):
                tabs += "    "
                line = line.replace(INDENT + " ", tabs)
            elif line.startswith(DEDENT):
                number_dedent = line.count(DEDENT)
                tabs = tabs[4 * number_dedent :]
                line = line.replace(DEDENT, "")
                line = line.strip()
                line = tabs + line
            elif line == DEDENT:
                line = ""
            else:
                line = tabs + line
            lines[i] = line
        untok_s = "\n".join(lines)
        # find string and comment with parser and detokenize string correctly
        ref_line = ""
        wip_line = ""
        try:
            for toktype, tok, _, _, line in tokenize.tokenize(
                BytesIO(untok_s.encode("utf-8")).readline
            ):
                if ref_line != line:
                    ref_line = line
                    # we'll be update "wip_line" little by little
                    # and replacing this line in the full code
                    # little by little as well
                    wip_line = line
                if toktype in (tokenize.STRING, tokenize.COMMENT):
                    tok_ = (
                        tok.replace("STRNEWLINE", "\n")
                        .replace("TABSYMBOL", "\t")
                        .replace(" ", "")
                        .replace("SPACETOKEN", " ")
                    )
                    # replace in line so that replacing in the whole file
                    # has limited border effect
                    new_line = wip_line.replace(tok, tok_)
                    untok_s = untok_s.replace(wip_line, new_line)
                    wip_line = new_line
        except KeyboardInterrupt as e:
            raise e
        except Exception as e:  # pylint: disable=broad-except
            # TODO raise ValueError(f'Invalid python function \n {code}\n') from e
            pass
        # detokenize imports
        untok_s = (
            untok_s.replace(". ", ".")
            .replace(" .", ".")
            .replace("import.", "import .")
            .replace("from.", "from .")
        )
        # special strings
        string_modifiers = ["r", "u", "f", "rf", "fr", "b", "rb", "br"]
        for modifier in string_modifiers + [s.upper() for s in string_modifiers]:
            untok_s = untok_s.replace(f" {modifier} '", f" {modifier}'").replace(
                f' {modifier} "', f' {modifier}"'
            )
        untok_s = untok_s.replace("> >", ">>").replace("< <", "<<")
        return untok_s

    def obfuscate_code(self, code: str):
        res, dico = obfuscateString(code, obfuscateNames=True, removeDocstrings=False)
        return res, dico_to_string(dico)

    def _get_functions_from_ast(
        self,
        code: str,
        node: ts.Node,
        class_funcs: tp.List[str],
        standalone_funcs: tp.List[str],
        _in_class: bool = False,
    ) -> None:
        if node.type == "function_definition":
            if _in_class:
                class_funcs.append(code[node.start_byte : node.end_byte])
            else:
                standalone_funcs.append(code[node.start_byte : node.end_byte])
        for child in node.children:
            self._get_functions_from_ast(
                code,
                child,
                class_funcs,
                standalone_funcs,
                _in_class or node.type == "class_definition",
            )

    def extract_functions(
        self,
        code: tp.Union[str, tp.List[str]],
        tokenized: bool = True,
        remove_python_2: bool = True,
    ) -> tp.Tuple[tp.List[str], tp.List[str]]:
        """
        Extract functions from python code
        tokenized; whether the code is tokenized or not
        """
        standalone_funcs, class_funcs = super(
            PythonTreeSitterProcessor, self
        ).extract_functions(code, tokenized)
        if remove_python_2:
            standalone_funcs = [x for x in standalone_funcs if not is_python_2(x)]
            class_funcs = [x for x in class_funcs if not is_python_2(x)]
        return standalone_funcs, class_funcs

    def dfs(
        self,
        code: bytes,
        node: ts.Node,
        tokens: tp.List[str],
        tokens_type: tp.List[str],
        scope_info: bool = False,  # TODO propagate?
    ) -> None:
        if len(node.children) == 0 or node.type in self.ast_nodes_type_string:
            bsnippet = code[node.start_byte : node.end_byte].strip(b" ")
            snippet = bsnippet.decode("utf8")
            is_docstring = False
            # identify docstrings
            if node.type == "string":
                p = node.parent  # parent should be a statement, with only the docstring
                if p.type == "expression_statement" and len(p.children) == 1:
                    is_docstring = True
            if len(snippet) > 0:
                tokens.append(snippet)
                tokens_type.append("docstring" if is_docstring else node.type)
            if node.type == "comment":
                # comments at the end of line are marked as next line
                # because next lines are added for expression statements :s
                if len(tokens) > 1 and tokens[-2] == tsp.NEWLINE_TOK:
                    prev = node.prev_sibling
                    if prev is not None and prev.end_point[0] == node.end_point[0]:
                        tokens[-1], tokens[-2] = tokens[-2], tokens[-1]
                        tokens_type[-1], tokens_type[-2] = (
                            tokens_type[-2],
                            tokens_type[-1],
                        )

            return
        if node.type == "block":
            tokens.append(tsp.NEWLINE_TOK)
            tokens_type.append(tsp.NEWLINE_TOK)
            tokens.append(INDENT)
            tokens_type.append(INDENT)
        for child in node.children:
            self.dfs(code, child, tokens, tokens_type, scope_info)
        if (
            node.type in ("decorator", "block") or node.type.endswith("_statement")
        ) and tokens[-1] not in (tsp.NEWLINE_TOK, DEDENT):
            # after = node.next_sibling
            # if after is None or after.end_point[0] > node.start_point[0]:
            tokens.append(tsp.NEWLINE_TOK)
            tokens_type.append(tsp.NEWLINE_TOK)
        if node.type == "block":
            tokens.append(DEDENT)
            tokens_type.append(DEDENT)
            if scope_info:
                tokens.append(ENDBLOCK)
                tokens_type.append(ENDBLOCK)
        if scope_info and node.type in {"function_definition"}:
            tokens.append(ENDFUNC)
            tokens_type.append(ENDFUNC)
        if scope_info and node.type in {"class_definition"}:
            tokens.append(ENDCLASS)
            tokens_type.append(ENDCLASS)

    def get_function_name(self, function: tp.Union[str, tp.List[str]]) -> str:
        assert isinstance(function, (str, list))
        if isinstance(function, str):
            function = function.split()
        return function[function.index("def") + 1]

    def obfuscate_types(self, code: str) -> tp.Tuple[str, str]:
        """Obfuscates all the type hints of the code"""
        obf_code, hints = self.extract_type_hints(code)
        ready = []
        toprep = []
        # prefill main special methods
        specials = {
            ".__len__": "int",
            ".__str__": "str",
            ".__repr__": "str",
            ".__hash__": "int",
        }
        for name in ["bool", "contains", "lt", "le", "eq", "ne", "gt", "ge"]:
            specials[f".__{name}__"] = "bool"
        for name in ["init", "init_subclass", "setattr", "setattribute"]:
            specials[f".__{name}__"] = "None"
        special_names = tuple(specials)
        for hint in hints:
            if hint.kind == "return" and hint.name.endswith(special_names):
                end = hint.name.split(".")[-1]
                ready.append(hint.with_value(specials["." + end]))
            elif name.endswith(
                (".__getattr__", ".__getattribute__")
            ):  # nearly impossible to type
                ready.append(hint)
            elif not hint.value:  # nothing to predict
                ready.append(hint)
            else:
                toprep.append(hint)
        # replace!
        tokens = obfuscation_tokens()
        cleaner = TypeCleaner()
        dico = {}
        for hint in toprep:
            tok = next(tokens)
            value = cleaner.clean(hint.value)
            # add optional if actually optional
            if hint.default is not None and hint.default == "None":
                if not value.startswith("Optional"):
                    value = f"Optional [ {value} ]"
            dico[tok] = " ".join(self.tokenize_code(value)[:-1])
            ready.append(hint.with_value(tok))
        repl = {h.uid: h.to_string() for h in ready}
        # probably slow but safer that format which may do weird stuff
        for name, val in repl.items():
            obf_code = obf_code.replace("{" + name + "}", val)
        for string in cleaner.get_imports(obf_code):
            obf_code = obf_code.replace(string, "")
        return obf_code, utils_deobfuscation.dico_to_string(dico)

    def extract_type_hints(self, code: str) -> tp.Tuple[str, tp.List["TypeHint"]]:
        """Extract all type hint emplacements in the code

        Parameter
        ---------
        code: str
            Python code to process

        Returns
        -------
        str
            the code, where type hint emplacements are filled with identifiers
            replacing this identifier with "" is equivalent to having no type,
            otherwise the replacement must include ":" or "->" depending on the kind
            of type hint
        list of TypeHint:
            the list of TypeHint objects which gathers the identifier and all
            type hint related information such as variable name, default value etc
        """
        handler = CodeHandler(code)
        tree = self.get_ast(handler.code)
        traversal = tsp.traverse_tree(tree, final=("parameters", "assignment"))
        hints = []
        for node in traversal:
            # deal with function parameters
            if node.type == "parameters":
                scope = ".".join(handler.get_scopes(node))
                params = 0
                for sub in node.children:
                    parts = []
                    if sub.type == "identifier":
                        parts = [sub]
                    elif "parameter" in sub.type:
                        parts = sub.children
                    if not parts:
                        continue
                    name = handler.read(parts[0])
                    if not params and name == "self":
                        continue
                    start = parts[0].end_byte
                    end = start
                    value = ""
                    for p in parts:
                        if p.type == "type":
                            end = p.end_byte
                            value = handler.read(p)
                    # check for default
                    default = None
                    if "default_parameter" in sub.type:
                        if parts[-2].type == "=":
                            default = handler.read(parts[-1])
                    h = TypeHint(
                        f"{scope}.{name}",
                        value=value,
                        kind="parameter",
                        default=default,
                    )
                    handler.add_replacement(start, end, "{" + h.uid + "}")
                    hints.append(h)
                    params += 1
                # safeguard for errors
                children = itertools.takewhile(
                    lambda n: n.type not in ("block", "expression_statement"),
                    node.parent.children,
                )
                sequence = ("parameters", "->", "type", ":")
                parts = [n for n in children if n.type in sequence][-4:]
                # now deal with function definitions
                if tuple(n.type for n in parts) == sequence:  # type is present
                    value = handler.read(parts[2])
                    h = TypeHint(scope, value=value, kind="return")
                    handler.add_replacement(
                        parts[0].end_byte, parts[2].end_byte, "{" + h.uid + "}"
                    )
                    hints.append(h)
                elif parts:  # no type
                    h = TypeHint(scope, value="", kind="return")
                    start = parts[-1].start_byte
                    handler.add_replacement(start, start, "{" + h.uid + "}")
                    hints.append(h)
            # deal with typed variables outside functions
            elif node.type == "assignment":
                parts = node.children[:3]
                if tuple(n.type for n in parts[1:]) == (":", "type"):
                    if parts[0].type not in ["identifier", "attribute"]:
                        continue
                    id_nodes = parts[:1]
                    scopes = handler.get_scopes(node)
                    if parts[0].type == "attribute":
                        id_nodes = [
                            x for x in parts[0].children[1:] if x.type == "identifier"
                        ]
                        if scopes[-1] == "__init__":
                            scopes = scopes[:-1]
                    name = ".".join(scopes + [handler.read(x) for x in id_nodes])
                    value = handler.read(node.children[2])
                    h = TypeHint(name, value=value, kind="variable")
                    handler.add_replacement(
                        node.children[0].end_byte,
                        node.children[2].end_byte,
                        "{" + h.uid + "}",
                    )
                    hints.append(h)
        return handler.generate(), hints


@dataclasses.dataclass
class Replacement:
    start: int
    end: int
    value: bytes


class CodeHandler:
    """Simpler operations on code with tree sitter nodes

    Parameters
    ----------
    code: str or bytes
        Code parsed by tree sitter
    """

    def __init__(self, code: tp.Union[str, bytes]) -> None:
        if not isinstance(code, bytes):
            code = code.encode("utf8")
        self.code = code
        self.replacements: tp.List[Replacement] = []

    def read(self, node: tp.Union[Replacement, ts.Node]) -> str:
        """Reads the string referred by the provided node"""
        if isinstance(node, Replacement):
            return self.read_range(node.start, node.end)
        return self.read_range(node.start_byte, node.end_byte)

    def read_range(self, start: int, end: int) -> str:
        """Reads the string within the provided range"""
        return self.code[start:end].decode("utf8")

    def add_replacement(
        self, start: int, end: int, string: tp.Union[bytes, str]
    ) -> None:
        """Adds a range from the base string which needs to be replaced by the given string
        Caution: ranges must be added in increasing sequence, and must be non-overlapping
        """
        if isinstance(string, str):
            string = string.encode("utf8")
        repl = Replacement(start, end, string)
        if self.replacements:
            last = self.replacements[-1]
            if start < last.end:
                error = ["Overlapping or unsorted replacements"]
                for z in (repl, last):
                    error.append(f"({z}, {self.read(z)} -> {z.value.decode('utf8')})")
                raise ValueError("\n".join(error))
        self.replacements.append(repl)

    def add_replacement_from_node(
        self, node: ts.Node, string: tp.Union[bytes, str]
    ) -> None:
        """Adds a node which needs to be replaced by a given string
        Caution: nodes must be added in increasing sequence, and must be non-overlapping
        """
        self.add_replacement(node.start_byte, node.end_byte, string)

    def generate(self) -> str:
        """Generate the new code with replacements"""
        parts = []
        start = 0
        for repl in self.replacements:
            # code up to the node
            parts.append(self.code[start : repl.start])
            parts.append(repl.value)
            start = repl.end
        parts.append(self.code[start:])
        return b"".join(parts).decode("utf8")

    def get_scopes(self, node: ts.Node) -> tp.List[str]:
        scopes = []
        while node is not None:
            if "_definition" in node.type:
                ids = [n for n in node.children if n.type == "identifier"]
                if ids:
                    scopes.append(self.read(ids[0]))
            node = node.parent
        return list(reversed(scopes))


class TypeCleaner:
    """Aims at:
    - identifying imports so as to remove them (avoids biasing the model)
    - uniformize how types are expressed
    """

    # TODO
    # - order in unions
    # - add optional ??

    _TAG = "tag2Replace"

    def __init__(self) -> None:
        self.processor = PythonTreeSitterProcessor()
        self.typing_classes = set(x for x in dir(tp) if x[0].isupper())

    def get_imports(self, code: tp.Union[str, bytes]) -> tp.List[str]:
        """Get a list of imports involving typing module"""
        handler = CodeHandler(code)
        tree = self.processor.get_ast(code)
        import_node = [
            "import_from_statement",
            "import_statement",
            "future_import_statement",
        ]
        finals = ["assignment", "block", "function_definition", "class_definition"]
        traversal = tsp.traverse_tree(tree, final=import_node + finals)
        typing_imports_code = []
        for node in traversal:
            if "import" not in node.type:
                continue
            data = [(n.type, handler.read(n)) for n in node.children]
            if len(data) < 2 or "typing" not in data[1][1].split(" ", maxsplit=1)[0]:
                continue  # a bit ugly but robust enough for now
            typing_imports_code.append(handler.read(node))
        return typing_imports_code

    def clean(self, typestr: str) -> str:
        """Clean a type string to make it as uniform as possible
        Eg: dict -> tp.Dict[str, tp.Any]
        """
        # using a tag instead, we can replace later on by whatever we want
        # eg: tag2Replace.Dict -> tp.Dict
        tag = self._TAG
        handler = CodeHandler(typestr)
        tree = self.processor.get_ast(handler.code)
        traversal = tsp.traverse_tree(tree)
        updater = {x: x[0].upper() + x[1:] for x in ["set", "list", "dict", "tuple"]}
        updater["object"] = "Any"
        move_after = -1
        for node in traversal:
            current = node
            if current.start_byte < move_after:
                continue
            if current.type == "comment":
                handler.add_replacement_from_node(current, "")
                move_after = current.end_byte
                continue
            val = handler.read(current)
            val = updater.get(val, val)
            if val in self.typing_classes:
                if current.parent is not None and current.parent.type == "attribute":
                    current = current.parent
                handler.add_replacement_from_node(current, f"{tag}.{val}")
                move_after = current.end_byte
        output = handler.generate()
        textio = f"{tag}.TextIO"
        textio_ph = "!#TEXTIO_PLACEHOLDER#!"  # avoid replacing TextIO by strIO
        replacements = {textio: textio_ph, f"{tag}.Text": "str"}
        # to be decided: replace np.ndarray?
        # replacements.update({x: "NDArray" for x in ["np.ndarray", "ndarray", "np.ndarray"]})
        # no line break, and use type, not string of type
        replacements.update({x: "" for x in ["\n", "\r", "'", '"']})
        for sin, sout in replacements.items():
            output = output.replace(sin, sout)
        output = output.replace(textio_ph, textio)
        # sanitize main containers
        list_like = ["Set", "List", "Iterator", "Iterable", "Sequence"]
        add_any = {f"{tag}.{x}": f"{tag}.Any" for x in list_like}
        add_any.update(
            {
                f"{tag}.Dict": f"str,{tag}.Any",
                f"{tag}.Mapping": f"str,{tag}.Any",
                f"{tag}.Callable": f"...,{tag}.Any",
                f"{tag}.Generator": f"{tag}.Any,None,None",
                f"{tag}.Tuple": f"{tag}.Any,...",
            }
        )
        for cls, content in add_any.items():
            # when there is no subtype, add the default one
            output = re.sub(cls + r"(?!\[)", f"{cls}[{content}]", output)
        output = self._reorder_union(output)
        output = output.replace(" ", "").replace(tag + ".", "")  # remove tag

        return output

    def _reorder_union(self, string: str) -> str:
        """Uniformize all unions (Union and | syntax)
        by applying Union syntax and ordering the options
        """
        union = f"{self._TAG}.Union"
        if not any(x in string for x in [union, "|"]):
            return string
        handler = CodeHandler(string)
        tree = self.processor.get_ast(handler.code)
        traversal = tsp.traverse_tree(tree)
        move_after = -1
        for node in traversal:
            if node.start_byte < move_after:
                continue
            children = self._extract_union_children(node, string)
            # test
            if children:
                content = [handler.read(n).strip() for n in children]
                content = sorted(set(self._reorder_union(x) for x in content))
                is_opt = "None" in content
                if is_opt:
                    content = [c for c in content if c != "None"]
                replacement = f"{union}[{','.join(content)}]"
                if len(content) == 1:
                    replacement = content[0]
                if is_opt:
                    replacement = f"{self._TAG}.Optional[{replacement}]"
                handler.add_replacement_from_node(node, replacement)
                move_after = node.end_byte
        return handler.generate()

    def _extract_union_children(self, node: ts.Node, string: str) -> tp.List[ts.Node]:
        """Recursively extract all the types in the union, whatever the format
        (Union or |)
        """
        children = []
        union = f"{self._TAG}.Union"
        handler = CodeHandler(string)
        if len(node.children) == 1:
            child = node.children[0]
            if node.start_byte == child.start_byte:
                if node.end_byte == child.end_byte:
                    return self._extract_union_children(child, string)
        if node.type == "binary_operator" and node.children[1].type == "|":
            children = node.children
        if (
            node.type in ["expression_statement", "subscript"]
            and len(node.children) > 1
        ):
            if handler.read(node.children[0]) == union:
                children = node.children[2:-1]
        children = [c for c in children if c.type not in "|,"]
        resplit = [self._extract_union_children(c, string) for c in children]
        out = list(
            itertools.chain.from_iterable(
                r if r else [c] for r, c in zip(resplit, children)
            )
        )
        return out


_counter = itertools.count()


def id_maker() -> str:
    """Safe id for replacement in the string"""
    num = _counter.__next__()
    return f"cg_{num}_" + uuid.uuid4().hex[:4]


@dataclasses.dataclass
class TypeHint:
    """Keep track of all information about a type hint
    including a uid to use as placeholder in the origin string
    """

    name: str
    value: str
    kind: str
    default: tp.Optional[str] = None
    uid: str = dataclasses.field(default_factory=id_maker, init=False)

    def __post_init__(self) -> None:
        if self.kind not in ("return", "parameter", "variable"):
            raise ValueError(f"Unknown kind {self.kind}")
        if self.default is not None and self.kind != "parameter":
            raise ValueError("Default can only be specified for parameters")

    def with_value(self, value: str) -> "TypeHint":
        """Creates a new TypeHint with all field similar but the value"""
        out = dataclasses.replace(self, value=value)
        out.uid = self.uid
        return out

    def to_string(self) -> str:
        """Returns the code for replacing the placeholder in the code.
        This includes the : or -> operator when the type hint is specified.
        """
        op = " -> " if self.kind == "return" else ": "
        return "" if not self.value else op + self.value
