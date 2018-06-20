#!/usr/bin/env python


import argparse
import sys
from repo import *
sys.path.append("../../../util/")
from config import *


def main():
    parser = argparse.ArgumentParser(
        description="Execution INI file generator")

    parser.add_argument("--cu", metavar="<cu>", type=int,
                        help="Number of Compute Unit")
    parser.add_argument("--arg", metavar="<arg>", type=argparse.FileType("r"),
                        help="List of path of argument config file")
    parser.add_argument("--exe", metavar="<exe>", type=argparse.FileType("r"),
                        help="List of path of executables")
    parser.add_argument("--src", metavar="<src>", type=argparse.FileType("r"),
                        help="List of path of OpenCL kernel source")
    parser.add_argument("--mrg", metavar="<mrg>", type=argparse.FileType("r"),
                        help="List of path of Merged OpenCL kernel source")

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

    mrg_repo = SrcRepo(args.mrg)
    # for k, v in mrg_repo.getRepo().iteritems():
    #     print k, v

    # print exe_repo.getRepo().keys()
    # print src_repo.getRepo().keys()
    # print mrg_repo.getRepo().keys()

    for key, value in mrg_repo.getRepo().iteritems():
        k0_name = key.split("_and_")[0]
        k1_name = key.split("_and_")[1]

        # print k0_name, k1_name
        k0_exe = exe_repo.getInfo(k0_name)
        k0_arg = arg_repo.getInfo(k0_name)
        k0_src = src_repo.getInfo(k0_name)

        k1_exe = exe_repo.getInfo(k1_name)
        k1_arg = arg_repo.getInfo(k1_name)
        k1_src = src_repo.getInfo(k1_name)

        km_src = mrg_repo.getInfo(key)

        condition = [k0_exe, k0_arg, k0_src, k1_exe, k1_arg, k1_src, km_src]
        if all(condition):
            app0 = AppSingle("0", k0_exe, k0_arg, k0_src, "")
            app1 = AppSingle("1", k1_exe, k1_arg, k1_src, "")
            appm = AppFusion(app0, app1, km_src, "")

            for k, v in appm.Dump(args.cu).iteritems():
                try:
                    os.stat(k)
                except:
                    os.mkdir(k)

                ouput_name = k + ".ini"
                ouput = open(os.path.join(k, ouput_name), "w")
                ouput.write(v)
                ouput.close()
    return


if __name__ == "__main__":
    main()
