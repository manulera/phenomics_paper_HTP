import sys
import json


def main(template_file, template_values_file):
    with open(template_values_file) as ins:
        template_values = json.load(ins)

    with open(template_file) as ins:
        template = ins.read()

    max_len = 1
    for value in template_values.values():
        if type(value) == list:
            max_len = max(len(value),max_len)

    with open('output.owl','w') as out:
        for i in range(max_len):
            this_chunk = template
            for key in template_values:
                value = template_values[key]
                if type(value) == list:
                    this_chunk = this_chunk.replace(f'${key}$',value[i])

                else:
                    this_chunk = this_chunk.replace(f'${key}$',value)
            out.write(this_chunk)
            out.write('\n')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])