import threading
from rich.align import Align
from rich.text import Text
from textual import events
from textual.app import App
from textual.reactive import Reactive
from rich.panel import Panel
from rich.pretty import Pretty
from rich.status import Status
from textual.widgets import (
    ScrollView,
    Footer,
    Header,
    Placeholder,
    TreeClick,
    TreeControl,
)
from textual.widget import Widget
from datetime import datetime, timedelta
from textual_app.get_log_task import GetLogTask
from textual_app.status_bar import StatusBar


async def get_lambdas(filename: str, tree: TreeControl) -> None:
    with open(filename, "rt") as fh:
        lines = fh.readlines()
        for line in lines:
            line = line.replace("\n", "")
            split_line = line.split(" ")
            region = split_line[-1] if len(split_line) == 2 else None
            full_name = split_line[0]
            line_name = full_name.split("/")[-1]
            await tree.add(
                tree.root.id,
                line_name,
                {"group_name": full_name, "group_region": region},
            )
    await tree.root.expand()


class RichWatchApp(App):
    main_body = Reactive(Panel(Align.center("Logs Content"), style="bold"))
    a = True

    async def watch_main_body(self, _):
        await self.scrollview.update(Panel(self.main_body))

    async def action_scroll_down(self):
        self.scrollview.scroll_down()

    async def action_scroll_up(self):
        self.scrollview.scroll_up()

    async def action_redownload(self):
        self.status_view.reset_timer()
        self.thread_trigger.set()

    async def action_auto_refresh(self):
        self.status_view.toggle_auto_refresh()

    async def action_custom_quit(self):
        self.log_thread.end()
        self.quit()

    async def action_hide_bars(self):
        # self.view.toggle("tree_bar")
        # self.view.toggle("status_bar")

        self.a = not self.a
        # await self.animator.animate(
        #     self.status_view, "layout_offset_x", 0 if self.a else 30)

    async def on_load(self, event: events.Load) -> None:
        await self.bind("b", "hide_bars()", "Toggle sidebar")
        await self.bind("j", "scroll_up()", "Go down")
        await self.bind("k", "scroll_down()", "Go up")
        await self.bind("r", "redownload()", "Redownload logs")
        await self.bind("a", "auto_refresh()", "Auto Refresh")
        await self.bind("q", "custom_quit()", "Quit")

    async def on_mount(self, event: events.Mount) -> None:
        self.thread_trigger = threading.Event()
        self.log_thread = GetLogTask(self, self.thread_trigger)

        # ----------- LAYOUT -----------
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")

        self.tree = TreeControl("List of Logs Groups", data={})

        self.scrollview = ScrollView(self.main_body)

        self.status_view = StatusBar(self.thread_trigger)
        await self.view.dock(
            ScrollView(self.tree), edge="left", size=30, name="tree_bar"
        )
        await self.view.dock(self.status_view, edge="right", size=30, name="status_bar")
        await self.view.dock(self.scrollview, name="mainbar")

        # --------- OTHER -----------
        await get_lambdas("log_groups.txt", self.tree)

        self.log_thread.start()

    async def handle_tree_click(self, message: TreeClick[dict]) -> None:
        region = message.node.data.get("group_region", None)
        action = message.node.data.get("group_name", None)
        if action is not None and not self.thread_trigger.is_set():
            self.log_thread.set_log_group_region(region)
            self.log_thread.set_log_group_name(action)
            self.status_view.reset_timer()
            self.thread_trigger.set()
