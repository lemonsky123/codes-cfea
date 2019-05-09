import sys
from collections import defaultdict


def parse_file(path):
    print(f"Start parsing file {path}")
    sample_items = defaultdict(dict)
    with open(path) as f:
        for line in f:
            if line.startswith("^SAMPLE = "):
                line_list = line.strip().split("= ")
                sample_name = line_list[1]
                print(f"\tStart parsing sample {sample_name}")
            elif line.startswith("!Sample_title = "):
                line_list = line.strip().split("= ")
                sample_items[sample_name]["sample_title"] = line_list[1]
            elif line.startswith("!Sample_source_name_ch1 = "):
                line_list = line.strip().split("= ")
                sample_items[sample_name]["sample_source"] = line_list[1]
            elif line.startswith("!Sample_organism_ch1 = "):
                line_list = line.strip().split("= ")
                sample_items[sample_name]["sample_organism"] = line_list[1]
            elif line.startswith("!Sample_characteristics_ch1 = tissue:"):
                line_list = line.strip().split(": ")
                sample_items[sample_name]["tissue"] = line_list[1]
            elif line.startswith("!Sample_characteristics_ch1 = molecule subtype:"):
                line_list = line.strip().split(": ")
                sample_items[sample_name]["molecule_subtype"] = line_list[1]
            elif line.startswith("!Sample_data_processing = Genome_build:"):
                line_list = line.strip().split(": ")
                sample_items[sample_name]["genome_build"] = line_list[1]
            elif line.startswith("!Sample_description =") and not line.startswith("!Sample_description = Sample name:"):
                line_list = line.strip().split("= ")
                sample_items[sample_name]["sample_description"] = line_list[1]
    return sample_items


def write(sample_items, path_out):
    print(f"Start writing to {path_out}")
    items = []
    for each_sample in sample_items:
        this_sample_values = sample_items[each_sample]
        items.extend(list(this_sample_values.keys()))
    items = list(set(items))
    with open(path_out, "w+") as out:
        out.write("sample" + "\t" + "\t".join(items) + "\n")
        for each_sample in sample_items:
            this_sample_values = sample_items[each_sample]
            this_sample_list = []
            for each_item in items:
                if each_item in this_sample_values:
                    this_sample_list.append(this_sample_values[each_item])
                else:
                    this_sample_list.append("NA")
            out.write(each_sample + "\t" + "\t".join(this_sample_list) + "\n")


def main():
    if len(sys.argv) < 3:
        print(f"Usage: python parseRawData.py GSE110185_family.soft bioproject.6.meta.xls")
        exit(0)
    path = sys.argv[1]
    path_out = sys.argv[2]
    sample_items = parse_file(path)
    write(sample_items, path_out)


if __name__ == '__main__':
    main()
