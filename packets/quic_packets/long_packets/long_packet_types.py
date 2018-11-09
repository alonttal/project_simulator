from enum import Enum


class LongPacketType(Enum):
    ZERO_RTT_PACKET = 0x7C
    HANDSHAKE_PACKET = 0x7D
    RETRY_PACKET = 0x7E
    INITIAL_PACKET = 0X7F
