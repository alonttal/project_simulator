import csv


class Exporter:
    EXPORTS_DIRECTORY = 'exports/'


class CsvExporter(Exporter):
    def export(self,
               file_name,
               times,
               real_number_of_connections,
               estimated_number_of_connections):
        with open(Exporter.EXPORTS_DIRECTORY + file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['times', 'real number of connections', 'estimated number of connections'])
            for i in range(0, len(times)):
                writer.writerow([times[i], real_number_of_connections[i], estimated_number_of_connections[i]])
