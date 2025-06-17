# This is where the magic happens!
# This file is executed on every boot (including wake-boot from deepsleep)
# Created By: Michael Pham

"""
Built for the PySquared FC Board
Version: 2.0.0
Published: Nov 19, 2024
"""

import gc
import os
import random
import time

import digitalio
import microcontroller
from busio import SPI

try:
    from board_definitions import proveskit_rp2040_v4 as board
except ImportError:
    import board

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

boot_time: float = time.time()

rtc = MicrocontrollerManager()

(boot_count := Counter(index=Register.boot_count)).increment()
error_count: Counter = Counter(index=Register.error_count)

logger: Logger = Logger(
    error_counter=error_count,
    colorized=False,
)

logger.info(
    "Booting",
    hardware_version=os.uname().version,
    software_version=__version__,
)

try:
    loiter_time: int = 5
    for i in range(loiter_time):
        logger.info(f"Code Starting in {loiter_time-i} seconds")
        time.sleep(1)

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

    radio = RFM9xManager(
        logger,
        config.radio,
        spi0,
        initialize_pin(logger, board.SPI0_CS0, digitalio.Direction.OUTPUT, True),
        initialize_pin(logger, board.RF1_RST, digitalio.Direction.OUTPUT, True),
    )

    packet_manager = PacketManager(
        logger,
        radio,
        config.radio.license,
        0.2,
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

    cdh = CommandDataHandler(config, logger, radio)

    beacon = Beacon(
        logger,
        config.cubesat_name,
        packet_manager,
        boot_time,
        imu,
        magnetometer,
        radio,
        error_count,
        boot_count,
    )

    def initial_boot():
        watchdog.pet()
        beacon.send()
        watchdog.pet()
        cdh.listen_for_commands()
        watchdog.pet()

    try:
        logger.info(
            "FC Board Stats",
            bytes_remaining=gc.mem_free(),
        )

        initial_boot()

    except Exception as e:
        logger.error("Error in Boot Sequence", e)

    finally:
        pass

    def main():
        radio.send(config.radio.license.encode("utf-8"))

        beacon.send()

        watchdog.pet()

        cdh.listen_for_commands()

        sleep_helper.safe_sleep(config.sleep_duration)

        # TODO(nateinaction): replace me
        # f.state_of_health()

        cdh.listen_for_commands()

        sleep_helper.safe_sleep(config.sleep_duration)

        cdh.listen_for_commands()

        sleep_helper.safe_sleep(config.sleep_duration)

        cdh.listen_for_commands()

        sleep_helper.safe_sleep(config.sleep_duration)

        packet_manager.send(random.choice(config.jokes).encode("utf-8"))

        watchdog.pet()

        cdh.listen_for_commands()

        sleep_helper.safe_sleep(config.sleep_duration)

    # def critical_power_operations():
    #     initial_boot()
    #     watchdog.pet()

    #     sleep_helper.long_hibernate()

    # def minimum_power_operations():
    #     initial_boot()
    #     watchdog.pet()

    #     sleep_helper.short_hibernate()

    ######################### MAIN LOOP ##############################
    try:
        while True:
            # L0 automatic tasks no matter the battery level
            # TODO(nateinaction): reemplement power level check when we have state of health
            # c.check_reboot()

            # if c.power_mode == "critical":
            #     critical_power_operations()

            # elif c.power_mode == "minimum":
            #     minimum_power_operations()

            # elif c.power_mode == "normal":
            #     main()

            # elif c.power_mode == "maximum":
            #     main()

            main()

    except Exception as e:
        logger.critical("Critical in Main Loop", e)
        time.sleep(10)
        microcontroller.on_next_reset(microcontroller.RunMode.NORMAL)
        microcontroller.reset()
    finally:
        logger.info("Going Neutral!")

except Exception as e:
    logger.critical("An exception occured within main.py", e)
