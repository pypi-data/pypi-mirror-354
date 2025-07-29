from sys import argv
from analyst_klondike.features.data_context.arg_file_load.arg_load import (
    set_file_from_argv
)
from analyst_klondike.ui.runner_app import get_app


if __name__ == "__main__":
    app = get_app()
    set_file_from_argv(argv)
    app.run()
