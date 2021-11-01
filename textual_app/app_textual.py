import threading
from rich.align import Align
from textual import events
from textual.app import App
from textual.reactive import Reactive
from rich.panel import Panel
from rich.status import Status
from textual.widgets import (
    ScrollView,
    Footer,
    Header,
    Placeholder,
    TreeClick,
    TreeControl,
)
from textual_app.get_thread import GetLogTask


async def get_lambdas(filename: str, tree: TreeControl) -> None:
    with open(filename, "rt") as fh:
        lines = fh.readlines()
        for line in lines:
            line = line.replace("\n", "")
            line_name = line.split("/")[-1]
            await tree.add(tree.root.id, line_name, {"group_name": line})
    await tree.root.expand()


class RichCloudApp(App):
    main_body = Reactive(Panel(Align.center("Logs Content"), style="bold"))

    async def watch_main_body(self, _):
        await self.scrollview.update(Panel(self.main_body))

    async def action_scroll_down(self):
        self.scrollview.scroll_down()

    async def action_scroll_up(self):
        self.scrollview.scroll_up()

    async def action_redownload(self):
        self.thread_trigger.set()

    async def on_load(self, event: events.Load) -> None:
        await self.bind("b", "view.toggle('sidebar')", "Toggle sidebar")
        await self.bind("j", "scroll_up()", "Go down")
        await self.bind("k", "scroll_down()", "Go up")
        await self.bind("r", "redownload()", "Redownload logs")
        await self.bind("q", "quit", "Quit")

    async def on_mount(self, event: events.Mount) -> None:

        # ----------- LAYOUT -----------
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")

        self.tree = TreeControl("List of Logs Groups", data={})

        self.scrollview = ScrollView(self.main_body)

        self.status_view = ScrollView(Panel(Status("Test")))
        await self.view.dock(
            ScrollView(self.tree), edge="left", size=30, name="sidebar"
        )
        await self.view.dock(self.status_view, edge="right", size=30, name="anotherbar")
        await self.view.dock(self.scrollview, name="mainbar")

        # --------- OTHER -----------
        await get_lambdas("log_groups.txt", self.tree)

        self.thread_trigger = threading.Event()
        self.log_thread = GetLogTask(self, self.thread_trigger)
        self.log_thread.start()

    async def handle_tree_click(self, message: TreeClick[dict]) -> None:
        action = message.node.data.get("group_name", None)
        if action is not None and not self.thread_trigger.is_set():
            self.log_thread.set_log_group_name(action)
            self.thread_trigger.set()
