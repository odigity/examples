#!/usr/bin/env python
from parsy import eof, regex, seq, string, string_from, success, test_char, ParseError


def print_all(*args, **kwargs):                     # useful for debugging
    print(f"args   = {args}")
    print(f"kwargs = {kwargs}")


##
##  Parsing Primitives  (produces parsers)
##


def ex__string():
    p = string("foo")

    print(p.parse("foo"))                           # foo

    try:
        print(p.parse("bar"))
    except ParseError as e:
        print(e)                                    # expected 'foo' at 0:0

    try:
        print(p.parse("foo1"))
    except ParseError as e:
        print(e)                                    # expected 'EOF' at 0:3

    print(p.parse_partial("foo1"))                  # ('foo', '1')


def ex__regex():
    # mostly behaves like string(), except for group support

    p = regex("(foo)bar", group=1)
    print(p.parse("foobar"))                        # foo

    p = regex("(foo)(bar)", group=(1,2))
    print(p.parse("foobar"))                        # ('foo', 'bar')

    p = regex("(?P<fg>foo)(?P<bg>bar)", group="fg")
    print(p.parse("foobar"))                        # foo


def ex__test_char():
    p = test_char(lambda c: c == "f", "mydesc")
    print(p.parse("f"))                             # f

    try:
        print(p.parse("bar"))
    except ParseError as e:
        print(e)                                    # expected 'mydesc' at 0:0

    try:
        print(p.parse("foo"))
    except ParseError as e:
        print(e)                                    # expected 'EOF' at 0:1

    (p.parse_partial("foo"))                        # ('f', 'oo')

    # NOTE: char_from() is almost identical, not worth seperate test


def ex__string_from():
    p = string_from("foo", "bar")
    print(p.parse("foo"))                           # foo
    print(p.parse("bar"))                           # bar

    try:
        print(p.parse("baz"))
    except ParseError as e:
        print(e)                                    # expected one of 'bar', 'foo' at 0:0

    try:
        print(p.parse("foo1"))
    except ParseError as e:
        print(e)                                    # expected 'EOF' at 0:3


def ex__eof():
    # NOTE: doesn't need to be instantiated first  (kinda like a pre-built parser)

    print(eof.parse(""))

    try:
        print(eof.parse("foo"))
    except ParseError as e:
        print(e)                                    # expected 'EOF' at 0:0

    try:
        print(eof.parse_partial("foo"))
    except ParseError as e:
        print(e)                                    # expected 'EOF' at 0:0


def ex__success():
    p = success("hello")

    print(p.parse(""))                              # hello

    try:
        print(p.parse("foo"))
    except ParseError as e:
        print(e)                                    # expected 'EOF' at 0:0


##
##  Parser Methods
##


def ex__desc():
    p = string("foo").desc("mydesc")
    try:
        print(p.parse("bar"))
    except ParseError as e:
        print(e)									# expected 'mydesc' at 0:0

    p = test_char(lambda c: c == "f", "mydesc1").desc("mydesc2")
    try:
        print(p.parse("bar"))
    except ParseError as e:
        print(e)                                    # expected 'mydesc2' at 0:0

    p = string_from("foo", "bar").desc("mydesc")
    try:
        print(p.parse("baz"))
    except ParseError as e:
        print(e)                                    # expected 'mydesc' at 0:0

    try:
        print(eof.desc("mydesc").parse("foo"))
    except ParseError as e:
        print(e)                                    # expected 'mydesc' at 0:0


def ex__then_and_skip():
    p = string("foo").then(string("bar"))
    print(p.parse("foobar"))                        # bar

    p = string("foo").skip(string("bar"))
    print(p.parse("foobar"))                        # foo


def ex__many():
    p = string("f").many()
    print(p.parse("f"))                             # ['f']
    print(p.parse("ff"))                            # ['f', 'f']

    try:
        print(p.parse("ffb"))
    except ParseError as e:
        print(e)                                    # expected one of 'EOF', 'f', at 0:2

    print(p.parse_partial("ffb"))                   # (['f', 'f'], 'b')


def ex__times():
    p = string("f").times(2)
    print(p.parse("ff"))                            # ['f', 'f']

    try:
        print(p.parse("f"))
    except ParseError as e:
        print(e)                                    # expected 'f' at 0:1

    try:
        print(p.parse("fff"))
    except ParseError as e:
        print(e)                                    # expected 'EOF' at 0:2


def ex__optional():
    p = string("foo").optional()
    print(p.parse(""))                              # None
    print(p.parse("foo"))                           # foo

    p = string("foo").optional("bar")
    print(p.parse(""))                              # bar
    print(p.parse("foo"))                           # foo


def ex__map():
    p = string("foo").map(lambda v: v.upper())
    print(p.parse("foo"))                           # FOO

    p = string("f").many().map(lambda v: v * 2)
    print(p.parse("ff"))                            # ['f', 'f', 'f', 'f']


def ex__combine():
    p = regex(r"(\d+)\*((\d+))", group=(1,2)).combine(lambda x, y: int(x) * int(y))
    print(p.parse("7*8"))                           # 56


def ex__seq():
    p = seq(string("foo"), string("bar"))
    print(p.parse("foobar"))                        # ['foo', 'bar']

    p = seq(
        f=string("foo"),
        _sep=string("-"),                           # underscores are included by seq
        b=string("bar"),
    )
    print(p.parse("foo-bar"))                       # {'f': 'foo', '_sep': '-', 'b': 'bar'}


def ex__seq_and_combine_dict():
    p = seq(
        f=string("foo"),
        _sep=string("-"),                           # underscores are omitted by combine_dict
        b=string("bar"),
    ).combine_dict(dict)
    print(p.parse("foo-bar"))



##
##  Main
##


##  Parsing Primitives

ex__string()
ex__regex()
ex__test_char()
ex__string_from()
ex__eof()
ex__success()

##  Parser Methods

ex__desc()
ex__then_and_skip()
ex__many()
ex__times()
ex__optional()
ex__map()
ex__combine()
ex__seq()
ex__seq_and_combine_dict()

