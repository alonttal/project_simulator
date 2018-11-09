class IpHeader:
    def __init__(self,
                 total_length,
                 ttl,
                 source_ip,
                 destination_ip):
        self.total_length = total_length
        self.ttl = ttl
        self.source_ip = source_ip
        self.destination_ip = destination_ip
