"""User hub for real-time user data from ProjectX Gateway API."""

import asyncio
import logging
import threading
import time
from typing import Any, Callable, Dict, List, Optional, Set

from projectx_sdk.realtime.connection import SignalRConnection

logger = logging.getLogger(__name__)


class UserHub:
    """
    Hub for user-specific real-time data (orders, positions, trades, accounts).

    This hub handles WebSocket connections to receive real-time updates about:
    - Order status changes
    - Position updates  
    - Trade executions
    - Account balance changes
    """

    def __init__(self, client_or_connection, base_hub_url=None, hub_url=None):
        """
        Initialize the user hub connection.

        This constructor supports multiple signatures for flexibility:
        1. UserHub(client, base_hub_url) - legacy construction using client and base URL
        2. UserHub(client, None, hub_url) - construction using client and direct hub URL
        3. UserHub(connection) - construction using a SignalRConnection directly

        Args:
            client_or_connection: Either a ProjectXClient instance or a SignalRConnection
            base_hub_url (str, optional): The base hub URL (for legacy constructor)
            hub_url (str, optional): The complete hub URL (overrides base_hub_url)
        """
        # Initialize instance variables first
        self.__init_instance_vars()

        # Determine if we're using the new or legacy constructor
        if isinstance(client_or_connection, SignalRConnection):
            # New constructor with SignalRConnection
            self._connection = client_or_connection
            self._is_connected = self._connection.is_connected()
            self._owns_connection = False
            
            # CRITICAL: Set up connection callback to trigger subscriptions
            # This is the key to making the new architecture work like raw test
            self._connection._connection_callback = lambda: self._on_connected()
        else:
            # Constructor with client and URL
            self._client = client_or_connection
            self._owns_connection = True

            if hub_url:
                # Direct hub URL provided
                self.hub_url = hub_url
                self.base_hub_url = None
                self.hub_path = None
            elif base_hub_url:
                # Base URL provided, construct hub URL
                self.base_hub_url = base_hub_url
                self.hub_path = "/hubs/user"
                self.hub_url = f"{base_hub_url}{self.hub_path}"
            else:
                raise ValueError(
                    "Either base_hub_url or hub_url is required when using client-based constructor"
                )

            # Initialize connection but don't start yet
            self._connection: Optional[SignalRConnection] = None  # type: ignore
            self._is_connected = False

        # Register handlers if using direct connection
        if not self._owns_connection:
            self._register_handlers()

    def __init_instance_vars(self):
        """Initialize all instance variables."""
        # Track active subscriptions
        self._account_subscribed = False
        self._subscribed_orders: Set[int] = set()
        self._subscribed_positions: Set[int] = set()
        self._subscribed_trades: Set[int] = set()

        # Event callbacks
        self._account_callbacks: List[Callable] = []
        self._order_callbacks: Dict[str, List[Any]] = {}  # account_id -> [callbacks]
        self._position_callbacks: Dict[str, List[Any]] = {}
        self._trade_callbacks: Dict[str, List[Any]] = {}
        
        # Connection state tracking for robust reconnection
        self._connection_state = {
            "connected": False,
            "reconnect_count": 0,
            "manual_reconnect_active": False,
            "last_disconnect_time": None
        }

    def _register_handlers(self):
        """Register event handlers for the user hub."""
        if self._connection:
            # For SignalRConnection wrapper, we need to register on the underlying connection
            if hasattr(self._connection, '_connection') and self._connection._connection:
                logger.debug("Registering event handlers on underlying raw connection (bypassing wrapper)")
                raw_connection = self._connection._connection
                
                # Register data event handlers on raw connection
                raw_connection.on("GatewayUserAccount", self._handle_account_update)
                raw_connection.on("GatewayUserOrder", self._handle_order_update)
                raw_connection.on("GatewayUserPosition", self._handle_position_update)
                raw_connection.on("GatewayUserTrade", self._handle_trade_update)
                
                # Register connection lifecycle handlers on raw connection
                raw_connection.on_open(lambda: self._on_connected())
                raw_connection.on_close(lambda *args: self._on_connection_closed(*args))
                raw_connection.on_error(lambda *args: self._on_connection_error(*args))
                
            else:
                logger.debug("Registering event handlers on direct connection")
                # Register data event handlers directly (legacy mode)
                self._connection.on("GatewayUserAccount", self._handle_account_update)
                self._connection.on("GatewayUserOrder", self._handle_order_update)
                self._connection.on("GatewayUserPosition", self._handle_position_update)
                self._connection.on("GatewayUserTrade", self._handle_trade_update)
                
                # CRITICAL: Also register connection lifecycle handlers for new architecture
                # This is needed when UserHub is created with SignalRConnection directly
                if hasattr(self._connection, 'on_open'):
                    self._connection.on_open(lambda: self._on_connected())
                if hasattr(self._connection, 'on_close'):
                    self._connection.on_close(lambda *args: self._on_connection_closed(*args))
                if hasattr(self._connection, 'on_error'):
                    self._connection.on_error(lambda *args: self._on_connection_error(*args))

    def start(self):
        """
        Start the hub connection.

        This is only needed for legacy mode.

        Returns:
            bool: True if connection started successfully
        """
        if not self._owns_connection:
            logger.warning("Cannot start connection in direct connection mode")
            return True

        if self._is_connected and self._connection_state["connected"]:
            logger.info("Connection already started")
            return True

        try:
            if self._connection is None:
                self._connection = self._build_connection()

            # Event handlers are now registered in _build_connection() like raw test
            # DO NOT call _register_handlers() here

            # Start the connection
            self._connection.start()
            return True

        except Exception as e:
            logger.error(f"Failed to start connection: {str(e)}")
            self._connection_state["connected"] = False
            return False

    def _build_connection(self):
        """
        Build the connection exactly like raw_user_test.py that works.

        Returns:
            The connection object
        """
        if not self._owns_connection:
            return self._connection

        from signalrcore.hub_connection_builder import HubConnectionBuilder

        # Get the current auth token
        token = self._client.auth.get_token()

        # Build URL exactly like raw test - with access_token in query string
        hub_url = f"{self.hub_url}?access_token={token}"

        # Build the connection exactly like raw test
        connection = (
            HubConnectionBuilder()
            .with_url(hub_url, options={
                "skip_negotiation": True,  # Match raw test exactly
                "transport": "websockets",
                "access_token_factory": lambda: self._client.auth.get_token(),  # Match raw test
                "timeout": 30,  # Match raw test
            })
            .with_automatic_reconnect({
                "type": "raw", 
                "keep_alive_interval": 10,
                "reconnect_interval": 2,
                "max_attempts": 0  # Infinite reconnection attempts - match raw test
            })
            .configure_logging(logger.level, handler=logging.StreamHandler())  # Match raw test
            .build()
        )

        # Set up event handlers EXACTLY like raw test - BEFORE starting connection
        # This is critical - handlers must be set before hub.start()
        connection.on("GatewayUserAccount", self._handle_account_update)
        connection.on("GatewayUserOrder", self._handle_order_update)
        connection.on("GatewayUserPosition", self._handle_position_update)
        connection.on("GatewayUserTrade", self._handle_trade_update)

        # Set up connection lifecycle handlers exactly like raw test
        connection.on_open(lambda: self._on_connected())
        connection.on_close(lambda *args: self._on_connection_closed(*args))
        connection.on_error(lambda *args: self._on_connection_error(*args))

        return connection

    def stop(self):
        """
        Stop the hub connection.

        This is only needed for legacy mode.

        Returns:
            bool: True if connection stopped successfully
        """
        if not self._owns_connection:
            logger.warning("Cannot stop connection in direct connection mode")
            return True

        if not self._is_connected or not self._connection:
            logger.info("Connection already stopped or not started")
            return True

        try:
            # Stop manual reconnection attempts
            self._connection_state["manual_reconnect_active"] = False
            self._connection_state["connected"] = False
            
            self._connection.stop()
            self._is_connected = False
            return True

        except Exception as e:
            logger.error(f"Failed to stop connection: {str(e)}")
            return False

    def reconnect_subscriptions(self):
        """Resubscribe to events after connection is established."""
        logger.info(f"🔧 DEBUG: reconnect_subscriptions called")
        logger.info(f"🔧 DEBUG: _account_subscribed={self._account_subscribed}")
        logger.info(f"🔧 DEBUG: _subscribed_orders={self._subscribed_orders}")
        logger.info(f"🔧 DEBUG: _subscribed_positions={self._subscribed_positions}")
        logger.info(f"🔧 DEBUG: _subscribed_trades={self._subscribed_trades}")
        
        # Resubscribe to accounts if previously subscribed
        if self._account_subscribed:
            logger.info(f"🔧 DEBUG: Resubscribing to accounts...")
            self.subscribe_accounts()

        # Resubscribe to orders
        for account_id in self._subscribed_orders:
            logger.info(f"🔧 DEBUG: Resubscribing to orders for account {account_id}...")
            self.subscribe_orders(account_id)

        # Resubscribe to positions
        for account_id in self._subscribed_positions:
            logger.info(f"🔧 DEBUG: Resubscribing to positions for account {account_id}...")
            self.subscribe_positions(account_id)

        # Resubscribe to trades
        for account_id in self._subscribed_trades:
            logger.info(f"🔧 DEBUG: Resubscribing to trades for account {account_id}...")
            self.subscribe_trades(account_id)
            
        logger.info(f"🔧 DEBUG: reconnect_subscriptions completed")

    def _on_connected(self):
        """
        Handle connection established or reconnection events.
        
        This restores all active subscriptions after a connection is established.
        """
        logger.info(f"🔧 DEBUG: _on_connected called! Setting connection flags...")
        self._connection_state["connected"] = True
        self._connection_state["reconnect_count"] += 1
        self._connection_state["manual_reconnect_active"] = False
        self._is_connected = True
        
        attempt_num = self._connection_state["reconnect_count"]
        logger.info(f"🟢 User hub connection established (attempt #{attempt_num}) - restoring subscriptions")
        
        # CRITICAL FIX: Automatically restore subscriptions on connection/reconnection
        # This matches the market hub's superior approach
        try:
            self.reconnect_subscriptions()
            logger.info("✅ Successfully reconnected all user hub subscriptions")
        except Exception as e:
            logger.error(f"❌ Error reconnecting user hub subscriptions: {e}")

    def _on_connection_closed(self, *args):
        """Handle connection closed event with robust manual reconnection."""
        logger.warning(f"User hub connection closed with args: {args}")
        self._connection_state["connected"] = False
        self._is_connected = False
        self._connection_state["last_disconnect_time"] = time.time()
        
        # Start manual reconnection if not already active and we own the connection
        if not self._connection_state["manual_reconnect_active"] and self._owns_connection:
            self._connection_state["manual_reconnect_active"] = True
            threading.Thread(target=self._attempt_manual_reconnection, daemon=True).start()

    def _on_connection_error(self, *args):
        """Handle connection error event with robust manual reconnection."""
        logger.error(f"User hub connection error: {args}")
        self._connection_state["connected"] = False
        self._is_connected = False
        self._connection_state["last_disconnect_time"] = time.time()
        
        # Start manual reconnection if not already active and we own the connection
        if not self._connection_state["manual_reconnect_active"] and self._owns_connection:
            self._connection_state["manual_reconnect_active"] = True
            threading.Thread(target=self._attempt_manual_reconnection, daemon=True).start()

    def _attempt_manual_reconnection(self):
        """Attempt manual reconnection with exponential backoff."""
        reconnect_delay = 5  # Start with 5 second delay
        max_delay = 60  # Max 60 seconds between attempts
        
        while not self._connection_state["connected"] and self._connection_state["manual_reconnect_active"]:
            try:
                logger.info(f"Attempting manual reconnection in {reconnect_delay} seconds...")
                time.sleep(reconnect_delay)
                
                if self._connection_state["connected"]:
                    break  # Connection restored while we were waiting
                
                logger.info("Creating new user hub connection for manual reconnection...")
                
                # Stop the old connection if it exists
                if self._connection:
                    try:
                        self._connection.stop()
                    except:
                        pass
                
                # Create a completely new connection
                self._connection = self._build_connection()
                
                # Register event handlers for the new connection
                self._register_handlers()
                
                # Start the new connection
                self._connection.start()
                
                # Connection success will be handled by _on_connected
                logger.info("Manual reconnection attempt completed")
                break
                
            except Exception as e:
                logger.error(f"Manual reconnection failed: {e}")
                # Exponential backoff
                reconnect_delay = min(reconnect_delay * 1.5, max_delay)
                continue
        
        self._connection_state["manual_reconnect_active"] = False

    def get_connection_status(self) -> Dict[str, Any]:
        """
        Get the current connection status.

        Returns:
            Dict containing connection state information
        """
        return {
            "connected": self._connection_state["connected"],
            "reconnect_count": self._connection_state["reconnect_count"],
            "manual_reconnect_active": self._connection_state["manual_reconnect_active"],
            "last_disconnect_time": self._connection_state["last_disconnect_time"],
            "account_subscribed": self._account_subscribed,
            "subscribed_orders": len(self._subscribed_orders),
            "subscribed_positions": len(self._subscribed_positions),
            "subscribed_trades": len(self._subscribed_trades)
        }

    def subscribe_accounts(self, callback=None):
        """
        Subscribe to account update events.

        Args:
            callback: Optional callback function for account updates.
                The function should accept a single argument (the account data).
        """
        logger.info("🔧 DEBUG: subscribe_accounts calling send method...")
        
        # Mark as subscribed and store callback
        self._account_subscribed = True
        if callback:
            self._account_callbacks.append(callback)

        # Send subscription immediately if connected (like raw test)
        if self._is_connected and self._connection:
            try:
                logger.info("🔧 DEBUG: Sending SubscribeAccounts with args []")
                self.send("SubscribeAccounts", [])
                logger.info("🔧 DEBUG: subscribe_accounts completed successfully")
            except Exception as e:
                logger.error(f"Failed to send SubscribeAccounts: {e}")
        else:
            logger.info("🔧 DEBUG: subscribe_accounts queued - will send when connected")

    def unsubscribe_accounts(self):
        """
        Unsubscribe from account updates.

        Returns:
            self: For method chaining
        """
        if self._is_connected and self._account_subscribed:
            self.send("UnsubscribeAccounts", [])
            self._account_subscribed = False

        return self

    def subscribe_orders(self, account_id, callback=None):
        """
        Subscribe to order updates for a specific account.

        Args:
            account_id (int): Account ID to subscribe to
            callback: Optional callback function for order updates.
                The function should accept two arguments (account_id, order_data).
        """
        logger.info(f"🔧 DEBUG: subscribe_orders calling send method for account {account_id}...")
        
        # Store subscription and callback
        self._subscribed_orders.add(account_id)
        if callback:
            if str(account_id) not in self._order_callbacks:
                self._order_callbacks[str(account_id)] = []
            self._order_callbacks[str(account_id)].append(callback)

        # Send subscription immediately if connected (like raw test)
        if self._is_connected and self._connection:
            try:
                # Ensure account_id is an integer like raw test uses
                if isinstance(account_id, str):
                    account_id = int(account_id)
                logger.info(f"🔧 DEBUG: Sending SubscribeOrders with args [{account_id}] (type: {type(account_id).__name__})")
                self.send("SubscribeOrders", [account_id])
                logger.info(f"🔧 DEBUG: subscribe_orders completed successfully for account {account_id}")
            except Exception as e:
                logger.error(f"Failed to send SubscribeOrders for account {account_id}: {e}")
        else:
            logger.info(f"🔧 DEBUG: subscribe_orders queued for account {account_id} - will send when connected")

    def unsubscribe_orders(self, account_id):
        """
        Unsubscribe from order updates for a specific account.

        Args:
            account_id (int): Account ID to unsubscribe from

        Returns:
            self: For method chaining
        """
        if self._is_connected and account_id in self._subscribed_orders:
            self.send("UnsubscribeOrders", [account_id])
            self._subscribed_orders.discard(account_id)

        return self

    def subscribe_positions(self, account_id, callback=None):
        """
        Subscribe to position updates for a specific account.

        Args:
            account_id (int): Account ID to subscribe to
            callback: Optional callback function for position updates.
                The function should accept two arguments (account_id, position_data).
        """
        # Store subscription and callback
        self._subscribed_positions.add(account_id)
        if callback:
            if str(account_id) not in self._position_callbacks:
                self._position_callbacks[str(account_id)] = []
            self._position_callbacks[str(account_id)].append(callback)

        # Send subscription immediately if connected (like raw test)
        if self._is_connected and self._connection:
            try:
                # Ensure account_id is an integer like raw test uses
                if isinstance(account_id, str):
                    account_id = int(account_id)
                logger.info(f"🔧 DEBUG: Sending SubscribePositions with args [{account_id}] (type: {type(account_id).__name__})")
                self.send("SubscribePositions", [account_id])
            except Exception as e:
                logger.error(f"Failed to send SubscribePositions for account {account_id}: {e}")

    def unsubscribe_positions(self, account_id):
        """
        Unsubscribe from position updates for a specific account.

        Args:
            account_id (int): Account ID to unsubscribe from

        Returns:
            self: For method chaining
        """
        if self._is_connected and account_id in self._subscribed_positions:
            self.send("UnsubscribePositions", [account_id])
            self._subscribed_positions.discard(account_id)

        return self

    def subscribe_trades(self, account_id, callback=None):
        """
        Subscribe to trade updates for a specific account.

        Args:
            account_id (int): Account ID to subscribe to
            callback: Optional callback function for trade updates.
                The function should accept two arguments (account_id, trade_data).
        """
        # Store subscription and callback
        self._subscribed_trades.add(account_id)
        if callback:
            if str(account_id) not in self._trade_callbacks:
                self._trade_callbacks[str(account_id)] = []
            self._trade_callbacks[str(account_id)].append(callback)

        # Send subscription immediately if connected (like raw test)
        if self._is_connected and self._connection:
            try:
                # Ensure account_id is an integer like raw test uses
                if isinstance(account_id, str):
                    account_id = int(account_id)
                logger.info(f"🔧 DEBUG: Sending SubscribeTrades with args [{account_id}] (type: {type(account_id).__name__})")
                self.send("SubscribeTrades", [account_id])
            except Exception as e:
                logger.error(f"Failed to send SubscribeTrades for account {account_id}: {e}")

    def unsubscribe_trades(self, account_id):
        """
        Unsubscribe from trade updates for a specific account.

        Args:
            account_id (int): Account ID to unsubscribe from

        Returns:
            self: For method chaining
        """
        if self._is_connected and account_id in self._subscribed_trades:
            self.send("UnsubscribeTrades", [account_id])
            self._subscribed_trades.discard(account_id)

        return self

    async def invoke(self, method, *args):
        """
        Invoke a hub method.

        Args:
            method (str): Hub method name
            *args: Arguments to pass to the method

        Returns:
            The result of the method invocation
        """
        if not self._is_connected or not self._connection:
            raise Exception("Not connected to hub")

        return await self._connection.invoke(method, *args)

    def send(self, method, args=None):
        """
        Send a hub method call - BYPASS broken SignalRConnection wrapper.
        Use direct HubConnectionBuilder approach that works in raw test.

        Args:
            method (str): Hub method name
            args (list, optional): Arguments to pass to the method as a list

        Returns:
            The result of the method call
        """
        if not self._is_connected or not self._connection:
            logger.error(f"Cannot send {method}: not connected (connected={self._is_connected}, connection={self._connection is not None})")
            raise Exception("Not connected to hub")

        try:
            logger.info(f"🔧 DEBUG: Sending {method} with args {args}")
            
            # CRITICAL FIX: Bypass the broken SignalRConnection wrapper entirely
            # Use the underlying HubConnectionBuilder connection directly like raw test
            if hasattr(self._connection, '_connection') and self._connection._connection:
                # Use the raw HubConnectionBuilder connection directly - this is what works!
                logger.info(f"🔧 DEBUG: Using direct HubConnectionBuilder connection (bypassing wrapper)")
                raw_connection = self._connection._connection
                
                # Important: Check if connection is in a good state before sending
                if not hasattr(raw_connection, 'state') or raw_connection.state != 'Connected':
                    logger.warning(f"🔧 DEBUG: Connection state is not 'Connected': {getattr(raw_connection, 'state', 'Unknown')}")
                
                result = raw_connection.send(method, args or [])
                logger.info(f"🔧 DEBUG: Direct send {method} completed successfully, result: {result}")
                return result
            else:
                # Fallback to wrapper if no direct access (shouldn't happen)
                logger.warning(f"🔧 DEBUG: No direct connection found, falling back to wrapper")
                return self._try_wrapper_send(method, args)
                
        except Exception as e:
            logger.error(f"🔧 DEBUG: Send {method} failed with error: {e}")
            logger.error(f"🔧 DEBUG: Error type: {type(e).__name__}")
            logger.error(f"🔧 DEBUG: Error args: {e.args}")
            # Don't show full traceback as it's usually not helpful for SignalR issues
            raise

    def _try_wrapper_send(self, method, args):
        """Fallback wrapper send method (known to be broken)."""
        # Handle different connection types
        if hasattr(self._connection, 'send'):
            # Legacy connection (like from raw test) - has direct send method
            logger.info(f"🔧 DEBUG: Using legacy connection.send() method")
            result = self._connection.send(method, args or [])
            logger.info(f"🔧 DEBUG: Send {method} completed successfully, result: {result}")
            return result
        elif hasattr(self._connection, 'invoke'):
            # SignalRConnection - has async invoke method, need to call it synchronously
            logger.info(f"🔧 DEBUG: Using SignalRConnection.invoke() method")
            
            # For SignalRConnection, we need to call invoke, but it's async
            # We'll use a different approach - call the underlying connection's send
            if hasattr(self._connection, '_connection') and hasattr(self._connection._connection, 'send'):
                logger.info(f"🔧 DEBUG: Using underlying connection send method")
                result = self._connection._connection.send(method, args or [])
                logger.info(f"🔧 DEBUG: Send {method} completed successfully, result: {result}")
                return result  
            else:
                # Fallback - try to create a simple sync wrapper around async invoke
                logger.info(f"🔧 DEBUG: Using async invoke with sync wrapper")
                import asyncio
                
                # Create a simple sync wrapper
                async def async_send():
                    return await self._connection.invoke(method, *(args or []))
                
                # Try to run in existing event loop or create new one
                try:
                    loop = asyncio.get_event_loop()
                    if loop.is_running():
                        # Already in event loop - this is tricky, but we'll use run_until_complete
                        result = asyncio.create_task(async_send())
                    else:
                        result = loop.run_until_complete(async_send())
                except RuntimeError:
                    # No event loop, create one
                    result = asyncio.run(async_send())
                
                logger.info(f"🔧 DEBUG: Send {method} completed successfully, result: {result}")
                return result
        else:
            raise AttributeError(f"Connection type {type(self._connection)} has no send or invoke method")

    def _handle_account_update(self, *args):
        """
        Handle account updates - EXACTLY like raw test, no account ID extraction.
        """
        try:
            logger.debug(f"Account data received: {args}")
            
            # Process exactly like raw_user_test.py - call callbacks for ALL account callbacks
            for callback in self._account_callbacks:
                try:
                    # Pass raw args directly like raw test
                    callback(*args)
                except Exception as e:
                    logger.error(f"Error in account callback: {e}")
        except Exception as e:
            logger.error(f"Error processing account update: {e}")

    def _handle_order_update(self, *args):
        """
        Handle order updates - EXACTLY like raw test, no account ID extraction.
        """
        try:
            logger.debug(f"Order data received: {args}")
            
            # Process exactly like raw_user_test.py - call callbacks for ALL order callbacks
            for account_id_str, callbacks in self._order_callbacks.items():
                for callback in callbacks:
                    try:
                        # Pass raw args directly like raw test
                        callback(*args)
                    except Exception as e:
                        logger.error(f"Error in order callback for {account_id_str}: {e}")
        except Exception as e:
            logger.error(f"Error processing order update: {e}")

    def _handle_position_update(self, *args):
        """
        Handle position updates - EXACTLY like raw test, no account ID extraction.
        """
        try:
            logger.debug(f"Position data received: {args}")
            
            # Process exactly like raw_user_test.py - call callbacks for ALL position callbacks
            for account_id_str, callbacks in self._position_callbacks.items():
                for callback in callbacks:
                    try:
                        # Pass raw args directly like raw test
                        callback(*args)
                    except Exception as e:
                        logger.error(f"Error in position callback for {account_id_str}: {e}")
        except Exception as e:
            logger.error(f"Error processing position update: {e}")

    def _handle_trade_update(self, *args):
        """
        Handle trade updates - EXACTLY like raw test, no account ID extraction.
        """
        try:
            logger.debug(f"Trade data received: {args}")
            
            # Process exactly like raw_user_test.py - call callbacks for ALL trade callbacks
            for account_id_str, callbacks in self._trade_callbacks.items():
                for callback in callbacks:
                    try:
                        # Pass raw args directly like raw test
                        callback(*args)
                    except Exception as e:
                        logger.error(f"Error in trade callback for {account_id_str}: {e}")
        except Exception as e:
            logger.error(f"Error processing trade update: {e}")
