from .config import Config
from .store import Store


class GlobalContext:
    config: Config
    store: Store

    def __init__(self):
        self.config = Config()
        self.store = Store()
