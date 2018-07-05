import os as _os
import subprocess
from src.base.enums import OperationSystem
from src.test_utils.os_utils import detect_os
from src.test_utils.file_utils import write_file_output


class Terminal(object):
    @classmethod
    def set_up_class(cls):
        if detect_os() == OperationSystem.WINDOWS.value:
            print("It's Windows OS.   ")
        else:
            print("It's kind of Unix OS.   ")

    @classmethod
    def get_cur_date(cls):
        process = subprocess.check_output("date")
        print('Current date is:', process.decode("utf-8"))

    @classmethod
    def ping_host(cls, host):
        process = subprocess.run(['ping', host], stdout=subprocess.PIPE)
        return process.stdout

    @classmethod
    def run_cd(cls, dir_name):
        _os.chdir(dir_name)

    @classmethod
    def run_newman(self, command):
        proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        process = str(proc.stdout)
        return process

    @classmethod
    def run_command_out(cls, command, file, *option, **option2):
        command = list(command)
        if (option):
            command.append(option)
        if (option2):
            command.append(option2)
        try:
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate(
                timeout=100)[0]
            process = proc.decode("utf-8")
            write_file_output(process, file)
            return process
        except subprocess.TimeoutExpired:
            raise TimeoutError

    @classmethod
    def run_command_in(cls, command, *option):
        if(option):
            list(command)
            command.append(option)
        else:
            list(command)
        try:
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate(timeout=100)[0]
            return proc
        except subprocess.TimeoutExpired:
            raise TimeoutError
