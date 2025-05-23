import asyncio

class QueueManager:
    def __init__(self, limit):
        self.queue = asyncio.Queue()
        self.limit = limit

    async def add(self, job):
        if self.queue.qsize() >= self.limit:
            raise Exception("Server sedang sibuk. Silakan coba lagi nanti.")
        await self.queue.put(job)

    async def process(self):
        while True:
            job = await self.queue.get()
            await job()
            self.queue.task_done()

global_queue = QueueManager(3)
