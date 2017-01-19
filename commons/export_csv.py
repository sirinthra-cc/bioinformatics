import csv
from _csv import QUOTE_NONE

from django.http import StreamingHttpResponse


class Echo(object):

    def write(self, value):
        return value


def get_streaming_response(output_name, output_path):
    rf = open(output_path, 'r')
    reader = csv.reader(rf, delimiter='\t')
    rows = [row for row in reader]

    wf = Echo()
    writer = csv.writer(wf, delimiter='\t', quotechar='', quoting=QUOTE_NONE)
    response = StreamingHttpResponse([writer.writerow(row) for row in rows],
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="%s.vcf"' % output_name
    return response
