import os
import mss
from datetime import datetime
import time
def screenshotLop():
    with mss.mss() as sct:
        folder = "screenshots"
        os.makedirs(folder, exist_ok=True)
        try:
            while True: 
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = os.path.join(folder, f"screenshot_{timestamp}.png")	
                sct.shot(output=filename)
                print(f"Saved {filename}")
                time.sleep(1)
        except KeyboardInterrupt:
            print("Screenshot loop stopped by user.")


if __name__ == "__main__":
    screenshotLop()	