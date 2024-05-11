from aiomisc_dependency import dependency

from tth.args import Parser
from tth.common.events.storage import IEventStorage
from tth.common.places.storage import IPlaceStorage
from tth.cron.parser import MtsPlacesParser


def config_cron_deps(parser: Parser) -> None:
    @dependency
    def mts_parser(
        event_storage: IEventStorage,
        place_storage: IPlaceStorage,
    ) -> MtsPlacesParser:
        return MtsPlacesParser(event_storage, place_storage)
