from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from rich.console import RenderableType
from rich.text import Text

from textual.widgets import TreeControl, TreeNode, TreeClick, NodeID
from textual.reactive import Reactive
from textual.widgets import ScrollView
from textual import events


@dataclass
class LambdaEntry:
    is_dir: bool
    log_name: str
    custom_name: str | None = None
    region: str | None = None
    is_chosen: bool = False


class ProjectTree(TreeControl[LambdaEntry]):
    def __init__(self, path: str, name: str = None) -> None:
        path = "List of Projects"
        data = LambdaEntry(True, "", None, None)
        super().__init__(path, name=name, data=data)
        self.root.tree.guide_style = "black"
        self.last_chosen = None

    has_focus: Reactive[bool] = Reactive(False)

    def get_root(self) -> TreeNode:
        return self.root

    def on_focus(self) -> None:
        self.has_focus = True

    def on_blur(self) -> None:
        self.has_focus = False

    async def watch_hover_node(self, hover_node: NodeID) -> None:
        for node in self.nodes.values():
            node.tree.guide_style = (
                "bold not dim red" if node.id == hover_node else "black"
            )
        self.refresh(layout=True)

    def render_node(self, node: TreeNode[LambdaEntry]) -> RenderableType:
        return self.render_tree_label(
            node,
            node.data.is_dir,
            node.expanded,
            node.is_cursor,
            node.id == self.hover_node,
            self.has_focus,
            node.data.is_chosen,
        )

    @lru_cache(maxsize=1024 * 32)
    def render_tree_label(
        self,
        node: TreeNode[LambdaEntry],
        is_dir: bool,
        expanded: bool,
        is_cursor: bool,
        is_hover: bool,
        has_focus: bool,
        is_chosen: bool,
    ) -> RenderableType:
        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }
        label = Text(node.label) if isinstance(node.label, str) else node.label
        if is_hover:
            label.stylize("underline bold")
        if is_dir:
            label.stylize("red")
            icon = "📂" if expanded else "📁"
        elif is_chosen:
            label.stylize("bright_blue")
            icon = "✔️"
            label.highlight_regex(r"\..*$", "blue")
        else:
            label.stylize("bright_green")
            icon = "❌"
            label.highlight_regex(r"\..*$", "green")

        if label.plain.startswith("."):
            label.stylize("dim")

        if is_cursor and has_focus:
            label.stylize("reverse")

        icon_label = Text(f"{icon} ", no_wrap=True, overflow="ellipsis") + label
        icon_label.apply_meta(meta)
        return icon_label

    async def on_mount(self, event: events.Mount) -> None:
        ...

    async def handle_tree_click(self, message: TreeClick[LambdaEntry]) -> None:
        dir_entry = message.node.data
        if dir_entry.is_dir:
            if not message.node.loaded:
                await message.node.expand()
            else:
                await message.node.toggle()
        else:
            if self.last_chosen is not None:
                self.last_chosen.data.is_chosen = False
            self.last_chosen = message.node
            message.node.data.is_chosen = True


if __name__ == "__main__":
    from textual.app import App

    class TreeApp(App):
        async def on_mount(self, event: events.Mount) -> None:
            await self.view.dock(ScrollView(ProjectTree(".")))

    TreeApp.run(log="textual.log")
