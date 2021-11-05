import threading
from threading import Event
import boto3
from other_tools.other import create_log_table


class GetLogTask(threading.Thread):
    def __init__(self, widget, trigger: Event):
        self.widget = widget
        self.trigger = trigger
        self.log_group_name = None
        self.should_run = True
        super(GetLogTask, self).__init__()

    def run(self):
        while self.should_run:
            if self.trigger.is_set():
                if self.log_group_name is None:
                    self.trigger.clear()
                    continue

                optionals = dict()
                if self.log_group_region is not None:
                    optionals["region_name"] = self.log_group_region

                session = boto3.session.Session(**optionals)
                client = session.client("logs")
                tmp_table = create_log_table(client, self.log_group_name)
                self.widget.main_body = tmp_table
                self.trigger.clear()

    def set_log_group_name(self, group_name: str):
        self.log_group_name = group_name

    def set_log_group_region(self, region: str):
        self.log_group_region = region

    def end(self):
        self.should_run = False
