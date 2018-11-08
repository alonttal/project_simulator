import time
from threading import Thread, Lock
from typing import Dict


class ConnectionsMapEntry:
    def __init__(self, timestamp, timeout):
        self.timestamp = timestamp
        self.timeout = timeout


class ConnectionsTracker:
    def __init__(self):
        self.__lock = Lock()
        self.__active = False
        self.__tracker_thread = Thread(None, self.__thread_track)
        self.__connections_map: Dict[str, ConnectionsMapEntry] = {}

        # TODO: remove
        self.__connections_map.update({'139283821': ConnectionsMapEntry(time.time(), 7)})

    def __thread_track(self):
        i = 0

        while self.__active:
            i += 1
            print(str(i) + " iteration")
            remove_keys = []
            for k, v in self.__connections_map.items():
                if time.time() - v.timestamp >= v.timeout:
                    print("removing " + k)
                    remove_keys.append(k)
            for k in remove_keys:
                self.__connections_map.pop(k)
            time.sleep(1)

    def start_tracking(self):
        self.__lock.acquire()
        if not self.__active:
            self.__active = True
            self.__tracker_thread.start()
            print("tracker started")
        self.__lock.release()

    def stop_tracking(self):
        self.__lock.acquire()
        if self.__active:
            self.__active = False
            self.__tracker_thread.join()
            print("tracker stopped")
        self.__lock.release()
