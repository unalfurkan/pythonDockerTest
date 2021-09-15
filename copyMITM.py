import multiprocessing
import os
import signal
import subprocess
import time


class MITM:
    def __start_mitm(self, __mitm_process):
        try:
            print("starting mitm proxy")
            self.__mitm_process.communicate()
            print("started: mitm proxy")
        except:
            print("crashed: mitm proxy")

    def __init__(self):
        self.process = None
        self.__mitm_process = None

    def start_mitm(self, transparent_proxy=True, outfile=''):

        if self.process is None:

            if transparent_proxy:
                print("starting mitm process as transparent proxy")
                self.__mitm_process = subprocess.Popen(['mitmdump', '--ignore-hosts', '.*'],
                                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                print("starting mitm process as sniff proxy")
                self.__mitm_process = subprocess.Popen(['mitmdump',
                                                        '-w', outfile],
                                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)


            self.process = multiprocessing.Process(name="mitm_proxy_process", target=self.__start_mitm,
                                                   args=(self.__mitm_process,))
            self.process.daemon = True  # do not work at back ground
            self.process.start()
        else:
            print("mitm process already working")

    def stop_mitm(self):
        try:
            print("stopping mitm process")
            os.kill(self.__mitm_process.pid, signal.SIGINT)
            self.process.kill()
            time.sleep(1)
            self.process = None
            print("stopped: mitm process")
        except:
            pass

print("testfile.txt create starting")

with open('testfile.txt', 'w') as fp:
    print("testfile.txt created")


out_file = "testmitmoutfile"
mitm = MITM()
time.sleep(5)
try:
    mitm.start_mitm(False, out_file)
    time.sleep(5)
finally:
    mitm.stop_mitm()
