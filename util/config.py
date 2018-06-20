import os.path
import clang.cindex

clang.cindex.Config.set_library_file("/usr/lib/llvm-5.0/lib/libclang.so.1")


class AppSingle(object):
    """Single application"""

    def __init__(self, index, executable, args, source, binary):
        self.index = index
        self.executable = executable
        self.args = args
        self.source = source
        self.binary = binary

        self.funcList = []
        self._init_func_list()

    def _init_func_list(self):
        index = clang.cindex.Index.create()
        tu = index.parse(self.source)
        self.FindFunctionFromSource(tu.cursor, self.source)

    def FindFunctionFromSource(self, node, file):
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            self.funcList.append(node.spelling)

        for c in node.get_children():
            self.FindFunctionFromSource(c, file)

    def GetFunctions(self):
        return self.funcList

    def HasFunction(self, name):
        if name in self.funcList:
            return True
        else:
            return False

    def Dump(self):
        ini = "[ APP" + str(self.index) + " ]\n"

        # Check executable path
        if os.path.isfile(self.executable):
            ini += "EXEC=" + self.executable + "\n"
            ini += "ARGS=" + self.args + "\n"

        # Check source path
        if os.path.isfile(self.source):
            ini += "KRNL=" + self.source + "\n"

        # Check binary path
        if os.path.isfile(self.binary):
            ini += "BIN=" + self.binary + "\n"

        return ini


class AppFusion(object):
    """Fusion application"""

    def __init__(self, app0, app1, source, binary):
        self.app0 = app0
        self.app1 = app1
        self.appm = AppSingle("M", "", "", source, binary)

    def getFunctions(self):
        return self.appm.GetFunctions()

    def Dump(self, denominator=32, step=1):
        ini_dict = {}

        fusion_func_list = self.appm.GetFunctions()
        for function in fusion_func_list:
            kernel_func_0 = function.split("_and_")[0]
            kernel_func_1 = function.split("_and_")[1]

            # Check if the standalone kernel source contains the function
            has_kernel_func_0 = self.app0.HasFunction(kernel_func_0)
            has_kernel_func_0 |= self.app1.HasFunction(kernel_func_0)
            has_kernel_func_1 = self.app1.HasFunction(kernel_func_1)
            has_kernel_func_1 |= self.app0.HasFunction(kernel_func_1)

            if has_kernel_func_0 and has_kernel_func_1:
                for numerator in range(1, denominator, step):
                    ini = ""

                    # Dump seperate apps
                    ini += self.app0.Dump() + "\n"
                    ini += self.app1.Dump() + "\n"
                    ini += self.appm.Dump() + "\n"

                    # Dump mix ratio setting
                    ini += "[ MIX ]\n"
                    ini += "KRNL0=" + kernel_func_0 + "\n"
                    ini += "KRNL1=" + kernel_func_1 + "\n"
                    ini += "M=" + str(denominator) + "\n"
                    ini += "N=" + str(numerator) + "\n"

                    # Add to dict
                    key = kernel_func_0 + "_and_" + kernel_func_1 + \
                        "_" + str(denominator) + "_" + str(numerator)
                    ini_dict[key] = ini

        return ini_dict

    def DumpOne(self, name, m, n):
        function = name

        kernel_func_0 = function.split("_and_")[0]
        kernel_func_1 = function.split("_and_")[1]

        # Check if the standalone kernel source contains the function
        has_kernel_func_0 = self.app0.HasFunction(kernel_func_0)
        has_kernel_func_0 |= self.app1.HasFunction(kernel_func_0)
        has_kernel_func_1 = self.app1.HasFunction(kernel_func_1)
        has_kernel_func_1 |= self.app0.HasFunction(kernel_func_1)

        if has_kernel_func_0 and has_kernel_func_1:
            ini = ""

            # Dump seperate apps
            ini += self.app0.Dump() + "\n"
            ini += self.app1.Dump() + "\n"
            ini += self.appm.Dump() + "\n"

            # Dump mix ratio setting
            ini += "[ MIX ]\n"
            ini += "KRNL0=" + kernel_func_0 + "\n"
            ini += "KRNL1=" + kernel_func_1 + "\n"
            ini += "M=" + str(m) + "\n"
            ini += "N=" + str(n) + "\n"

        return ini
