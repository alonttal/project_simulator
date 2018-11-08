from tcp_packet import TcpFlag, TcpPacket
from ip_header import IpHeader


class TcpParser:
    ACK_MASK = 0x10

    def __build_ip_header(self, raw_ip_header):
        return IpHeader(
            raw_ip_header.len,
            raw_ip_header.ttl,
            raw_ip_header.src,
            raw_ip_header.dst
        )

    def __build_tcp_packet(self, raw_tcp_packet, ip_header):
        flags = []
        if raw_tcp_packet.flags & TcpParser.ACK_MASK:
            # print("ACK FLAG")
            flags.append(TcpFlag.ACK)
        # if raw_tcp_packet.flags & 0x08:
        #     print("RST FLAG")

        return TcpPacket(
            ip_header,
            raw_tcp_packet.sport,
            raw_tcp_packet.dport,
            raw_tcp_packet.seq,
            raw_tcp_packet.ack,
            raw_tcp_packet.dataofs,
            flags,
            raw_tcp_packet.window,
            raw_tcp_packet.chksum,
            raw_tcp_packet.urgptr,
            raw_tcp_packet.options
        )

    def parse(self, packet):
        ip_header = self.__build_ip_header(packet['IP'])
        tcp_packet = self.__build_tcp_packet(packet['TCP'], ip_header)
        return tcp_packet
