import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler 
logging.basicConfig(filename="/home/dimaa/Downloads/watchDog.log",level=logging.INFO,format="%(asctime)s:%(filename)s:%(lineno)d:%(message)s")
path = "/home/dimaa/Downloads/testDir" #sys.argv[1] if len(sys.argv) > 1 else '.'

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')




if __name__ == "__main__":
    
    # event_handler = LoggingEventHandler()
    event_handler = MyHandler() 
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
