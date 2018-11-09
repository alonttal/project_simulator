class UdpHeader:
    def __init__(self,
                 source_port,
                 destination_port,
                 length,
                 checksum):
        self.source_port = source_port
        self.destination_port = destination_port
        self.length = length
        self.checksum = checksum
