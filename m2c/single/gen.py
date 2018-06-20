#!/usr/bin/env python

import argparse
import sys
from repo import *
sys.path.append("../../util/")
from config import *


def main():
    parser = argparse.ArgumentParser(
        description="Execution INI file generator")

    parser.add_argument("--arg", metavar="<arg>", type=argparse.FileType("r"),
                        help="List of path of argument config file")
    parser.add_argument("--exe", metavar="<exe>", type=argparse.FileType("r"),
                        help="List of path of executables")
    parser.add_argument("--src", metavar="<src>", type=argparse.FileType("r"),
                        help="List of path of OpenCL kernel source")
    parser.add_argument("--bin", metavar="<bin>", type=argparse.FileType("r"),
                        help="List of path of OpenCL kernel binary")

    args = parser.parse_args()

    arg_repo = ArgRepo(args.arg)
    # for k, v in arg_repo.getRepo().iteritems():
    #     print k, v

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
        app_exe = v
        app_arg = arg_repo.getInfo(k)
        app_src = src_repo.getInfo(k)
        app_bin_dict = bin_repo.getInfo(k)

        # print app_exe, app_arg, app_src
        # print app_bin_dict

        condition = [app_exe, app_arg, app_src, app_bin_dict]
        if all(condition):
            for key_schd, app_bin in app_bin_dict.iteritems():
                app = AppSingle("0", app_exe, app_arg, app_src, app_bin)

                kernels = app.GetFunctions()

                for kernel in kernels:
                    try:
                        os.stat(kernel)
                    except OSError:
                        os.mkdir(kernel)

                    try:
                        os.stat(kernel + "/" + key_schd)
                    except OSError:
                        os.mkdir(kernel + "/" + key_schd)

                    ouput_name = kernel + ".ini"
                    print ouput_name
                    ouput = open(os.path.join(
                        kernel + "/" + key_schd, ouput_name), "w")
                    ouput.write(app.Dump())
                    ouput.write("[ MIX ]\nKRNL0=" + kernel + "\n")
                    ouput.close()

    return


if __name__ == "__main__":
    main()
