# import time module, Observer, FileSystemEventHandler
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pyAesCrypt
import logging
logging.basicConfig(filename="Decryptor.log",
                    level=logging.INFO, format="%(asctime)s:%(filename)s:%(lineno)d:%(message)s")

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
decryptor_path = desktop+"\\aes_decryptor"

if not os.path.exists(decryptor_path):
    os.mkdir(decryptor_path)


class OnMyWatch:
    # Set the directory on watch
    watchDirectory = decryptor_path

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
            if srcPath.find(".aes") != -1:
                decrptor(srcPath)
            else:
                pass
        else:
            pass
    
    
def decrptor(srcPath):
    bufferSize = 64 * 1024
    password = "js198989"
    try:
        infile = srcPath
        outfile = srcPath.replace('.aes', '')
        pwd = password
        buffSize = bufferSize
        pyAesCrypt.decryptFile(infile, outfile, pwd, buffSize)
        os.remove(infile)
        return True
    except Exception as ex:
        logging.exception(f"ERROR-MESSAGE")
        pass


if __name__ == '__main__':
    logging.info("Decryptor Started Working...")
    watch = OnMyWatch()
    watch.run()