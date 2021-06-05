# import time module, Observer, FileSystemEventHandler
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pyAesCrypt
import logging
logging.basicConfig(filename="Encryptor.log",
                    level=logging.INFO, format="%(asctime)s:%(filename)s:%(lineno)d:%(message)s")


def ignore_pathVerifier(srcPath):
    ignoreList = ['avatars',  'files_external',  'index.html', 'owncloud.log', 'ocTransferId', 'part']
    try:
        path_list = srcPath.split("/")
        ### Compare the string found or not
        result = set(ignoreList) & set(path_list)
        if result:
            return "ignore"
        else:
            return "allow"
    except Exception as ex:
        logging.exception(f"ERROR-MESSAGE")
        return "allow"



class OnMyWatch:
    # Set the directory on watch
    watchDirectory = "/var/www/html/owncloud/data/"
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
        if event.event_type == 'created' or event.event_type == 'modified' or event.event_type == 'moved': 
            # Event is modified, you can process it now
            logging.info(f"Watchdog received modified event - {event.src_path}")
            srcPath = event.src_path
            if os.path.isfile(srcPath) == True and srcPath.find(".aes") == -1 and srcPath.find("ocTransferId") == -1:
                if ignore_pathVerifier(srcPath) == "allow":
                    encrptor(srcPath)
                else:pass
            else:
                pass
        else:
            pass

def encrptor(srcPath):
    bufferSize = 64 * 1024
    password = "js198989"
    try:
        infile = srcPath
        outfile = srcPath+".aes"
        pwd = password
        buffSize = bufferSize
        pyAesCrypt.encryptFile(infile, outfile, pwd, buffSize)
        os.system(f"rm -f {infile}")
        return True
    except Exception as ex:
        logging.exception(f"ERROR-MESSAGE")
        pass


if __name__ == '__main__':
    logging.info("Encryptor Started Working...")
    watch = OnMyWatch()
    watch.run()