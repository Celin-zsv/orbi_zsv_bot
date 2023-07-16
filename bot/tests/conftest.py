from unittest.mock import Mock

import pytest
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


@pytest.fixture
async def memory_storage():
    storage = MemoryStorage()
    try:
        yield storage
    finally:
        await storage.close()


@pytest.fixture
async def state(memory_storage):
    return FSMContext(storage=memory_storage, chat=Mock(), user=Mock())
