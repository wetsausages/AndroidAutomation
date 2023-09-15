import os
import psutil
import subprocess

class Connection:
    def __init__(self):
        if self._check_adb_device():
            if not self._check_bluestacks() and not self._check_scrcpy():
                print('Starting scrcpy...')
                subprocess.Popen(['wt', '-w', '0', 'scrcpy'])
                self.attached_device = 'Android/scrcpy'
            else: self.attached_device = 'BlueStacks'
        else:
            if self._check_bluestacks():
                try: 
                    os.system('adb connect localhost:5555')
                    print("Bluestacks instance attached to ADB...")
                    self.attached_device = 'BlueStacks'
                except: 
                    print("Unable to attach Bluestacks instance - make sure it's bridge-enabled in settings.")
                    quit()
            else:
                print('No devices found - either connect an Android device with USB debugging enabled or start a Bluestacks instance with ADB connection enabled.')
                quit()

    def _check_adb_device(self):
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        return len(lines) > 1

    def _check_scrcpy(self):
        return self._check_process('scrcpy')
    
    def _check_bluestacks(self):
        return self._check_process('HD-Player')

    def _check_process(self, process_name):
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if process_name in process.info['name']:
                return True
        return False

