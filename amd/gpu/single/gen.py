#!/usr/bin/env python


import argparse
import sys
from repo import *
sys.path.append("../../../util/")
from config import *


def main():
    parser = argparse.ArgumentParser(
        description="Execution INI file generator")

    parser.add_argument("--exe", metavar="<exe>", type=argparse.FileType("r"),
                        help="List of path of executables")
    parser.add_argument("--src", metavar="<src>", type=argparse.FileType("r"),
                        help="List of path of OpenCL kernel source")
    parser.add_argument("--bin", metavar="<bin>", type=argparse.FileType("r"),
                        help="List of path of OpenCL kernel binary")

    args = parser.parse_args()

    exe_repo = ExeRepo(args.exe)
    # for k, v in exe_repo.getRepo().iteritems():
    #     print k, v

    src_repo = SrcRepo(args.src)
    # for k, v in src_repo.getRepo().iteritems():
    #     print k, v

    bin_repo = BinRepo(args.bin)
    # for k, v in bin_repo.getRepo().iteritems():
    #     print k, v

    for k, v in exe_repo.getRepo().iteritems():
        app_exe = v[0]
        app_arg = v[1]
        app_src = src_repo.getInfo(k)
        app_bin = bin_repo.getInfo(k)

        # print app_exe, app_arg, app_src
        # print app_bin_dict

        condition = [app_exe, app_arg, app_src, app_bin]
        if all(condition):
            app = AppSingle("0", app_exe, app_arg, app_src, app_bin)
            ouput_name = k + ".ini"
            # print ouput_name

            try:
                os.stat(k)
            except:
                os.mkdir(k)

            ouput = open(os.path.join(k, ouput_name), "w")
            ouput.write(app.Dump())
            ouput.close()

    return


if __name__ == "__main__":
    main()
