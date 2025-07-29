from analyst_klondike.features.theme.actions import ChangeThemeAction
from analyst_klondike.state.app_state import AppState
from analyst_klondike.state.base_action import BaseAction


def apply(state: AppState, action: BaseAction) -> AppState:
    if isinstance(action, ChangeThemeAction):
        state.theme = action.theme
        state.is_dark = action.is_dark
        return state
    return state
