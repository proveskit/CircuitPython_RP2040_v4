"""
Built for the PySquared FC Board V4x
Published: May, 2025
"""

import digitalio
from busio import SPI

try:
    from board_definitions import proveskit_rp2040_v4 as board
except ImportError:
    import board

import os

from lib.proveskit_rp2040_v4.register import Register
from lib.pysquared.beacon import Beacon
from lib.pysquared.cdh import CommandDataHandler
from lib.pysquared.config.config import Config
from lib.pysquared.hardware.busio import _spi_init, initialize_i2c_bus
from lib.pysquared.hardware.digitalio import initialize_pin
from lib.pysquared.hardware.imu.manager.lsm6dsox import LSM6DSOXManager
from lib.pysquared.hardware.magnetometer.manager.lis2mdl import LIS2MDLManager
from lib.pysquared.hardware.radio.manager.rfm9x import RFM9xManager
from lib.pysquared.hardware.radio.packetizer.packet_manager import PacketManager
from lib.pysquared.logger import Logger
from lib.pysquared.nvm.counter import Counter
from lib.pysquared.rtc.manager.microcontroller import MicrocontrollerManager
from lib.pysquared.sleep_helper import SleepHelper
from lib.pysquared.watchdog import Watchdog
from version import __version__

rtc = MicrocontrollerManager()

logger: Logger = Logger(
    error_counter=Counter(index=Register.error_count),
    colorized=False,
)

logger.info(
    "Booting",
    hardware_version=os.uname().version,
    software_version=__version__,
)

try:
    watchdog = Watchdog(logger, board.WDT_WDI)
    watchdog.pet()

    logger.debug("Initializing Config")
    config: Config = Config("config.json")

    # TODO(nateinaction): fix spi init
    spi0: SPI = _spi_init(
        logger,
        board.SPI0_SCK,
        board.SPI0_MOSI,
        board.SPI0_MISO,
    )

    spi0_cs0 = initialize_pin(logger, board.SPI0_CS0, digitalio.Direction.OUTPUT, True)
    logger.debug("SPI0 CS0 initialized")
    rf1_rst = initialize_pin(logger, board.RF1_RST, digitalio.Direction.OUTPUT, True)
    logger.debug("RF1 RST initialized")

    radio = RFM9xManager(
        logger,
        config.radio,
        spi0,
        spi0_cs0,
        rf1_rst,
    )

    i2c1 = initialize_i2c_bus(
        logger,
        board.I2C1_SCL,
        board.I2C1_SDA,
        100000,
    )

    magnetometer = LIS2MDLManager(logger, i2c1)

    imu = LSM6DSOXManager(logger, i2c1, 0x6B)

    sleep_helper = SleepHelper(logger, watchdog, config)

    cdh = CommandDataHandler(logger, config, radio)

    packet_manager = PacketManager(
        logger,
        radio,
        config.radio.license,
        0.2,
    )

    beacon = Beacon(
        logger,
        config.cubesat_name,
        packet_manager,
        imu,
        magnetometer,
        radio,
    )
except Exception as e:
    logger.critical("An exception occurred within repl.py", e)
