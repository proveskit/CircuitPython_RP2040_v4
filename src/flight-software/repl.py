from lib.proveskit_rp2040_v4.register import Register
from lib.pysquared.config.config import Config
from lib.pysquared.logger import Logger
from lib.pysquared.nvm.counter import Counter

logger: Logger = Logger(
    error_counter=Counter(index=Register.error_count),
    colorized=False,
)
config: Config = Config("config.json")
