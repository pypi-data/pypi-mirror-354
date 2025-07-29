from analyst_klondike.features.data_context.init_action import (
    InitAction,
    init_state)
from analyst_klondike.state.app_state import AppState
from analyst_klondike.state.base_action import BaseAction


def apply(state: AppState, action: BaseAction) -> AppState:
    if isinstance(action, InitAction):
        init_state(state, action.data, action.file_path)
        return state
    return state
