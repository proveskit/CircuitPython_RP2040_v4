import board
import digitalio
import microcontroller
from busio import SPI

import lib.pysquared.nvm.register as register
from lib.pysquared.config.config import Config
from lib.pysquared.hardware.busio import _spi_init
from lib.pysquared.hardware.digitalio import initialize_pin
from lib.pysquared.hardware.radio.manager.rfm9x import RFM9xManager
from lib.pysquared.logger import Logger
from lib.pysquared.nvm.counter import Counter
from lib.pysquared.nvm.flag import Flag
from lib.pysquared.repl.radio_test import RadioTest
from lib.pysquared.satellite import Satellite

logger: Logger = Logger(
    error_counter=Counter(index=register.ERRORCNT, datastore=microcontroller.nvm),
    colorized=False,
)
config: Config = Config("config.json")

c: Satellite = Satellite(logger, config)

spi0: SPI = _spi_init(
    logger,
    board.SPI0_SCK,
    board.SPI0_MOSI,
    board.SPI0_MISO,
)

radio = RFM9xManager(
    logger,
    config.radio,
    Flag(index=register.FLAG, bit_index=7, datastore=microcontroller.nvm),
    spi0,
    initialize_pin(logger, board.SPI0_CS0, digitalio.Direction.OUTPUT, True),
    initialize_pin(logger, board.RF1_RST, digitalio.Direction.OUTPUT, True),
)

radio_test = RadioTest(logger, radio)
