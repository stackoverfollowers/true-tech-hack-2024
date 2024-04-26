from aiogram import Router

from tth.bot.commands.ui_commands import register_commands
from tth.bot.dialogs.admins.router import router as admin_dialog_router
from tth.bot.dialogs.regulars.router import router as user_dialog_router


def register_dialogs(root_router: Router) -> None:
    root_router.include_routers(
        admin_dialog_router,
        user_dialog_router,
    )
    register_commands(root_router)
