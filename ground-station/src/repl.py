import digitalio
from busio import SPI

try:
    from board_definitions import proveskit_rp2040_v4 as board
except ImportError:
    import board

from lib.proveskit_rp2040_v4.register import Register
from lib.pysquared.config.config import Config
from lib.pysquared.hardware.busio import _spi_init
from lib.pysquared.hardware.digitalio import initialize_pin
from lib.pysquared.hardware.radio.manager.rfm9x import RFM9xManager
from lib.pysquared.hardware.radio.packetizer.packet_manager import PacketManager
from lib.pysquared.logger import Logger
from lib.pysquared.nvm.counter import Counter

logger: Logger = Logger(
    error_counter=Counter(index=Register.error_count),
    colorized=False,
)
config: Config = Config("config.json")

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

while True:
    bytes = packet_manager.listen(3)
    if bytes is not None:
        logger.info(f"Received {len(bytes)} bytes: {bytes.hex()}")
