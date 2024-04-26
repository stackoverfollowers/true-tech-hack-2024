from aiogram_dialog import DialogManager, ShowMode, StartMode

from tth.bot.dialogs.admins.states import MainMenuSG as AdminMainMenuSG
from tth.bot.dialogs.regulars.states import MainMenuSG as RegularMainMenuSG
from tth.common.telegram.models import TelegramUserModel


async def start_new_dialog(dialog_manager: DialogManager) -> None:
    user: TelegramUserModel = dialog_manager.middleware_data["user"]
    if user.is_admin:
        await dialog_manager.start(
            state=AdminMainMenuSG.menu,
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.SEND,
        )
    elif user.is_regular:
        await dialog_manager.start(
            state=RegularMainMenuSG.menu,
        )
    else:
        raise Exception("Unknown user type")
