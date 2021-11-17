from textual.widget import Widget
from datetime import datetime, timedelta
import threading
from rich.panel import Panel
from rich.align import Align


class StatusBar(Widget):
    delta_time: timedelta = timedelta(seconds=0)
    last_updated: datetime = datetime.now()
    auto_refresh: bool = False

    def __init__(self, trigger: threading.Event) -> None:
        self.trigger = trigger
        super(StatusBar, self).__init__()

    def update_refresh(self) -> None:
        if self.auto_refresh and self.delta_time.total_seconds() > 10:
            self.trigger.set()
            self.reset_timer()
        self.refresh()

    def reset_timer(self) -> None:
        self.last_updated = datetime.now()
        self.delta_time = timedelta(seconds=0)

    def on_mount(self) -> None:
        self.set_interval(0.2, self.update_refresh)

    def toggle_auto_refresh(self) -> None:
        self.auto_refresh = not self.auto_refresh

    def render(self) -> Panel:
        self.delta_time = datetime.now() - self.last_updated
        text = (
            f"[bold]Auto Refresh: "
            f"[{'green' if self.auto_refresh else 'red'}]{self.auto_refresh}[/]\n"
            f"[bold]Last Update:  [cyan]{str(self.delta_time)[:-7]}"
        )
        return Panel(Align.center(text, vertical="middle"))
