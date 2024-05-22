import winpty
from tkwinterm.winlog_handler import LogThread
import queue
import threading

class WinPtyHandler:
    def __init__(self, log_file=None, initial_command = None, cols=80, rows=24):
        # Initialize winpty
        self.pty_process = winpty.PtyProcess.spawn('cmd.exe')
        self.pty_process.setwinsize(cols=cols, rows=rows)

        self.log_queue = queue.Queue()
        self.log_thread = None
        if log_file:
            self.log_thread = LogThread(self.log_queue, log_file)
            self.log_thread.start()

        self.closed = False

        if initial_command:
            self.send_command(initial_command)
            
    def send_command(self, command):
        self.pty_process.write(command)

    def read_terminal_data(self, data_callback):
         while not self.closed:
            try:
                data = self.pty_process.read()
                if not data:
                    break
                if self.log_thread:
                    self.log_queue.put(data)
                data_callback(data)
            except (OSError, ValueError) as e:
                if self.closed:
                    break
                else:
                    raise e

    def close(self):
        self.closed = True
        if self.log_thread:
            self.log_queue.put(None)  # Signal the logging thread to stop
            self.log_thread.join()
        self.pty_process.close()

    def resize_pty(self, cols, rows):
        self.pty_process.setwinsize(cols=cols, rows=rows)
