class IpWindow:
    def __init__(self, ip, start_time, end_time, belongs_to_client):
        self.belongs_to_client = belongs_to_client
        self.end_time = end_time
        self.start_time = start_time
        self.ip = ip
        self.initial_num = 0
        self.non_initial_num = 0

