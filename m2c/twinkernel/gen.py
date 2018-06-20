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
    parser.add_argument("--msrc", metavar="<msrc>",
                        type=argparse.FileType("r"),
                        help="List of path of Merged OpenCL kernel source")
    parser.add_argument("--mbin", metavar="<mbin>",
                        type=argparse.FileType("r"),
                        help="List of path of Merged OpenCL kernel binary")
    parser.add_argument("--mflt", metavar="<mflt>",
                        type=argparse.FileType("r"),
                        help="List of path of filter")

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

    bin_repo = SrcRepo(args.bin)
    # for k, v in bin_repo.getRepo().iteritems():
    #     print k, v

    msrc_repo = SrcRepo(args.msrc)
    # for k, v in msrc_repo.getRepo().iteritems():
    #     print k, v

    mbin_repo = BinRepo(args.mbin)
    # for k, v in mbin_repo.getRepo().iteritems():
    #     print k, v

    mflt_repo = FltRepo(args.mflt)

    for key, value in msrc_repo.getRepo().iteritems():
        k0_name = key.split("_fuse_")[0].split("_and_")[0]
        k1_name = key.split("_fuse_")[0].split("_and_")[1]
        # print k0_name, k1_name

        k0_exe = exe_repo.getInfo(k0_name)
        k0_arg = arg_repo.getInfo(k0_name)
        k0_src = src_repo.getInfo(k0_name)

        # print k0_name, k0_exe, k0_arg, k0_src

        k1_exe = exe_repo.getInfo(k1_name)
        k1_arg = arg_repo.getInfo(k1_name)
        k1_src = src_repo.getInfo(k1_name)

        # print k1_name, k1_exe, k1_arg, k1_src

        km_src = msrc_repo.getInfo(key)

        # print km_src
        # print key
        # print mbin_repo.getInfo(key)

        if mbin_repo.getInfo(key):
            for km_bin_sched, km_bin in mbin_repo.getInfo(key).iteritems():
                sched = km_bin_sched.split("_")[0]
                k0_bin = bin_repo.getInfo("_".join([k0_name, sched]))
                k1_bin = bin_repo.getInfo("_".join([k1_name, sched]))
                # print km_bin_sched

                condition = [k0_exe, k0_arg, k0_src, k0_bin,
                             k1_exe, k1_arg, k1_src, k1_bin,
                             km_src, km_bin]

                if all(condition):
                    app0 = AppSingle("0", k0_exe, k0_arg, k0_src, k0_bin)
                    app1 = AppSingle("1", k1_exe, k1_arg, k1_src, k1_bin)
                    appm = AppFusion(app0, app1, km_src, km_bin)

                    for kernel in appm.getFunctions():
                        km_info = mflt_repo.getInfo(kernel)
                        # print key, km_info
                        if km_info is not None:
                            config = appm.DumpOne(kernel, km_info[0], 32)

                            try:
                                os.stat(kernel)
                            except OSError:
                                os.mkdir(kernel)

                            try:
                                os.stat(kernel + "/" + km_bin_sched)
                            except OSError:
                                os.mkdir(kernel + "/" + km_bin_sched)

                            for ratio in xrange(1, 10):
                                ratio = str(ratio)
                                try:
                                    os.stat(
                                        "/".join([kernel, km_bin_sched, ratio]))
                                except OSError:
                                    os.mkdir(
                                        "/".join([kernel, km_bin_sched, ratio]))

                                ouput_name = kernel + ".ini"
                                # print ouput_name

                                path = "/".join([kernel, km_bin_sched, ratio])
                                ouput = open(os.path.join(
                                    path, ouput_name), "w")
                                ouput.write(config)
                                ouput.close()
    return


if __name__ == "__main__":
    main()
