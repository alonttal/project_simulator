class QuicPacket:
    DEFAULT_CONNECTION_ID_LENGTH = 64

    def __init__(self,
                 source_ip,
                 destination_connection_id,
                 send_time,
                 is_initial=False):
        self.source_ip = source_ip
        self.destination_connection_id = destination_connection_id
        self.send_time = send_time
        self.is_initial = is_initial
