import re
import os
import sys


def parse_meta(path_meta, path_bw):
    print(f"Start reading from {path_meta}")
    with open(path_meta) as file:
        for line in file:
            if line.startswith("sample"):
                continue
            line_list = line.strip().split("\t")
            if len(line_list) == 0:
                continue
            sample_name = line_list[0]
            url = line_list[8]
            cfea_number = line_list[23]
            if os.path.exists(f"{path_bw}/{cfea_number}.cov"):
                continue
            if os.path.exists(f"{path_bw}/{cfea_number}.bed"):
                continue
            if len(url.split(",")) > 1:
                sample_url = os.path.basename(url.split(",")[0]).split(".")[0]
            else:
                sample_url = os.path.basename(url).split(".")[0]
            if re.search("_f1$", sample_url):
                sample_url = re.sub(f"_f1$", "", sample_url)
            if os.path.exists(f"{path_bw}/{sample_name}.cov"):
                print(f"Rename: {sample_name}.cov  to  {cfea_number}.cov")
                os.rename(f"{path_bw}/{sample_name}.cov", f"{path_bw}/{cfea_number}.cov")
            elif os.path.exists(f"{path_bw}/{sample_url}.cov"):
                print(f"Rename:  {sample_url}.cov  to  {cfea_number}.cov")
                os.rename(f"{path_bw}/{sample_url}.cov", f"{path_bw}/{cfea_number}.cov")
            else:
                print(f"Sample does not have a wig file, please check!  {sample_name}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python rename_bw_cf_number.py [path_meta] [path_bw]")
        exit(-1)
    path_meta = sys.argv[1]
    path_bw = sys.argv[2]
    parse_meta(path_meta, path_bw)


if __name__ == '__main__':
    main()
