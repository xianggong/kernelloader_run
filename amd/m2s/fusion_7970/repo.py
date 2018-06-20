import os.path
import pandas as pd


class ArgRepo(object):
    """ArgRepo contains a list of parameters for an executable"""

    def __init__(self, file):
        self.arg_file_list = [x.strip() for x in file.readlines()]

        self.arg_dict = {}

        self.initArgDict()

    def initArgDict(self):
        for item in self.arg_file_list:
            with open(item) as f:
                content = f.readlines()
                content = [x.strip() for x in content]
                exec_name = item.split("/")[-2]
                self.arg_dict[exec_name] = content
                # print exec_name, content

    def getInfo(self, exec_name):
        if exec_name in self.arg_dict:
            return " ".join(self.arg_dict[exec_name])
        else:
            return ""

    def getRepo(self):
        return self.arg_dict


class ExeRepo(object):
    """ExeRepo contains a list of absolute path of the .so files"""

    def __init__(self, file):
        self.exe_list = [x.strip() for x in file.readlines()]

        # Path to so file
        self.exe_dict = {}

        # Contains a pair of string with so file path and argument
        self.exe_repo = {}

        self.initRepo()

    def getExecName(self, so_file_path):
        name = os.path.basename(so_file_path).split(".")[0]
        return name

    def getInfo(self, key):
        if key in self.exe_repo.keys():
            return self.exe_repo[key]

    def initExeDict(self):
        for item in self.exe_list:
            # Without 'lib' prefix and '_m2s' postfix
            exec_name = self.getExecName(item)[3:].split("_m2s")[0]
            self.exe_dict[exec_name] = item
        # print self.exe_dict

    def initRepo(self):
        self.initExeDict()
        if not self.exe_repo:
            for key, value in self.exe_dict.iteritems():
                self.exe_repo[key] = value

    def getRepo(self):
        return self.exe_repo


class SrcRepo(object):
    """ExeRepo contains a list of absolute path of the .so files"""

    def __init__(self, file):
        self.src_list = [x.strip() for x in file.readlines()]
        # Path to so file
        self.src_dict = {}

        # Contains a pair of string with so file path and argument
        self.src_repo = {}

        self.initSrcDict()

    def getSrcName(self, so_file_path):
        name = os.path.basename(so_file_path).split(".")[0]
        return name

    def initSrcDict(self):
        for item in self.src_list:
            # Without 'lib' prefix
            src_name = self.getSrcName(item)
            self.src_dict[src_name] = item
        # print self.src_dict

    def getRepo(self):
        # If first run
        if not self.src_repo:
            for key, value in self.src_dict.iteritems():
                self.src_repo[key] = value

        return self.src_repo

    def getInfo(self, key):
        if key in self.src_dict.keys():
            return self.src_dict[key]


class BinRepo(object):
    """ExeRepo contains a list of absolute path of the .so files"""

    def __init__(self, file):
        self.bin_list = [x.strip() for x in file.readlines()]
        # Path to so file
        self.bin_dict = {}

        # Contains a pair of string with so file path and argument
        self.bin_repo = {}

        self.initBinDict()

    def getBinName(self, so_file_path):
        name = os.path.basename(so_file_path).split(".")[0]
        return name

    def initBinDict(self):
        for item in self.bin_list:
            # Without 'lib' prefix
            app_name = self.getBinName(item).split("_")[0]
            bin_schd = self.getBinName(item).split("_")[1]
            if app_name not in self.bin_dict.keys():
                self.bin_dict[app_name] = {}
                self.bin_dict[app_name][bin_schd] = item
            else:
                self.bin_dict[app_name][bin_schd] = item
        # print self.bin_dict

    def getRepo(self):
        # If first run
        if not self.bin_repo:
            for key, value in self.bin_dict.iteritems():
                self.bin_repo[key] = value

        return self.bin_repo

    def getInfo(self, key):
        if key in self.bin_dict.keys():
            return self.bin_dict[key]

class FltRepo(object):
    """FltRepo contain s a list of kernel pairs and the ratio"""

    def __init__(self, file):
        self.filter = {}
        self.df = pd.read_csv(file)
        # print self.df
        self.init()

    def init(self):
        count_speedup = 0
        count_slowdown = 0

        for benchmark in self.df['benchmark'].unique():
            # print benchmark
            benchInfo = self.df[self.df['benchmark'] == benchmark]
            benchBest = self.df.iloc[[benchInfo['speedup'].idxmax()]]

            if benchBest['speedup'].values[0] > 1.0:
                # print benchmark, benchBest['m'].values[0], benchBest['speedup'].values[0]
                count_speedup += 1
                self.filter[benchmark] = [
                    benchBest['m'].values[0], benchBest['speedup'].values[0]]
            else:
                count_slowdown += 1
                # print benchmark, benchBest['speedup'].values[0]

            #     self.filter[benchmark] = [0, benchBest['speedup'].values[0]]
        # print self.filter

        print count_speedup, count_slowdown, count_speedup + count_slowdown

    def getInfo(self, benchmark):
        return self.filter.get(benchmark, None)