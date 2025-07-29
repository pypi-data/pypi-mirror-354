from os.path import dirname, join, exists

from analyst_klondike.features.data_context.set_opened_file_action import SetOpenedFileAction
from analyst_klondike.state.app_dispatch import app_dispatch


def set_file_from_argv(argv: list[str]) -> None:
    if len(argv) != 2:
        return

    current_dir = dirname(argv[0])
    fname = _first_existed_file(current_dir, argv[1:])
    if fname is not None:
        fpath = join(current_dir, fname)
        app_dispatch(SetOpenedFileAction(
            opened_file_name=fname,
            opened_file_path=fpath
        ))
    else:
        print(f"File '{fname}' not exists")
        print("Run again with no argument and try open file manually")


def _first_existed_file(curr_dir: str, args: list[str]) -> str | None:
    return next((
        f for f in args if exists(join(curr_dir, f))
    ), None)
