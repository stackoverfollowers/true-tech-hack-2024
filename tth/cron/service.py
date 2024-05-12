import logging

from aiomisc.service.cron import CronService

from tth.cron.parser import MtsPlacesParser

log = logging.getLogger(__name__)


class CronDataLoader(CronService):
    __required__ = ("cron_spec",)
    __dependencies__ = ("mts_parser",)

    cron_spec: str
    mts_parser: MtsPlacesParser

    async def callback(self) -> None:
        log.info("Running cron callback")
        await self.mts_parser.parse()
        log.info("Finishing cron callback")

    async def start(self) -> None:
        self.register(self.callback, spec=self.cron_spec)
        log.info("Starting cron service with spec: %s", self.cron_spec)
        await super().start()
