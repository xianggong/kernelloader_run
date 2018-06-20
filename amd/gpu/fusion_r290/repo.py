import os.path

exe_arg_dict = {
    'mriQ': ["dataset/small/32_32_32_dataset.bin"],
    'spmv': ["dataset/small/input/1138_bus.mtx",
             "dataset/small/input/vector.bin"],
    'sad': ["dataset/default/input/reference.bin",
            "dataset/default/input/frame.bin"],
    'sgemm': ["dataset/small/input/matrix1.txt",
              "dataset/small/input/matrix2.txt",
              "dataset/small/input/matrix2t.txt"],
    'bfs': ["dataset/1M/graph_input.dat"],
}


class ExeRepo(object):
    """ExeRepo contains a list of absolute path of the .so files"""

    def __init__(self, file):
        self.exe_list = [x.strip() for x in file.readlines()]
        # Path to so file
        self.exe_dict = {}
        # Arguments
        self.arg_dict = {}

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
            # Without 'lib' prefix
            exec_name = self.getExecName(item)[3:]
            self.exe_dict[exec_name] = item
        # print self.exe_dict

    def initArgDict(self):
        for exec_name, exec_path in self.exe_dict.iteritems():
            # Directory absolute path
            exec_path = os.path.dirname(exec_path) + "/"

            args = ""
            if exec_name not in exe_arg_dict:
                # Polybench default args
                args = "i 1"
            else:
                # Parboil default args
                args = "i "
                for arg in exe_arg_dict[exec_name]:
                    arg = exec_path + arg
                    if os.path.isfile(arg):
                        args += arg + " "
                    else:
                        exit(0)

            self.arg_dict[exec_name] = args
        # print self.arg_dict

    def initRepo(self):
        self.initExeDict()
        self.initArgDict()
        if not self.exe_repo:
            for key, value in self.exe_dict.iteritems():
                self.exe_repo[key] = [value, self.arg_dict[key]]

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
