"""Minimal non-evaluating, Liquid-like text templating.

MIT License

Copyright (c) 2025-present James Prior <jamesgr.prior@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

import json
import os
import re
from collections import deque
from contextlib import contextmanager
from itertools import chain
from re import Pattern
from typing import Callable
from typing import Iterable
from typing import Iterator
from typing import Mapping
from typing import NamedTuple
from typing import Optional
from typing import Protocol
from typing import Sequence
from typing import Type
from typing import TypeAlias

__all__ = (
    "render",
    "Template",
    "TemplateSyntaxError",
    "StrictUndefined",
    "Undefined",
)


def render(
    source: str,
    data: Mapping[str, object],
    *,
    serializer: Callable[[object], str] | None = None,
    undefined: Type[Undefined] | None = None,
) -> str:
    """Render template _source_ with variables from _data_.

    Use `template = Template(source)` then `template.render(data)` if you need
    to render the same template multiple times with different data.
    """
    return Template(source, serializer=serializer, undefined=undefined).render(data)


class Template:
    """A compiled template, ready to be rendered."""

    def __init__(
        self,
        source: str,
        *,
        serializer: Callable[[object], str] | None = None,
        undefined: Type[Undefined] | None = None,
    ):
        self.source = source
        self.serializer = serializer or serialize
        self.undefined = undefined or Undefined
        try:
            self.nodes = Parser(Scanner(source).tokens).parse()
        except TemplateError as err:
            err.source = source
            raise

    def render(self, data: Mapping[str, object]) -> str:
        """Render this template with variables from _data_."""
        scope = Scope(data, serializer=self.serializer, undefined=self.undefined)
        buffer: list[str] = []
        for node in self.nodes:
            if isinstance(node, str):
                buffer.append(node)
            else:
                try:
                    node.render(scope, buffer)
                except TemplateError as err:
                    err.source = self.source
                    raise
        return "".join(buffer)


class TemplateError(Exception):
    """Base class for all template exceptions."""

    def __init__(self, *args: object, token: Token):
        super().__init__(*args)
        self.token = token
        self.source: str | None = None

    def __str__(self) -> str:
        if not self.token or self.token.start < 0 or not self.source:
            return super().__str__()

        _kind, value, index = self.token
        context = self.error_context(self.source, index)

        if not context:
            return super().__str__()

        line, col, current = context
        position = f"{current!r}:{line}:{col}"
        pad = " " * len(str(line))
        pointer = (" " * col) + ("^" * len(value))

        return os.linesep.join(
            [
                self.args[0],
                f"{pad} -> {position}",
                f"{pad} |",
                f"{line} | {current}",
                f"{pad} | {pointer} {self.args[0]}",
            ]
        )

    def error_context(self, text: str, index: int) -> tuple[int, int, str] | None:
        """Return the line number, column number and current line of text."""
        lines = text.splitlines(keepends=True)
        cumulative_length = 0
        target_line_index = -1

        for i, line in enumerate(lines):
            cumulative_length += len(line)
            if index < cumulative_length:
                target_line_index = i
                break

        if target_line_index == -1:
            return None

        line_number = target_line_index + 1  # 1-based
        column_number = index - (cumulative_length - len(lines[target_line_index]))
        current_line = lines[target_line_index].rstrip()
        return (line_number, column_number, current_line)


class TemplateSyntaxError(TemplateError):
    """An exception raised during template parsing due to unexpected template syntax."""


class UndefinedVariableError(TemplateError):
    """An exception raised by the strict undefined type."""


class Token(NamedTuple):
    kind: str
    value: str
    start: int


_StateFn: TypeAlias = Callable[[], Optional["_StateFn"]]

_RE_TRIVIA = re.compile(r"[ \n\r\t]+")
_RE_TAG_NAME = re.compile(r"(?:end)?(?:if|for|elif|elsif|else)")
_RE_WORD = re.compile(r"[\u0080-\uFFFFa-zA-Z_][\u0080-\uFFFFa-zA-Z0-9_-]*")
_RE_MARKUP_START = re.compile(r"\{\{|\{%")
_RE_MARKUP_END = re.compile(r"[\}%]\}?")
_RE_PUNCTUATION = re.compile(r"[\[\]\.\(\)]")
_RE_INT = re.compile(r"-?\d+")

_TOKEN_MAP: dict[str, str] = {
    "[": "TOKEN_L_BRACKET",
    "]": "TOKEN_R_BRACKET",
    ".": "TOKEN_DOT",
    "(": "TOKEN_L_PAREN",
    ")": "TOKEN_R_PAREN",
    "and": "TOKEN_AND",
    "or": "TOKEN_OR",
    "not": "TOKEN_NOT",
    "in": "TOKEN_IN",
}

_ESCAPES = frozenset(["b", "f", "n", "r", "t", "u", "/", "\\"])


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.pos = 0

        state: _StateFn | None = self.lex_markup
        while state is not None:
            state = state()

    def emit(self, kind: str, value: str) -> None:
        self.tokens.append(Token(kind, value, self.start))
        self.start = self.pos

    def next(self) -> str:
        try:
            ch = self.source[self.pos]
            self.pos += 1
            return ch
        except IndexError:
            return ""

    def peek(self) -> str:
        try:
            return self.source[self.pos]
        except IndexError:
            return ""

    def scan(self, pattern: Pattern[str]) -> str | None:
        match = pattern.match(self.source, self.pos)
        if match:
            self.pos += match.end() - match.start()
            return match[0]
        return None

    def scan_until(self, pattern: Pattern[str]) -> str | None:
        match = pattern.search(self.source, self.pos)
        if match:
            self.pos = match.start()
            return self.source[self.start : match.start()]
        return None

    def skip(self, pattern: Pattern[str]) -> bool:
        match = pattern.match(self.source, self.pos)
        if match:
            self.pos += match.end() - match.start()
            self.start = self.pos
            return True
        return False

    def accept_whitespace_control(self) -> bool:
        ch = self.peek()
        if ch in ("-", "~"):
            self.pos += 1
            self.emit("TOKEN_WC", ch)
            return True
        return False

    def lex_markup(self) -> _StateFn | None:
        value = self.scan(_RE_MARKUP_START)

        if value == r"{{":
            self.emit("TOKEN_OUT_START", value)
            self.accept_whitespace_control()
            self.skip(_RE_TRIVIA)
            return self.lex_expression

        if value == r"{%":
            self.emit("TOKEN_TAG_START", value)
            self.accept_whitespace_control()
            self.skip(_RE_TRIVIA)
            return self.lex_tag

        return self.lex_other

    def lex_expression(self) -> _StateFn | None:
        while True:
            self.skip(_RE_TRIVIA)

            if value := self.scan(_RE_INT):
                self.emit("TOKEN_INT", value)
            elif value := self.scan(_RE_PUNCTUATION):
                self.emit(_TOKEN_MAP.get(value, "TOKEN_UNKNOWN"), value)
            elif value := self.scan(_RE_WORD):
                self.emit(_TOKEN_MAP.get(value, "TOKEN_WORD"), value)
            else:
                peeked = self.peek()
                if peeked == "'":
                    self.pos += 1
                    self.start = self.pos
                    self.scan_string("'", "TOKEN_SINGLE_QUOTE_STRING")
                elif peeked == '"':
                    self.pos += 1
                    self.start = self.pos
                    self.scan_string('"', "TOKEN_DOUBLE_QUOTE_STRING")
                else:
                    break

        self.accept_whitespace_control()
        value = self.scan(_RE_MARKUP_END)

        if value == r"}}":
            self.emit("TOKEN_OUT_END", value)
        elif value == r"%}":
            self.emit("TOKEN_TAG_END", value)
        elif value in (r"%", r"}"):
            raise TemplateSyntaxError(
                "incomplete markup detected",
                token=Token("TOKEN_ERROR", value, self.start),
            )
        else:
            raise TemplateSyntaxError(
                f"unexpected {self.peek()!r}",
                token=Token("TOKEN_ERROR", self.next(), self.start),
            )

        return self.lex_markup

    def lex_tag(self) -> _StateFn | None:
        if tag_name := self.scan(_RE_TAG_NAME):
            self.emit("TOKEN_TAG_NAME", tag_name)
            self.skip(_RE_TRIVIA)
            return self.lex_expression

        raise TemplateSyntaxError(
            "unknown, missing or malformed tag name",
            token=Token("TOKEN_UNKNOWN", self.peek(), self.start),
        )

    def lex_other(self) -> _StateFn | None:
        if value := self.scan_until(_RE_MARKUP_START):
            self.emit("TOKEN_OTHER", value)
            return self.lex_markup

        self.pos = len(self.source)

        if self.pos > self.start:
            self.emit("TOKEN_OTHER", self.source[self.start :])

        return None

    def scan_string(self, quote: str, kind: str) -> None:
        if self.peek() == quote:
            # Empty string
            self.pos += 1
            self.start = self.pos
            self.emit(kind, "")
            return

        needs_unescaping = False

        while True:
            ch = self.next()

            if ch == "\\":
                peeked = self.peek()
                if peeked in _ESCAPES or peeked == quote:
                    needs_unescaping = True
                    self.pos += 1
                else:
                    raise TemplateSyntaxError(
                        "invalid escape sequence",
                        token=Token("TOKEN_ERROR", ch, self.pos),
                    )

            if ch == quote:
                if needs_unescaping:
                    try:
                        self.emit(
                            kind,
                            _unescape(self.source[self.start : self.pos - 1], quote),
                        )
                    except json.JSONDecodeError as err:
                        raise TemplateSyntaxError(
                            "invalid escape sequence",
                            token=Token("TOKEN_ERROR", ch, self.pos - 1),
                        ) from err
                else:
                    self.emit(kind, self.source[self.start : self.pos - 1])
                return

            if not ch:
                raise TemplateSyntaxError(
                    "unclosed string literal",
                    token=Token("TOKEN_ERROR", quote, self.start),
                )


def _unescape(s: str, quote: str) -> str:
    if quote == "'":
        s = s.replace('"', '\\"').replace("\\'", "'")
    unescaped: str = json.loads(f'"{s}"')
    return unescaped


class Markup(Protocol):
    """The interface for a tag or output statement."""

    def render(self, data: Scope, buffer: list[str]) -> None:
        """Render this node to _buffer_ with reference to variables in _data_."""
        ...  # pragma: no cov


class Expression(Protocol):
    """The interface for a loop or logical expression."""

    def evaluate(self, data: Scope) -> object:
        """Evaluate this expression with reference to variables in _data_."""
        ...  # pragma: no cov


Node: TypeAlias = str | Markup


def serialize(obj: object) -> str:
    return json.dumps(obj) if isinstance(obj, (list, dict, tuple)) else str(obj)


class Output:
    def __init__(self, expression: Expression):
        self.expression = expression

    def render(self, data: Scope, buffer: list[str]) -> None:
        value = self.expression.evaluate(data)
        buffer.append(data.serialize(value))


class IfTag:
    def __init__(
        self,
        blocks: list[tuple[Expression, list[Node]]],
        default: Optional[list[Node]],
    ):
        self.blocks = blocks
        self.default = default

    def render(self, data: Scope, buffer: list[str]) -> None:
        for expression, block in self.blocks:
            if expression.evaluate(data):
                for node in block:
                    if isinstance(node, str):
                        buffer.append(node)
                    else:
                        node.render(data, buffer)
                return

        if self.default:
            for node in self.default:
                if isinstance(node, str):
                    buffer.append(node)
                else:
                    node.render(data, buffer)


class ForTag:
    def __init__(
        self,
        name: str,
        target: Expression,
        block: list[Node],
        default: Optional[list[Node]],
    ):
        self.name = name
        self.target = target
        self.block = block
        self.default = default

    def render(self, data: Scope, buffer: list[str]) -> None:
        target = self.target.evaluate(data)

        if not isinstance(target, Iterable):
            if self.default:
                self.render_block(data, buffer, self.default)
            return

        if isinstance(target, Mapping):
            target = target.items()

        namespace: dict[str, object] = {}
        rendered = False

        with data.extend(namespace):
            for item in target:
                namespace[self.name] = item
                rendered = True
                self.render_block(data, buffer, self.block)

        if not rendered and self.default:
            self.render_block(data, buffer, self.default)

    def render_block(self, data: Scope, buffer: list[str], nodes: list[Node]) -> None:
        for node in nodes:
            if isinstance(node, str):
                buffer.append(node)
            else:
                node.render(data, buffer)


class Undefined:
    """The object used when a template variable can not be resolved."""

    def __init__(self, name: str, token: Token):
        self.name = name
        self.token = token

    def __str__(self) -> str:
        return ""

    def __bool__(self) -> bool:
        return False

    def __iter__(self) -> Iterable[object]:
        yield from ()


class StrictUndefined(Undefined):
    def __str__(self) -> str:
        raise UndefinedVariableError(f"{self.name!r} is undefined", token=self.token)

    def __bool__(self) -> bool:
        return False

    def __iter__(self) -> Iterable[object]:
        raise UndefinedVariableError(f"{self.name!r} is undefined", token=self.token)


_UNDEFINED = object()


class Scope(Mapping[str, object]):
    def __init__(
        self,
        *maps: Mapping[str, object],
        serializer: Callable[[object], str] = json.dumps,
        undefined: Type[Undefined] = Undefined,
    ):
        self._maps = deque(maps)
        self.serialize = serializer
        self.undefined = undefined

    def __getitem__(self, key: str) -> object:
        for mapping in self._maps:
            try:
                return mapping[key]
            except KeyError:
                pass
        raise KeyError(key)

    def __iter__(self) -> Iterator[str]:
        return chain(*self._maps)

    def __len__(self) -> int:
        return sum(len(_map) for _map in self._maps)

    def get(self, key: str, default: object = _UNDEFINED) -> object:
        try:
            return self[key]
        except KeyError:
            return default

    def push(self, namespace: Mapping[str, object]) -> None:
        self._maps.appendleft(namespace)

    def pop(self) -> Mapping[str, object]:
        return self._maps.popleft()

    @contextmanager
    def extend(self, namespace: Mapping[str, object]) -> Iterator[Scope]:
        self.push(namespace)
        try:
            yield self
        finally:
            self.pop()


class BooleanExpression:
    def __init__(self, expression: Expression):
        self.expression = expression

    def evaluate(self, data: Scope) -> bool:
        return bool(self.expression.evaluate(data))


class LogicalNotExpression:
    def __init__(self, expression: Expression):
        self.expression = expression

    def evaluate(self, data: Scope) -> bool:
        return not bool(self.expression.evaluate(data))


class BinaryExpression:
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right


class LogicalAndExpression(BinaryExpression):
    def evaluate(self, data: Scope) -> object:
        left = self.left.evaluate(data)
        if left:
            return self.right.evaluate(data)
        return left


class LogicalOrExpression(BinaryExpression):
    def evaluate(self, data: Scope) -> object:
        left = self.left.evaluate(data)
        if left:
            return left
        return self.right.evaluate(data)


class StringLiteral:
    def __init__(self, value: str):
        self.value = value

    def evaluate(self, _data: Scope) -> object:
        return self.value


class Variable:
    def __init__(self, token: Token, path: list[str | int]):
        self.token = token
        self.path = path

    def evaluate(self, data: Scope) -> object:
        it = iter(self.path)
        root = next(it, None)

        if not isinstance(root, str):
            return data.undefined(str(root), self.token)

        obj = data.get(root, _UNDEFINED)

        if obj == _UNDEFINED:
            return data.undefined(root, self.token)

        for i, segment in enumerate(it):
            if isinstance(obj, Mapping):
                obj = obj.get(segment, _UNDEFINED)
            elif isinstance(obj, Sequence) and isinstance(segment, int):
                try:
                    obj = obj[segment]
                except IndexError:
                    obj = _UNDEFINED
            else:
                obj = _UNDEFINED

            if obj == _UNDEFINED:
                return data.undefined(self.path_to_str(self.path[: i + 2]), self.token)

        return obj

    def path_to_str(self, path: list[str | int]) -> str:
        it = iter(path)
        buf: list[str] = [str(next(it, ""))]
        for segment in it:
            if isinstance(segment, str):
                if _RE_WORD.fullmatch(segment):
                    buf.append(f".{segment}")
                else:
                    buf.append(f"[{segment!r}]")
            else:
                buf.append(f"[{segment}]")
        return "".join(buf)


_TERMINATE_EXPRESSION: set[str] = {
    "TOKEN_WC",
    "TOKEN_OUT_END",
    "TOKEN_TAG_END",
    "TOKEN_OTHER",
    "TOKEN_EOF",
}

_TERMINATE_GROUPED_EXPRESSION: set[str] = {"TOKEN_EOF", "TOKEN_OTHER", "TOKEN_RPAREN"}

_END_IF_BLOCK: set[str] = {
    "else",
    "elif",
    "elsif",
    "endif",
}

_END_FOR_BLOCK: set[str] = {
    "else",
    "endfor",
}

_PRECEDENCE_LOWEST = 1
_PRECEDENCE_LOGICAL_OR = 2
_PRECEDENCE_LOGICAL_AND = 3
_PRECEDENCE_PREFIX = 4

_PRECEDENCES: dict[str, int] = {
    "TOKEN_AND": _PRECEDENCE_LOGICAL_AND,
    "TOKEN_OR": _PRECEDENCE_LOGICAL_OR,
    "TOKEN_NOT": _PRECEDENCE_PREFIX,
}

_BINARY_OPERATORS: set[str] = {"TOKEN_AND", "TOKEN_OR"}


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0
        self.eof = Token("TOKEN_EOF", "", -1)
        self.whitespace_carry: Optional[str] = None

    def current(self) -> Token:
        try:
            return self.tokens[self.pos]
        except IndexError:
            return self.eof

    def next(self) -> Token:
        try:
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        except IndexError:
            return self.eof

    def peek(self, offset: int = 1) -> Token:
        try:
            return self.tokens[self.pos + offset]
        except IndexError:
            return self.eof

    def eat(self, kind: str, message: str | None = None) -> Token:
        token = self.next()
        if token.kind != kind:
            raise TemplateSyntaxError(
                message or f"unexpected {token.value!r}", token=token
            )
        return token

    def eat_empty_tag(self, name: str) -> Token:
        self.eat("TOKEN_TAG_START", f"expected tag {name!r}")
        self.skip_wc()
        name_token = self.eat("TOKEN_TAG_NAME", f"expected tag {name!r}")

        if name_token.value != name:
            raise TemplateSyntaxError(
                f"unexpected tag {name_token.value!r}", token=name_token
            )

        self.carry_wc()
        self.eat("TOKEN_TAG_END", f"expected tag {name!r}")
        return name_token

    def expect_expression(self) -> None:
        if self.current().kind in _TERMINATE_EXPRESSION:
            raise TemplateSyntaxError("missing expression", token=self.current())

    def peek_wc(self) -> Optional[str]:
        token = self.peek()
        if token.kind == "TOKEN_WC":
            return token.value
        return None

    def carry_wc(self) -> None:
        if self.current().kind == "TOKEN_WC":
            self.whitespace_carry = self.next().value
        else:
            self.whitespace_carry = None

    def skip_wc(self) -> None:
        if self.current().kind == "TOKEN_WC":
            self.pos += 1

    def tag(self, name: str) -> bool:
        token = self.peek()
        if token.kind == "TOKEN_WC":
            token = self.peek(2)
        return token.kind == "TOKEN_TAG_NAME" and token.value == name

    def peek_tag_name(self) -> str:
        token = self.current()
        if token.kind == "TOKEN_WC":
            token = self.peek()

        if token.kind == "TOKEN_TAG_NAME":
            return token.value
        raise TemplateSyntaxError("missing tag name", token=token)

    def trim(self, value: str, left_trim: str | None, right_trim: str | None) -> str:
        if left_trim == right_trim:
            if left_trim == "-":
                return value.strip()
            if left_trim == "~":
                return value.strip("\r\n")
            return value

        if left_trim == "-":
            value = value.lstrip()
        elif left_trim == "~":
            value = value.lstrip("\r\n")

        if right_trim == "-":
            value = value.rstrip()
        elif right_trim == "~":
            value = value.rstrip("\r\n")

        return value

    def parse(self, end: set[str] | None = None) -> list[Node]:
        nodes: list[Node] = []

        while True:
            token = self.next()
            kind, value, _ = token

            if kind == "TOKEN_OTHER":
                nodes.append(self.trim(value, self.whitespace_carry, self.peek_wc()))
            elif kind == "TOKEN_OUT_START":
                if self.current().kind == "TOKEN_WC":
                    self.pos += 1
                nodes.append(self.parse_output())
            elif kind == "TOKEN_TAG_START":
                if end and self.peek_tag_name() in end:
                    self.pos -= 1
                    return nodes

                if self.current().kind == "TOKEN_WC":
                    self.pos += 1
                nodes.append(self.parse_tag())
            elif kind == "TOKEN_EOF":
                return nodes
            else:
                raise TemplateSyntaxError(f"unexpected {kind}", token=token)

    def parse_output(self) -> Markup:
        expr = self.parse_primary()
        self.carry_wc()
        self.eat("TOKEN_OUT_END")
        return Output(expr)

    def parse_tag(self) -> Markup:
        token = self.eat("TOKEN_TAG_NAME")

        if token.value == "if":
            blocks: list[tuple[Expression, list[Node]]] = []
            self.expect_expression()
            expr = BooleanExpression(self.parse_primary())
            self.carry_wc()
            self.eat("TOKEN_TAG_END")
            block = self.parse(_END_IF_BLOCK)
            blocks.append((expr, block))

            while self.tag("elsif") or self.tag("elif"):
                self.eat("TOKEN_TAG_START")
                self.skip_wc()
                self.eat("TOKEN_TAG_NAME")
                self.expect_expression()
                expr = BooleanExpression(self.parse_primary())
                self.carry_wc()
                self.eat("TOKEN_TAG_END")
                block = self.parse(_END_IF_BLOCK)
                blocks.append((expr, block))

            if self.tag("else"):
                self.eat_empty_tag("else")
                default = self.parse(_END_IF_BLOCK)
            else:
                default = None

            self.eat_empty_tag("endif")
            return IfTag(blocks, default)

        if token.value == "for":
            self.expect_expression()
            identifier = self.parse_identifier()
            self.eat("TOKEN_IN", "missing 'in'")
            self.expect_expression()
            target = self.parse_primary()
            self.carry_wc()
            self.eat("TOKEN_TAG_END")
            block = self.parse(_END_FOR_BLOCK)

            if self.tag("else"):
                self.eat_empty_tag("else")
                default = self.parse(_END_FOR_BLOCK)
            else:
                default = None

            self.eat_empty_tag("endfor")
            return ForTag(identifier, target, block, default)

        raise TemplateSyntaxError(f"unexpected tag {token.value!r}", token=token)

    def parse_primary(self, precedence: int = _PRECEDENCE_LOWEST) -> Expression:
        token = self.current()
        left_kind = token.kind

        left: Expression

        if left_kind in ("TOKEN_SINGLE_QUOTE_STRING", "TOKEN_DOUBLE_QUOTE_STRING"):
            left = StringLiteral(self.next().value)
        elif left_kind == "TOKEN_L_PAREN":
            left = self.parse_group()
        elif left_kind in ("TOKEN_WORD", "TOKEN_L_BRACKET"):
            left = self.parse_path()
        elif left_kind == "TOKEN_NOT":
            self.pos += 1
            left = LogicalNotExpression(self.parse_primary(_PRECEDENCE_PREFIX))
        else:
            raise TemplateSyntaxError(f"unexpected {left_kind}", token=token)

        while True:
            kind = self.current().kind

            if kind == "TOKEN_UNKNOWN":
                raise TemplateSyntaxError(
                    f"unexpected {self.current().value!r}", token=self.current()
                )

            if (
                kind == "TOKEN_EOF"
                or _PRECEDENCES.get(kind, _PRECEDENCE_LOWEST) < precedence
                or kind not in _BINARY_OPERATORS
            ):
                break

            left = self.parse_infix_expression(left)

        return left

    def parse_infix_expression(self, left: Expression) -> Expression:
        token = self.next()
        kind = token.kind
        precedence = _PRECEDENCES.get(kind, _PRECEDENCE_LOWEST)
        right = self.parse_primary(precedence)

        if kind == "TOKEN_AND":
            return LogicalAndExpression(left, right)

        if kind == "TOKEN_OR":
            return LogicalOrExpression(left, right)

        raise TemplateSyntaxError(f"unexpected operator {kind}", token=token)

    def parse_group(self) -> Expression:
        self.eat("TOKEN_L_PAREN")
        expr = self.parse_primary()
        self.eat("TOKEN_R_PAREN", "unbalanced parentheses")
        return expr

    def parse_identifier(self) -> str:
        token = self.eat("TOKEN_WORD")
        if self.current().kind in ("TOKEN_DOT", "TOKEN_L_BRACKET"):
            raise TemplateSyntaxError(
                "expected an identifier, found a path", token=token
            )
        return token.value

    def parse_path(self) -> Expression:
        segments: list[str | int] = []
        token = self.current()

        if self.current().kind == "TOKEN_WORD":
            segments.append(self.next().value)

        while True:
            kind = self.next().kind
            if kind == "TOKEN_L_BRACKET":
                segments.append(self.parse_bracketed_path_selector())
            elif kind == "TOKEN_DOT":
                segments.append(self.parse_shorthand_path_selector())
            else:
                self.pos -= 1
                return Variable(token, segments)

    def parse_bracketed_path_selector(self) -> str | int:
        token = self.next()
        kind, value, _ = token
        segment: int | str

        if kind == "TOKEN_INT":
            segment = int(value)
        elif kind in ("TOKEN_DOUBLE_QUOTE_STRING", "TOKEN_SINGLE_QUOTE_STRING"):
            segment = value
        elif kind == "TOKEN_R_BRACKET":
            raise TemplateSyntaxError("empty bracketed segment", token=token)
        else:
            raise TemplateSyntaxError(f"unexpected {kind}", token=token)

        self.eat("TOKEN_R_BRACKET")
        return segment

    def parse_shorthand_path_selector(self) -> str | int:
        token = self.next()
        kind, value, _ = token

        if kind == "TOKEN_INT":
            return int(value)

        if kind in ("TOKEN_WORD", "TOKEN_AND", "TOKEN_OR", "TOKEN_NOT"):
            return value

        raise TemplateSyntaxError(f"unexpected {kind}", token=token)
