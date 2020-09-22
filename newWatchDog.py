# import time module, Observer, FileSystemEventHandler
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pyAesCrypt
import logging
logging.basicConfig(filename="/home/dimaa/Downloads/watchDog.log",
                    level=logging.INFO, format="%(asctime)s:%(filename)s:%(lineno)d:%(message)s")


class OnMyWatch:
    # Set the directory on watch
    watchDirectory = "/home/dimaa/Downloads/testDir"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(
            event_handler, self.watchDirectory, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif (event.event_type == 'created' or event.event_type == 'modified') and event.event_type != 'deleted':
            # Event is modified, you can process it now
            logging.info(f"Watchdog received modified event - {event.src_path}")
            srcPath = event.src_path
            if srcPath.find(".aes") == -1:
                encrptor(srcPath)
            else:
                pass
        else:
            pass
    
    
def encrptor(srcPath):
    bufferSize = 64 * 1024
    password = "3F1A18279BA64A38A215931601B946F4"
    try:
        infile = srcPath
        outfile = srcPath+".aes"
        pwd = password
        buffSize = bufferSize
        pyAesCrypt.encryptFile(infile, outfile, pwd, buffSize)
        os.system(f"rm -f {infile}")

        return True
    except Exception as ex:
        print(ex)
        pass


if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()
