import sys
import re
import json
from datetime import datetime
import pytz


def main(file_name: str):
    template_file_name = file_name.split('.')[0] + '_parameters.json'

    # get the current time in UTC
    now_utc = datetime.now(tz=pytz.utc)

    # format the time in ISO 8601 format with a timezone designator
    now_iso = now_utc.strftime('%Y-%m-%dT%H:%M:%SZ')

    with open(file_name, 'r') as file:
        data = file.read().replace('\n', '')

    parameters = set(re.findall('\$.*?\$', data))
    out_dict = dict()
    for p in parameters:
        parameter_name = p[1:-1]
        if parameter_name == 'iso_time':
            out_dict[parameter_name] = now_iso
        else:
            out_dict[parameter_name] = ''

    with open(template_file_name,'w') as out:
        json.dump(out_dict,out,indent=4, sort_keys=True)

if __name__ == '__main__':
    main(sys.argv[1])