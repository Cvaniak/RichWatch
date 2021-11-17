import threading
from rich.align import Align
from textual import events
from textual.app import App
from textual.reactive import Reactive
from rich.panel import Panel
from textual.widgets import ScrollView, Footer, Header, TreeClick, TreeControl, TreeNode
from textual_app.get_log_task import GetLogTask
from textual_widgets.status_bar import StatusBar
from textual_widgets.project_tree import ProjectTree, LambdaEntry
import yaml


async def get_lambdas_1(filename: str, tree: TreeControl) -> None:
    with open(filename, "r") as fh:
        dictionary_yaml = yaml.safe_load(fh)
        default_region = dictionary_yaml.get("default_region", None)
        if default_region is not None:
            del dictionary_yaml["region"]

        for p in dictionary_yaml:
            for lambda_ in dictionary_yaml[p]:
                path = lambda_["path"]
                custom_name = lambda_.get("custom_name", path.split("/")[-1])
                region = lambda_.get("region", default_region)
                await tree.add(
                    tree.root.id,
                    custom_name,
                    {"path": path, "region": region},
                )

    await tree.root.expand()


async def get_lambdas(filename: str, node: TreeNode[LambdaEntry]) -> None:
    with open(filename, "r") as fh:
        dictionary_yaml = yaml.safe_load(fh)
        default_region = dictionary_yaml.get("region", None)
        if default_region is not None:
            del dictionary_yaml["region"]

        for project in dictionary_yaml:
            await node.add(project, LambdaEntry(True, "", None, None))
            new_node = node.children[-1]

            for lambda_ in dictionary_yaml[project]:
                log_group_name = lambda_["path"]
                custom_name = lambda_.get("custom-name", log_group_name.split("/")[-1])
                region = lambda_.get("region", default_region)
                await new_node.add(
                    custom_name,
                    LambdaEntry(
                        False,
                        log_group_name,
                        custom_name,
                        region,
                    ),
                )
            new_node.loaded = True
            await new_node.expand()
        node.loaded = True
        await node.expand()


class RichWatchApp(App):
    def __init__(
        self, log_groups_file="log_groups.yaml", thread_class=GetLogTask, **kwargs
    ) -> None:
        self.log_groups_file = log_groups_file
        self.thread_class = thread_class
        super(RichWatchApp, self).__init__(**kwargs)

    main_body = Reactive(Panel(Align.center("Logs Content"), style="bold"))

    async def watch_main_body(self, _) -> None:
        await self.main_view.update(Panel(self.main_body))

    async def action_scroll_down(self) -> None:
        self.main_view.scroll_down()

    async def action_scroll_up(self) -> None:
        self.main_view.scroll_up()

    async def action_redownload(self) -> None:
        self.status_view.reset_timer()
        self.thread_trigger.set()

    async def action_auto_refresh(self) -> None:
        self.status_view.toggle_auto_refresh()

    async def action_custom_quit(self) -> None:
        self.log_thread.end()
        await self.shutdown()

    async def action_hide_bars(self) -> None:
        await self.view.action_toggle("tree_bar")
        await self.view.action_toggle("status_bar")

    async def on_load(self, event: events.Load) -> None:
        await self.bind("b", "hide_bars()", "Toggle sidebar")
        await self.bind("j", "scroll_up()", "Go down")
        await self.bind("k", "scroll_down()", "Go up")
        await self.bind("r", "redownload()", "Redownload logs")
        await self.bind("a", "auto_refresh()", "Auto Refresh")
        await self.bind("q", "custom_quit()", "Quit")

    async def on_mount(self, event: events.Mount) -> None:
        self.thread_trigger = threading.Event()
        self.log_thread = self.thread_class(self, self.thread_trigger)

        # ----------- LAYOUT -----------
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")

        self.tree = ProjectTree("List of Logs Groups", name="my_name")

        self.main_view = ScrollView(self.main_body)

        self.status_view = StatusBar(self.thread_trigger)
        self.tree_view = ScrollView(self.tree)
        await self.view.dock(self.tree_view, edge="left", size=30, name="tree_bar")
        await self.view.dock(self.status_view, edge="right", size=30, name="status_bar")
        await self.view.dock(self.main_view, name="main_bar")

        # --------- OTHER -----------
        await get_lambdas(self.log_groups_file, self.tree.root)

        self.log_thread.start()

    async def handle_tree_click(self, message: TreeClick[LambdaEntry]) -> None:
        region = message.node.data.region
        action = message.node.data.log_name
        if action is not None and not self.thread_trigger.is_set():
            self.log_thread.set_log_group_region(region)
            self.log_thread.set_log_group_name(action)
            self.status_view.reset_timer()
            self.thread_trigger.set()
