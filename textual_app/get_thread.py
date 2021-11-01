import sys
import threading
from threading import Event
import boto3
from other_tools.other import create_log_table


class GetLogTask(threading.Thread):
    def __init__(self, widget, trigger: Event):
        self.widget = widget
        self.trigger = trigger
        self.log_group_name = None
        session = boto3.session.Session()
        self.client = session.client("logs")
        super(GetLogTask, self).__init__()

    def run(self):
        while True:
            if self.trigger.is_set():
                if self.log_group_name is None:
                    self.trigger.clear()
                    continue
                tmp_table = create_log_table(self.client, self.log_group_name)
                self.widget.main_body = tmp_table
                self.trigger.clear()

    def set_log_group_name(self, group_name: str):
        self.log_group_name = group_name
