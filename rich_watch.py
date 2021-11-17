from textual_app.rich_watch_app import RichWatchApp
from textual_app.get_log_task import GetLogTaskTest
import sys

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) > 1 and sys.argv[1] == "dry-run":
        print("DryRun")
        RichWatchApp.run(
            title="RichWatch TUI dry-run",
            thread_class=GetLogTaskTest,
            log_groups_file="dry_run/log_groups.yaml",
        )
    else:
        RichWatchApp.run(title="RichWatch TUI")
