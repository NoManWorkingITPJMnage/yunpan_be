import os
import time

from yunpan.settings import TMP_FILE_PATH


def clear_zip():
    while(True):
        print('per 10 minute clear zip')
        for root, dir, names in os.walk(TMP_FILE_PATH):
            for name in names:
                file_name = os.path.join(root, name)
                file_time = os.stat(file_name).st_ctime
                now_time = time.time()
                if now_time - file_time > 3600:
                    os.remove(file_name)

        time.sleep(3600)

clear_zip()