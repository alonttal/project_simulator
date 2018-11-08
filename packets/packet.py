class Packet:
    def __init__(self,
                 header_form,
                 reserved_bits,
                 destination_connection_id):
        self.header_form = header_form
        self.reserved_bits = reserved_bits
        self.destination_connection_id = destination_connection_id
