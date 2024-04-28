from tth.args import Parser
from tth.common.deps import config_deps as config_common_deps
from tth.rest.deps import config_deps as config_rest_deps


def config_all_deps(parser: Parser) -> None:
    config_common_deps(parser)
    config_rest_deps(parser)
