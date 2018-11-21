import time
import threading
import signal

GAZE_DATA_FILE = 'c:\\users\\nando\\desktop\\gaze_data.txt'
 
class StartReading(threading.Thread):
 
    def __init__(self):
        super(StoppableThread, self).__init__()
        threading.Thread.__init__(self)
 
        # The shutdown_flag is a threading.Event object that
        # indicates whether the thread should be terminated.
        self.shutdown_flag = threading.Event()
 
        # ... Other thread setup code here ...
 
    def run(self):
        print('Thread #%s started' % self.ident)
        os.system("C:\\Users\\nando\\CoreSDK\\samples\\Streams\\Interaction_Streams_101\\bin\\Debug\\Interaction_Streams_101.exe")
 
        while not self.shutdown_flag.is_set():
            # ... Job code here ...
            time.sleep(0.5)
 
        print('Thread #%s stopped' % self.ident)
 

class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass
 
 
def service_shutdown(signum, frame):
    print('Caught signal %d' % signum)
    raise ServiceExit