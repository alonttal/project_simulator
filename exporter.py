import csv


class Exporter:
    EXPORTS_DIRECTORY = 'exports/'

    def __init__(self, file_name):
        self.file_name = Exporter.EXPORTS_DIRECTORY + file_name


class CsvExporter(Exporter):

    def __init__(self, file_name):
        super().__init__(file_name)

    def write(self, mode, *lists):
        with open(self.file_name, mode, newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            for val in zip(*lists):
                writer.writerow(val)

    def write_headers(self, *headers):
        self.write('a', *([h] for h in headers))

    def clear_file(self):
        open(self.file_name, 'w').close()
