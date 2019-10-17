#!/usr/bin/env python
"""
:file: EnumClassTests.py

This file contains tests for the 'EnumClass' type formatter.

:date: 10/06/2016
:authors:
    - Gilad Naaman <gilad@naaman.io>
"""

from .utils import *


class EOpcodeThingie(EnumClass):
    a = Literal()
    b = Literal()
    c = Literal(10)
    d = Literal()


class StructThingie(Struct):
    opcode = EOpcodeThingie
    pad = u8(0xFF)


class StructStuff(Struct):
    opcode = EOpcodeThingie(type_formatter=u8)


class EnumClassTests(HydrasTestCase):
    def test_enum_class(self):
        s = StructThingie()

        # Test values
        s.opcode = EOpcodeThingie.a
        self.assertEqual(s.serialize(), b'\x00\x00\x00\x00\xFF')
        s.opcode = EOpcodeThingie.b
        self.assertEqual(s.serialize(), b'\x01\x00\x00\x00\xFF')
        s.opcode = EOpcodeThingie.c
        self.assertEqual(s.serialize(), b'\x0a\x00\x00\x00\xFF')
        s.opcode = EOpcodeThingie.d
        self.assertEqual(s.serialize(), b'\x0b\x00\x00\x00\xFF')

    def test_sized_enum_class(self):
        s = StructStuff()

        s.opcode = EOpcodeThingie.a
        self.assertEqual(s.serialize(), b'\x00')
        s.opcode = EOpcodeThingie.b
        self.assertEqual(s.serialize(), b'\x01')
        s.opcode = EOpcodeThingie.c
        self.assertEqual(s.serialize(), b'\x0a')
        s.opcode = EOpcodeThingie.d
        self.assertEqual(s.serialize(), b'\x0b')

    def test_format_options(self):
        f = EOpcodeThingie(type_formatter=u8)
        self.assertEqual(f.format(0), b'\x00')
        self.assertEqual(f.format(1), b'\x01')
        self.assertEqual(f.format(10), b'\x0a')
        self.assertEqual(f.format(11), b'\x0b')

        self.assertEqual(f.format(EOpcodeThingie.a), b'\x00')
        self.assertEqual(f.format(EOpcodeThingie.b), b'\x01')
        self.assertEqual(f.format(EOpcodeThingie.c), b'\x0a')
        self.assertEqual(f.format(EOpcodeThingie.d), b'\x0b')

        self.assertEqual(f.format('a'), b'\x00')
        self.assertEqual(f.format('b'), b'\x01')
        self.assertEqual(f.format('c'), b'\x0a')
        self.assertEqual(f.format('d'), b'\x0b')

        with self.assertRaises(KeyError):
            f.format('e')

    def test_parse_options(self):
        f = EOpcodeThingie(type_formatter=u8)
        self.assertEqual(0, f.parse('\x00'))
        self.assertEqual(10, f.parse('\x0A'))

        with self.assertRaises(ValueError):
            f.parse('\xFF')

    def test_self_compatibility(self):
        s = StructStuff()
        self.assertEqual(s, StructStuff.deserialize(s.serialize()))

    def test_enum_array(self):
        enarr = EOpcodeThingie[2]
        self.assertEqual(enarr.format((EOpcodeThingie.a, EOpcodeThingie.b)), b'\x00\x00\x00\x00\x01\x00\x00\x00')


if __name__ == '__main__':
    unittest.main()
