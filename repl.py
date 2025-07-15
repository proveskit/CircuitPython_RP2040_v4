import microcontroller
# ADDED FROM SDCARDSTUFFS
#---------------------------
try:
    from board_definitions import proveskit_rp2040_v4 as board
except ImportError:
    import board

from lib.pysquared.hardware.busio import _spi_init
from lib.pysquared.sdcard.manager import SDCardManager
#---------------------------

import lib.pysquared.nvm.register as register
from lib.pysquared.config.config import Config
from lib.pysquared.logger import Logger
from lib.pysquared.nvm.counter import Counter
from lib.pysquared.satellite import Satellite
from version import __version__

logger: Logger = Logger(
    error_counter=Counter(index=register.ERRORCNT, datastore=microcontroller.nvm),
    colorized=False,
)
config: Config = Config("config.json")
logger.info("Initializing a cubesat object as `c` in the REPL...")
c: Satellite = Satellite(logger, config)


logger.info("Initializing spi0 in the REPL...")
spi0 = _spi_init(
        logger,
        board.SPI0_SCK,
        board.SPI0_MOSI,
        board.SPI0_MISO,
)


logger.info("Initializing sd card object as 'sd' in the REPL...")
sd = SDCardManager(logger, spi0, board.SPI0_CS1, 400000)

logger.set_sd(sd)