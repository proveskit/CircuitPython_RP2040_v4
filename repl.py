import lib.pysquared.nvm.register as register
from lib.pysquared.config.config import Config
from lib.pysquared.logger import Logger
from lib.pysquared.nvm.counter import Counter
from lib.pysquared.satellite import Satellite

logger: Logger = Logger(
    error_counter=Counter(index=register.ERRORCNT),
    colorized=False,
)
config: Config = Config("config.json")
logger.info("Initializing a cubesat object as `c` in the REPL...")
c: Satellite = Satellite(logger, config)
