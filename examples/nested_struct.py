#!/usr/bin/env python

from hydras import *


class Header(Struct):
    Opcode = uint16_t
    SourceID = uint8_t
    DestinationID = uint8_t
    PayloadLength = uint64_t
    CRC = uint32_t


class SyncMessage(Struct):
    Header = Header(Opcode=1, PayloadLength=0)


class AckMessage(Struct):
    Header = Header(Opcode=2, PayloadLength=0)


class DataFragmentMessage(Struct):
    Header = Header(Opcode=3, PayloadLength=1024)
    Payload = Array(1024)


if __name__ == '__main__':
    msg = DataFragmentMessage()
    # =>
    # Header:
    # 	Opcode: 3
    # 	SourceID: 0
    # 	DestinationID: 0
    # 	PayloadLength: 1024
    # 	CRC: 0
    # Payload: [0, 0, 0, 0, 0, ..., 0]

    msg.Payload = b'SomeOtherData'
    msg.Header.PayloadLength = len(msg.Payload)

    raw_data = msg.serialize()
    # =>
    # b'030000000d0000000000000000000000536f6d654f74686572446174610000000000000000 ...
    #  ^ Header start                  ^ Payload start
