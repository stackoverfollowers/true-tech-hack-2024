import logging

from aiomisc.service.cron import CronService

from tth.cron.parser import MtsPlacesParser

log = logging.getLogger(__name__)


class CronDataLoader(CronService):
    __dependencies__ = (
        "mts_parser",
    )

    mts_parser: MtsPlacesParser

    async def callback(self) -> None:
        log.info("Running cron callback")
        await self.mts_parser.parse()
        log.info("Finishing cron callback")

    async def start(self) -> None:
        # run the job every 20 minutes
        self.register(self.callback, spec="*/20 * * * *", )
        await super().start()
