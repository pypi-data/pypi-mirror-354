import pytest
from unittest.mock import AsyncMock

from disagreement.shard_manager import ShardManager
from disagreement.client import Client


class DummyGateway:
    def __init__(self, *args, **kwargs):
        self.connect = AsyncMock()
        self.close = AsyncMock()


class DummyClient:
    def __init__(self):
        self._http = object()
        self._event_dispatcher = object()
        self.token = "t"
        self.intents = 0
        self.verbose = False


def test_shard_manager_creates_shards(monkeypatch):
    monkeypatch.setattr("disagreement.shard_manager.GatewayClient", DummyGateway)
    client = DummyClient()
    manager = ShardManager(client, shard_count=3)
    assert len(manager.shards) == 0
    manager._create_shards()
    assert len(manager.shards) == 3


@pytest.mark.asyncio
async def test_shard_manager_start_and_close(monkeypatch):
    monkeypatch.setattr("disagreement.shard_manager.GatewayClient", DummyGateway)
    client = DummyClient()
    manager = ShardManager(client, shard_count=2)
    await manager.start()
    for shard in manager.shards:
        shard.gateway.connect.assert_awaited_once()
    await manager.close()
    for shard in manager.shards:
        shard.gateway.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_client_uses_shard_manager(monkeypatch):
    dummy_manager = AsyncMock()
    monkeypatch.setattr("disagreement.client.ShardManager", lambda c, n: dummy_manager)
    c = Client(token="x", shard_count=2)
    monkeypatch.setattr(c, "wait_until_ready", AsyncMock())
    await c.connect()
    dummy_manager.start.assert_awaited_once()
