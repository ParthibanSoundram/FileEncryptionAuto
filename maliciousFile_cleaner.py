# import time module, Observer, FileSystemEventHandler
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from OTXv2 import OTXv2
import argparse
import IndicatorTypes
import hashlib

import logging
logging.basicConfig(
    filename="/home/dimaa/Documents/rough-work/watchDog.log",
    level=logging.INFO, format="%(asctime)s:%(filename)s:%(lineno)d:%(message)s"
)

API_KEY = 'b8604201fee2be44a75e20fc88ba089c1d4bd231c3f473a36f8fa0334b1edc56'
OTX_SERVER = 'https://otx.alienvault.com/'
otx = OTXv2(API_KEY, server=OTX_SERVER)


class OnMyWatch:
    try:
        # Set the directory on watch
        watchDirectory = "/home/dimaa/Downloads/"
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
    except Exception as ex:
        print(f"OnMyWatch : {ex}")


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        # elif (event.event_type == 'created' or event.event_type == 'modified') and event.event_type != 'deleted':
        elif (event.event_type == 'created'):
            # Event is modified, you can process it now
            logging.info(f"Watchdog received modified event - {event.src_path}")
            srcPath = event.src_path
            otxScanner(srcPath)
        else:
            pass
    
# Get a nested key from a dict, without having to do loads of ifs
def getValue(results, keys):
    if type(keys) is list and len(keys) > 0:
        if type(results) is dict:
            key = keys.pop(0)
            if key in results:
                return getValue(results[key], keys)
            else:
                return None
        else:
            if type(results) is list and len(results) > 0:
                return getValue(results[0], keys)
            else:
                return results
    else:
        return results


def file_(otx, hash):
    alerts = []
    hash_type = IndicatorTypes.FILE_HASH_MD5
    if len(hash) == 64:
        hash_type = IndicatorTypes.FILE_HASH_SHA256
    if len(hash) == 40:
        hash_type = IndicatorTypes.FILE_HASH_SHA1
    result = otx.get_indicator_details_full(hash_type, hash)

    avg = getValue( result, ['analysis','analysis','plugins','avg','results','detection'])
    if avg:
        alerts.append({'avg': avg})

    clamav = getValue( result, ['analysis','analysis','plugins','clamav','results','detection'])
    if clamav:
        alerts.append({'clamav': clamav})

    avast = getValue( result, ['analysis','analysis','plugins','avast','results','detection'])
    if avast:
        alerts.append({'avast': avast})

    microsoft = getValue( result, ['analysis','analysis','plugins','cuckoo','result','virustotal','scans','Microsoft','result'])
    if microsoft:
        alerts.append({'microsoft': microsoft})

    symantec = getValue( result, ['analysis','analysis','plugins','cuckoo','result','virustotal','scans','Symantec','result'])
    if symantec:
        alerts.append({'symantec': symantec})

    kaspersky = getValue( result, ['analysis','analysis','plugins','cuckoo','result','virustotal','scans','Kaspersky','result'])
    if kaspersky:
        alerts.append({'kaspersky': kaspersky})

    suricata = getValue( result, ['analysis','analysis','plugins','cuckoo','result','suricata','rules','name'])
    if suricata and 'trojan' in str(suricata).lower():
        alerts.append({'suricata': suricata})
    return alerts


def isMalicious_file(file1):
    try:
        otxRes = file_(otx, file1)
        if len(otxRes) > 0:
            return True
        else:
            return False
    except Exception as ex:
        print(f"Exception : {ex}")
        return False


def otxScanner(srcPath):
    try:
        hash = hashlib.md5(open(srcPath, 'rb').read()).hexdigest()
        otxResp = isMalicious_file(hash)
        if otxResp == True:
            os.system(f"rm -f {srcPath}")
            logging.info(f"!!! ALERT.. Malicious File Found in {srcPath}. It's Removed Successfully.")
    except Exception as ex:
        pass

if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()
    # otxScanner("/home/dimaa/Downloads/eicar_com.zip")
