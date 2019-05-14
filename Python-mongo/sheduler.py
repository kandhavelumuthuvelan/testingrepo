import urllib.request
import threading
 
def run_check():
    threading.Timer(30.0, run_check).start()
    print("HTTP Request sent.")
 
run_check()