class SubConnection:
    DEFAULT_CONNECTION_ID_LENGTH = 64

    def __init__(self,
                 of_connection_num,
                 destination_connection_id,
                 source_ip,
                 start_time,
                 end_time,
                 is_initial=False):
        self.of_connection_num = of_connection_num
        self.destination_connection_id = destination_connection_id
        self.source_ip = source_ip
        self.start_time = start_time
        self.end_time = end_time
        self.is_initial = is_initial
