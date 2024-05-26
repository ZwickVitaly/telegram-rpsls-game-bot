from aiogram import Dispatcher
from settings import logger


class DispatcherLifespan(Dispatcher):
    def __init__(self, *args, lifespan=None, **kwargs):
        logger.debug("Initializing Dispatcher with lifespan")
        super().__init__(*args, **kwargs)
        self.lifespan = lifespan

    async def start_polling(self, *args, **kwargs) -> None:
        if self.lifespan:
            if isinstance(self.lifespan, type):
                self.lifespan = self.lifespan()
            async with self.lifespan:
                await super().start_polling(*args, **kwargs)
        else:
            logger.debug("No lifespan polling")
            await super().start_polling(*args, **kwargs)