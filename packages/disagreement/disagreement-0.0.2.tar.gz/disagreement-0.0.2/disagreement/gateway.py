# disagreement/gateway.py

"""
Manages the WebSocket connection to the Discord Gateway.
"""

import asyncio
import traceback
import aiohttp
import json
import zlib
import time
from typing import Optional, TYPE_CHECKING, Any, Dict

from .enums import GatewayOpcode, GatewayIntent
from .errors import GatewayException, DisagreementException, AuthenticationError
from .interactions import Interaction

if TYPE_CHECKING:
    from .client import Client  # For type hinting
    from .event_dispatcher import EventDispatcher
    from .http import HTTPClient
    from .interactions import Interaction  # Added for INTERACTION_CREATE

# ZLIB Decompression constants
ZLIB_SUFFIX = b"\x00\x00\xff\xff"
MAX_DECOMPRESSION_SIZE = 10 * 1024 * 1024  # 10 MiB, adjust as needed


class GatewayClient:
    """
    Handles the Discord Gateway WebSocket connection, heartbeating, and event dispatching.
    """

    def __init__(
        self,
        http_client: "HTTPClient",
        event_dispatcher: "EventDispatcher",
        token: str,
        intents: int,
        client_instance: "Client",  # Pass the main client instance
        verbose: bool = False,
        *,
        shard_id: Optional[int] = None,
        shard_count: Optional[int] = None,
    ):
        self._http: "HTTPClient" = http_client
        self._dispatcher: "EventDispatcher" = event_dispatcher
        self._token: str = token
        self._intents: int = intents
        self._client_instance: "Client" = client_instance  # Store client instance
        self.verbose: bool = verbose
        self._shard_id: Optional[int] = shard_id
        self._shard_count: Optional[int] = shard_count

        self._ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self._loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self._heartbeat_interval: Optional[float] = None
        self._last_sequence: Optional[int] = None
        self._session_id: Optional[str] = None
        self._resume_gateway_url: Optional[str] = None

        self._keep_alive_task: Optional[asyncio.Task] = None
        self._receive_task: Optional[asyncio.Task] = None

        # For zlib decompression
        self._buffer = bytearray()
        self._inflator = zlib.decompressobj()

    async def _decompress_message(
        self, message_bytes: bytes
    ) -> Optional[Dict[str, Any]]:
        """Decompresses a zlib-compressed message from the Gateway."""
        self._buffer.extend(message_bytes)

        if len(message_bytes) < 4 or message_bytes[-4:] != ZLIB_SUFFIX:
            # Message is not complete or not zlib compressed in the expected way
            return None
            # Or handle partial messages if Discord ever sends them fragmented like this,
            # but typically each binary message is a complete zlib stream.

        try:
            decompressed = self._inflator.decompress(self._buffer)
            self._buffer.clear()  # Reset buffer after successful decompression
            return json.loads(decompressed.decode("utf-8"))
        except zlib.error as e:
            print(f"Zlib decompression error: {e}")
            self._buffer.clear()  # Clear buffer on error
            self._inflator = zlib.decompressobj()  # Reset inflator
            return None
        except json.JSONDecodeError as e:
            print(f"JSON decode error after decompression: {e}")
            return None

    async def _send_json(self, payload: Dict[str, Any]):
        if self._ws and not self._ws.closed:
            if self.verbose:
                print(f"GATEWAY SEND: {payload}")
            await self._ws.send_json(payload)
        else:
            print("Gateway send attempted but WebSocket is closed or not available.")
            # raise GatewayException("WebSocket is not connected.")

    async def _heartbeat(self):
        """Sends a heartbeat to the Gateway."""
        payload = {"op": GatewayOpcode.HEARTBEAT, "d": self._last_sequence}
        await self._send_json(payload)
        # print("Sent heartbeat.")

    async def _keep_alive(self):
        """Manages the heartbeating loop."""
        if self._heartbeat_interval is None:
            # This should not happen if HELLO was processed correctly
            print("Error: Heartbeat interval not set. Cannot start keep_alive.")
            return

        try:
            while True:
                await self._heartbeat()
                await asyncio.sleep(
                    self._heartbeat_interval / 1000
                )  # Interval is in ms
        except asyncio.CancelledError:
            print("Keep_alive task cancelled.")
        except Exception as e:
            print(f"Error in keep_alive loop: {e}")
            # Potentially trigger a reconnect here or notify client
            await self._client_instance.close_gateway(code=1000)  # Generic close

    async def _identify(self):
        """Sends the IDENTIFY payload to the Gateway."""
        payload = {
            "op": GatewayOpcode.IDENTIFY,
            "d": {
                "token": self._token,
                "intents": self._intents,
                "properties": {
                    "$os": "python",  # Or platform.system()
                    "$browser": "disagreement",  # Library name
                    "$device": "disagreement",  # Library name
                },
                "compress": True,  # Request zlib compression
            },
        }
        if self._shard_id is not None and self._shard_count is not None:
            payload["d"]["shard"] = [self._shard_id, self._shard_count]
        await self._send_json(payload)
        print("Sent IDENTIFY.")

    async def _resume(self):
        """Sends the RESUME payload to the Gateway."""
        if not self._session_id or self._last_sequence is None:
            print("Cannot RESUME: session_id or last_sequence is missing.")
            await self._identify()  # Fallback to identify
            return

        payload = {
            "op": GatewayOpcode.RESUME,
            "d": {
                "token": self._token,
                "session_id": self._session_id,
                "seq": self._last_sequence,
            },
        }
        await self._send_json(payload)
        print(
            f"Sent RESUME for session {self._session_id} at sequence {self._last_sequence}."
        )

    async def update_presence(
        self,
        status: str,
        activity_name: Optional[str] = None,
        activity_type: int = 0,
        since: int = 0,
        afk: bool = False,
    ):
        """Sends the presence update payload to the Gateway."""
        payload = {
            "op": GatewayOpcode.PRESENCE_UPDATE,
            "d": {
                "since": since,
                "activities": (
                    [
                        {
                            "name": activity_name,
                            "type": activity_type,
                        }
                    ]
                    if activity_name
                    else []
                ),
                "status": status,
                "afk": afk,
            },
        }
        await self._send_json(payload)

    async def _handle_dispatch(self, data: Dict[str, Any]):
        """Handles DISPATCH events (actual Discord events)."""
        event_name = data.get("t")
        sequence_num = data.get("s")
        raw_event_d_payload = data.get(
            "d"
        )  # This is the 'd' field from the gateway event

        if sequence_num is not None:
            self._last_sequence = sequence_num

        if event_name == "READY":  # Special handling for READY
            if not isinstance(raw_event_d_payload, dict):
                print(
                    f"Error: READY event 'd' payload is not a dict or is missing: {raw_event_d_payload}"
                )
                # Consider raising an error or attempting a reconnect
                return
            self._session_id = raw_event_d_payload.get("session_id")
            self._resume_gateway_url = raw_event_d_payload.get("resume_gateway_url")

            app_id_str = "N/A"
            # Store application_id on the client instance
            if (
                "application" in raw_event_d_payload
                and isinstance(raw_event_d_payload["application"], dict)
                and "id" in raw_event_d_payload["application"]
            ):
                app_id_value = raw_event_d_payload["application"]["id"]
                self._client_instance.application_id = (
                    app_id_value  # Snowflake can be str or int
                )
                app_id_str = str(app_id_value)
            else:
                print(
                    f"Warning: Could not find application ID in READY payload. App commands may not work."
                )

            # Parse and store the bot's own user object
            if "user" in raw_event_d_payload and isinstance(
                raw_event_d_payload["user"], dict
            ):
                try:
                    # Assuming Client has a parse_user method that takes user data dict
                    # and returns a User object, also caching it.
                    bot_user_obj = self._client_instance.parse_user(
                        raw_event_d_payload["user"]
                    )
                    self._client_instance.user = bot_user_obj
                    print(
                        f"Gateway READY. Bot User: {bot_user_obj.username}#{bot_user_obj.discriminator}. Session ID: {self._session_id}. App ID: {app_id_str}. Resume URL: {self._resume_gateway_url}"
                    )
                except Exception as e:
                    print(f"Error parsing bot user from READY payload: {e}")
                    print(
                        f"Gateway READY (user parse failed). Session ID: {self._session_id}. App ID: {app_id_str}. Resume URL: {self._resume_gateway_url}"
                    )
            else:
                print(
                    f"Warning: Bot user object not found or invalid in READY payload."
                )
                print(
                    f"Gateway READY (no user). Session ID: {self._session_id}. App ID: {app_id_str}. Resume URL: {self._resume_gateway_url}"
                )

            await self._dispatcher.dispatch(event_name, raw_event_d_payload)
        elif event_name == "INTERACTION_CREATE":
            # print(f"GATEWAY RECV INTERACTION_CREATE: {raw_event_d_payload}")
            if isinstance(raw_event_d_payload, dict):
                interaction = Interaction(
                    data=raw_event_d_payload, client_instance=self._client_instance
                )
                await self._dispatcher.dispatch(
                    "INTERACTION_CREATE", raw_event_d_payload
                )
                # Dispatch to a new client method that will then call AppCommandHandler
                if hasattr(self._client_instance, "process_interaction"):
                    asyncio.create_task(
                        self._client_instance.process_interaction(interaction)
                    )  # type: ignore
                else:
                    print(
                        "Warning: Client instance does not have process_interaction method for INTERACTION_CREATE."
                    )
            else:
                print(
                    f"Error: INTERACTION_CREATE event 'd' payload is not a dict: {raw_event_d_payload}"
                )
        elif event_name == "RESUMED":
            print("Gateway RESUMED successfully.")
            # RESUMED 'd' payload is often an empty object or debug info.
            # Ensure it's a dict for the dispatcher.
            event_data_to_dispatch = (
                raw_event_d_payload if isinstance(raw_event_d_payload, dict) else {}
            )
            await self._dispatcher.dispatch(event_name, event_data_to_dispatch)
        elif event_name:
            # For other events, ensure 'd' is a dict, or pass {} if 'd' is null/missing.
            # Models/parsers in EventDispatcher will need to handle potentially empty dicts.
            event_data_to_dispatch = (
                raw_event_d_payload if isinstance(raw_event_d_payload, dict) else {}
            )
            # print(f"GATEWAY RECV EVENT: {event_name} | DATA: {event_data_to_dispatch}")
            await self._dispatcher.dispatch(event_name, event_data_to_dispatch)
        else:
            print(f"Received dispatch with no event name: {data}")

    async def _process_message(self, msg: aiohttp.WSMessage):
        """Processes a single message from the WebSocket."""
        if msg.type == aiohttp.WSMsgType.TEXT:
            try:
                data = json.loads(msg.data)
            except json.JSONDecodeError:
                print(
                    f"Failed to decode JSON from Gateway: {msg.data[:200]}"
                )  # Log snippet
                return
        elif msg.type == aiohttp.WSMsgType.BINARY:
            decompressed_data = await self._decompress_message(msg.data)
            if decompressed_data is None:
                print("Failed to decompress or decode binary message from Gateway.")
                return
            data = decompressed_data
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print(
                f"WebSocket error: {self._ws.exception() if self._ws else 'Unknown WSError'}"
            )
            raise GatewayException(
                f"WebSocket error: {self._ws.exception() if self._ws else 'Unknown WSError'}"
            )
        elif msg.type == aiohttp.WSMsgType.CLOSED:
            close_code = (
                self._ws.close_code
                if self._ws and hasattr(self._ws, "close_code")
                else "N/A"
            )
            print(f"WebSocket connection closed by server. Code: {close_code}")
            # Raise an exception to signal the closure to the client's main run loop
            raise GatewayException(f"WebSocket closed by server. Code: {close_code}")
        else:
            print(f"Received unhandled WebSocket message type: {msg.type}")
            return

        if self.verbose:
            print(f"GATEWAY RECV: {data}")
        op = data.get("op")
        # 'd' payload (event_data) is handled specifically by each opcode handler below

        if op == GatewayOpcode.DISPATCH:
            await self._handle_dispatch(data)  # _handle_dispatch will extract 'd'
        elif op == GatewayOpcode.HEARTBEAT:  # Server requests a heartbeat
            await self._heartbeat()
        elif op == GatewayOpcode.RECONNECT:  # Server requests a reconnect
            print("Gateway requested RECONNECT. Closing and will attempt to reconnect.")
            await self.close(code=4000)  # Use a non-1000 code to indicate reconnect
        elif op == GatewayOpcode.INVALID_SESSION:
            # The 'd' payload for INVALID_SESSION is a boolean indicating resumability
            can_resume = data.get("d") is True
            print(f"Gateway indicated INVALID_SESSION. Resumable: {can_resume}")
            if not can_resume:
                self._session_id = None  # Clear session_id to force re-identify
                self._last_sequence = None
            # Close and reconnect. The connect logic will decide to resume or identify.
            await self.close(
                code=4000 if can_resume else 4009
            )  # 4009 for non-resumable
        elif op == GatewayOpcode.HELLO:
            hello_d_payload = data.get("d")
            if (
                not isinstance(hello_d_payload, dict)
                or "heartbeat_interval" not in hello_d_payload
            ):
                print(
                    f"Error: HELLO event 'd' payload is invalid or missing heartbeat_interval: {hello_d_payload}"
                )
                await self.close(code=1011)  # Internal error, malformed HELLO
                return
            self._heartbeat_interval = hello_d_payload["heartbeat_interval"]
            print(f"Gateway HELLO. Heartbeat interval: {self._heartbeat_interval}ms.")
            # Start heartbeating
            if self._keep_alive_task:
                self._keep_alive_task.cancel()
            self._keep_alive_task = self._loop.create_task(self._keep_alive())

            # Identify or Resume
            if self._session_id and self._resume_gateway_url:  # Check if we can resume
                print("Attempting to RESUME session.")
                await self._resume()
            else:
                print("Performing initial IDENTIFY.")
                await self._identify()
        elif op == GatewayOpcode.HEARTBEAT_ACK:
            # print("Received heartbeat ACK.")
            pass  # Good, connection is alive
        else:
            print(f"Received unhandled Gateway Opcode: {op} with data: {data}")

    async def _receive_loop(self):
        """Continuously receives and processes messages from the WebSocket."""
        if not self._ws or self._ws.closed:
            print("Receive loop cannot start: WebSocket is not connected or closed.")
            return

        try:
            async for msg in self._ws:
                await self._process_message(msg)
        except asyncio.CancelledError:
            print("Receive_loop task cancelled.")
        except aiohttp.ClientConnectionError as e:
            print(f"ClientConnectionError in receive_loop: {e}. Attempting reconnect.")
            # This might be handled by an outer reconnect loop in the Client class
            await self.close(code=1006)  # Abnormal closure
        except Exception as e:
            print(f"Unexpected error in receive_loop: {e}")
            traceback.print_exc()
            # Consider specific error types for more granular handling
            await self.close(code=1011)  # Internal error
        finally:
            print("Receive_loop ended.")
            # If the loop ends unexpectedly (not due to explicit close),
            # the main client might want to try reconnecting.

    async def connect(self):
        """Connects to the Discord Gateway."""
        if self._ws and not self._ws.closed:
            print("Gateway already connected or connecting.")
            return

        gateway_url = (
            self._resume_gateway_url or (await self._http.get_gateway_bot())["url"]
        )
        if not gateway_url.endswith("?v=10&encoding=json&compress=zlib-stream"):
            gateway_url += "?v=10&encoding=json&compress=zlib-stream"

        print(f"Connecting to Gateway: {gateway_url}")
        try:
            await self._http._ensure_session()  # Ensure the HTTP client's session is active
            assert (
                self._http._session is not None
            ), "HTTPClient session not initialized after ensure_session"
            self._ws = await self._http._session.ws_connect(gateway_url, max_msg_size=0)
            print("Gateway WebSocket connection established.")

            if self._receive_task:
                self._receive_task.cancel()
            self._receive_task = self._loop.create_task(self._receive_loop())

        except aiohttp.ClientConnectorError as e:
            raise GatewayException(
                f"Failed to connect to Gateway (Connector Error): {e}"
            ) from e
        except aiohttp.WSServerHandshakeError as e:
            if e.status == 401:  # Unauthorized during handshake
                raise AuthenticationError(
                    f"Gateway handshake failed (401 Unauthorized): {e.message}. Check your bot token."
                ) from e
            raise GatewayException(
                f"Gateway handshake failed (Status: {e.status}): {e.message}"
            ) from e
        except Exception as e:  # Catch other potential errors during connection
            raise GatewayException(
                f"An unexpected error occurred during Gateway connection: {e}"
            ) from e

    async def close(self, code: int = 1000):
        """Closes the Gateway connection."""
        print(f"Closing Gateway connection with code {code}...")
        if self._keep_alive_task and not self._keep_alive_task.done():
            self._keep_alive_task.cancel()
            try:
                await self._keep_alive_task
            except asyncio.CancelledError:
                pass  # Expected

        if self._receive_task and not self._receive_task.done():
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass  # Expected

        if self._ws and not self._ws.closed:
            await self._ws.close(code=code)
            print("Gateway WebSocket closed.")

        self._ws = None
        # Do not reset session_id, last_sequence, or resume_gateway_url here
        # if the close code indicates a resumable disconnect (e.g. 4000-4009, or server-initiated RECONNECT)
        # The connect logic will decide whether to resume or re-identify.
        # However, if it's a non-resumable close (e.g. Invalid Session non-resumable), clear them.
        if code == 4009:  # Invalid session, not resumable
            print("Clearing session state due to non-resumable invalid session.")
            self._session_id = None
            self._last_sequence = None
            self._resume_gateway_url = None  # This might be re-fetched anyway
