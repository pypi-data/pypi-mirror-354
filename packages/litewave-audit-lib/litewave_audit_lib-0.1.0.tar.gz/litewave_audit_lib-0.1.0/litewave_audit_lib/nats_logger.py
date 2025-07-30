import json
import uuid
import logging
from datetime import datetime
from typing import Optional, Dict, Any
import threading

from nats.aio.client import Client as NATS
import asyncio
from litewave_audit_lib.base import BaseAuditLogger

logger = logging.getLogger(__name__)

class NATSAuditLogger(BaseAuditLogger):
    """
    Synchronous NATS Audit Logger with persistent connection.

    This logger maintains a persistent connection to NATS and only reconnects
    when necessary. It uses a thread-local connection to ensure thread safety.
    """

    _thread_local = threading.local()

    def __init__(
        self,
        nats_connection_url: str,
        subject: str,
        max_retries: int = 100,
        retry_delay: float = 1.0,
        **kwargs: Any,
    ):
        # Validate essential parameters
        if not nats_connection_url:
            raise ValueError("NATS URL must be provided.")
        if not subject:
            raise ValueError("NATS subject must be provided.")

        # NATS connection options, extended with common settings for robustness
        self._opts = {
            "servers": [nats_connection_url],
            "max_reconnect_attempts": max_retries,
            "reconnect_time_wait": retry_delay,
            "connect_timeout": 2.0,  # Timeout for initial connection attempt
            "ping_interval": 10.0,   # How often to send pings to keep connection alive
            **kwargs,                # Allow additional NATS options
        }
        self.subject = subject
        self._connected = False

    def _get_connection(self):
        """Get or create a thread-local NATS connection."""
        if not hasattr(self._thread_local, 'nc'):
            self._thread_local.nc = None
            self._thread_local.connected = False
            self._thread_local.loop = None
        return self._thread_local.nc, self._thread_local.connected, self._thread_local.loop

    def _set_connection(self, nc, connected, loop=None):
        """Set the thread-local NATS connection."""
        self._thread_local.nc = nc
        self._thread_local.connected = connected
        if loop:
            self._thread_local.loop = loop

    def _ensure_connected(self):
        """
        Internal helper method to ensure the NATS connection is established
        before performing any operations.
        """
        nc, connected, loop = self._get_connection()
        
        # Only attempt to connect if not already connected or if the connection is closed
        if not connected or nc is None or nc.is_closed:
            logger.info(f"Attempting to establish NATS connection to: {self._opts['servers'][0]}")
            try:
                # Create a new event loop for this thread if needed
                if loop is None or loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                
                # Create and connect the NATS client
                nc = NATS()
                loop.run_until_complete(nc.connect(**self._opts))
                self._set_connection(nc, True, loop)
                logger.info(f"Successfully connected to NATS: {self._opts['servers'][0]}")
            except Exception as e:
                self._set_connection(None, False)
                logger.error(f"Failed to connect to NATS server: {e}")
                raise

    def connect(self) -> None:
        """
        Public method to explicitly establish the NATS connection.
        This method is synchronous (blocking).
        """
        self._ensure_connected()

    def log(
        self,
        *,
        who: str,
        resource: str,
        action: str,
        timestamp: Optional[datetime] = None,
        location: Optional[str] = None,
        request_context: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        client: Optional[Dict[str, Any]] = None,
        id: Optional[str] = None,
    ) -> None:
        """
        Publish an audit entry to NATS. This method is synchronous (blocking).
        It ensures a connection before publishing and handles serialization of the log data.

        Args:
            who: The user or system performing the action
            resource: The resource being acted upon
            action: The action being performed
            timestamp: Optional timestamp of the action (defaults to current time)
            location: Optional location information
            request_context: Optional request context information
            context: Optional additional context
            client: Optional client information
            id: Optional ID for the audit log (defaults to a new UUID if not provided)
        """
        # Ensure connection before attempting to publish
        self._ensure_connected()
        nc, _, loop = self._get_connection()

        # Construct the audit log data payload
        data = {
            "id": id or str(uuid.uuid4()),  # Use provided id or generate new UUID
            "who": who,
            "resource": resource,
            "action": action,
            "timestamp": (timestamp or datetime.utcnow()).isoformat(),  # Use current UTC time if not provided
            "location": location,
            "request_context": request_context,
            "context": context,
            "client": client,
        }
        # Filter out None values before JSON serialization for cleaner logs
        payload = json.dumps({k: v for k, v in data.items() if v is not None}).encode('utf-8')

        try:
            # Publish using the event loop
            loop.run_until_complete(nc.publish(self.subject, payload))
            logger.debug(f"Published audit log to '{self.subject}': {data}")
        except Exception as e:
            logger.error(f"Failed to publish audit log to '{self.subject}': {e}")
            # If publish fails, mark connection as disconnected
            self._set_connection(None, False)
            raise RuntimeError(f"Unable to publish audit log: {e}")

    def close(self) -> None:
        """
        Close the NATS connection cleanly. This method is synchronous (blocking).
        """
        nc, connected, loop = self._get_connection()
        # Only attempt to close if a connection exists and is not already closed
        if connected and nc and not nc.is_closed:
            try:
                # Close using the event loop
                loop.run_until_complete(nc.close())
                self._set_connection(None, False)
                logger.info("NATS connection successfully closed.")
            except Exception as e:
                logger.warning(f"Error encountered while closing NATS connection: {e}")
        else:
            logger.info("NATS connection is already closed or was never established.")

    def __enter__(self) -> "NATSAuditLogger":
        """
        Context manager entry point. Automatically connects to NATS.
        """
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc: Optional[Exception],
        tb: Any,
    ) -> None:
        """
        Context manager exit point. Automatically closes the NATS connection.
        """
        self.close()

