"""FIX 4.4 broker implementation using QuickFIX-Python."""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from .base import BrokerBase, BrokerEvent, OrderRequest, OrderStatus

# Try to import QuickFIX, but handle gracefully if not available
try:
    import quickfix as fix

    QUICKFIX_AVAILABLE = True
except ImportError:
    QUICKFIX_AVAILABLE = False
    fix = None

logger = logging.getLogger(__name__)


class FIXMessageHandler:
    """Handles FIX message processing."""

    def __init__(self, broker: "FIX44Broker"):
        self.broker = broker

    def handle_execution_report(self, message: Any) -> None:
        """Handle execution report messages."""
        if not QUICKFIX_AVAILABLE:
            return

        try:
            # Extract order ID
            cl_ord_id = fix.ClOrdID()
            message.getField(cl_ord_id)
            order_id = cl_ord_id.getValue()

            # Extract symbol
            symbol = fix.Symbol()
            message.getField(symbol)
            symbol_value = symbol.getValue()

            # Extract execution type
            exec_type = fix.ExecType()
            message.getField(exec_type)
            exec_type_value = exec_type.getValue()

            # Extract order status
            ord_status = fix.OrdStatus()
            message.getField(ord_status)
            status_value = ord_status.getValue()

            # Map FIX status to our status
            status_map = {
                fix.OrdStatus_NEW: OrderStatus.NEW,
                fix.OrdStatus_PARTIALLY_FILLED: OrderStatus.PARTIALLY_FILLED,
                fix.OrdStatus_FILLED: OrderStatus.FILLED,
                fix.OrdStatus_CANCELED: OrderStatus.CANCELLED,
                fix.OrdStatus_REJECTED: OrderStatus.REJECTED,
            }

            order_status = status_map.get(status_value, OrderStatus.NEW)

            # Create broker event based on execution type
            event_type_map = {
                fix.ExecType_NEW: "ACK",
                fix.ExecType_PARTIAL_FILL: "FILL",
                fix.ExecType_FILL: "FILL",
                fix.ExecType_CANCELED: "CANCEL",
                fix.ExecType_REJECTED: "REJECT",
            }

            event_type = event_type_map.get(exec_type_value, "ACK")

            # Extract fill details if available
            quantity = None
            price = None

            if exec_type_value in [fix.ExecType_PARTIAL_FILL, fix.ExecType_FILL]:
                try:
                    last_qty = fix.LastQty()
                    message.getField(last_qty)
                    quantity = float(last_qty.getValue())

                    last_px = fix.LastPx()
                    message.getField(last_px)
                    price = float(last_px.getValue())
                except Exception:
                    pass  # Fields may not be present

            # Create and emit broker event
            event = BrokerEvent(
                event_type=event_type,
                order_id=order_id,
                symbol=symbol_value,
                timestamp=datetime.now(),
                quantity=quantity,
                price=price,
                status=order_status,
            )

            # Schedule emission in the async event loop
            asyncio.create_task(self.broker._emit_event(event))

        except Exception as e:
            logger.error(f"Error processing execution report: {e}")


class FIXApplication:
    """QuickFIX application implementation."""

    def __init__(self, broker: "FIX44Broker"):
        self.broker = broker
        self.message_handler = FIXMessageHandler(broker)

    def onCreate(self, sessionID):
        """Called when session is created."""
        logger.info(f"FIX session created: {sessionID}")

    def onLogon(self, sessionID):
        """Called when logon is successful."""
        logger.info(f"FIX session logged on: {sessionID}")
        self.broker._on_logon(sessionID)

    def onLogout(self, sessionID):
        """Called when logout occurs."""
        logger.info(f"FIX session logged out: {sessionID}")
        self.broker._on_logout(sessionID)

    def toAdmin(self, message, sessionID):
        """Called for outgoing admin messages."""
        pass

    def fromAdmin(self, message, sessionID):
        """Called for incoming admin messages."""
        pass

    def toApp(self, message, sessionID):
        """Called for outgoing application messages."""
        logger.debug(f"Sending message: {message}")

    def fromApp(self, message, sessionID):
        """Called for incoming application messages."""
        try:
            msg_type = fix.MsgType()
            message.getHeader().getField(msg_type)

            if msg_type.getValue() == fix.MsgType_ExecutionReport:
                self.message_handler.handle_execution_report(message)
            else:
                logger.debug(f"Received message type: {msg_type.getValue()}")

        except Exception as e:
            logger.error(f"Error processing incoming message: {e}")


class FIX44Broker(BrokerBase):
    """FIX 4.4 broker implementation using QuickFIX-Python.

    This is a skeleton implementation that demonstrates the structure
    for a FIX broker. It handles logon/heartbeat and basic message processing.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the FIX broker.

        Args:
            config: Configuration dictionary containing FIX settings
        """
        super().__init__("FIX44Broker", config)

        if not QUICKFIX_AVAILABLE:
            logger.warning("QuickFIX-Python not available. Install with: pip install quickfix")

        self.session_id: Optional[Any] = None
        self.initiator: Optional[Any] = None
        self.application: Optional[FIXApplication] = None
        self.logged_on = False

        # Ensure config is not None
        config = config or {}

        # Default FIX configuration
        self.fix_config = {
            "SenderCompID": config.get("sender_comp_id", "EOMS"),
            "TargetCompID": config.get("target_comp_id", "BROKER"),
            "SocketConnectHost": config.get("host", "localhost"),
            "SocketConnectPort": config.get("port", "5001"),
            "BeginString": "FIX.4.4",
            "DataDictionary": config.get("data_dictionary", "FIX44.xml"),
            "StartTime": "00:00:00",
            "EndTime": "24:00:00",
            "HeartBtInt": "30",
            "UseDataDictionary": "Y",
            "ReconnectInterval": "5",
        }
        self.fix_config.update(config.get("fix_settings", {}))

    async def connect(self) -> bool:
        """Connect to the FIX server.

        Returns:
            True if connection successful, False otherwise
        """
        if not QUICKFIX_AVAILABLE:
            logger.error("QuickFIX-Python not available")
            return False

        try:
            # Create settings
            settings = fix.SessionSettings()

            # Create session ID
            begin_string = self.fix_config["BeginString"]
            sender_comp_id = self.fix_config["SenderCompID"]
            target_comp_id = self.fix_config["TargetCompID"]

            self.session_id = fix.SessionID(begin_string, sender_comp_id, target_comp_id)

            # Add session settings
            settings.set(self.session_id, fix.Dictionary(self.fix_config))

            # Create application
            self.application = FIXApplication(self)

            # Create store factory and log factory
            store_factory = fix.FileStoreFactory(settings)
            log_factory = fix.FileLogFactory(settings)

            # Create initiator
            self.initiator = fix.SocketInitiator(
                self.application, store_factory, settings, log_factory
            )

            # Start the initiator
            self.initiator.start()

            # Wait for logon (with timeout)
            for _ in range(30):  # Wait up to 30 seconds
                await asyncio.sleep(1)
                if self.logged_on:
                    self.connected = True
                    logger.info("FIX broker connected successfully")
                    return True

            logger.error("FIX broker failed to logon within timeout")
            return False

        except Exception as e:
            logger.error(f"Error connecting to FIX broker: {e}")
            return False

    async def disconnect(self) -> None:
        """Disconnect from the FIX server."""
        try:
            if self.initiator:
                self.initiator.stop()
            self.connected = False
            self.logged_on = False
            logger.info("FIX broker disconnected")
        except Exception as e:
            logger.error(f"Error disconnecting from FIX broker: {e}")

    async def place_order(self, order: OrderRequest) -> bool:
        """Place a new order via FIX.

        Args:
            order: The order request to place

        Returns:
            True if order was sent successfully
        """
        if not self.connected or not QUICKFIX_AVAILABLE:
            return False

        try:
            # Create New Order Single message
            message = fix.Message()
            header = message.getHeader()
            header.setField(fix.MsgType(fix.MsgType_NewOrderSingle))

            # Set required fields
            message.setField(fix.ClOrdID(order.order_id))
            message.setField(fix.Symbol(order.symbol))

            # Map order side
            side_map = {
                order.side.BUY: fix.Side_BUY,
                order.side.SELL: fix.Side_SELL,
            }
            message.setField(fix.Side(side_map[order.side]))

            # Set quantity
            message.setField(fix.OrderQty(order.quantity))

            # Map order type
            type_map = {
                order.order_type.MARKET: fix.OrdType_MARKET,
                order.order_type.LIMIT: fix.OrdType_LIMIT,
            }
            message.setField(fix.OrdType(type_map[order.order_type]))

            # Set price for limit orders
            if order.order_type.LIMIT and order.price:
                message.setField(fix.Price(order.price))

            # Set time in force
            message.setField(fix.TimeInForce(fix.TimeInForce_DAY))

            # Set transaction time
            message.setField(fix.TransactTime())

            # Send the message
            if fix.Session.sendToTarget(message, self.session_id):
                logger.debug(f"Sent order: {order.order_id}")
                return True
            else:
                logger.error(f"Failed to send order: {order.order_id}")
                return False

        except Exception as e:
            logger.error(f"Error placing order: {e}")
            return False

    async def amend_order(self, order_id: str, **kwargs) -> bool:
        """Amend an existing order via FIX.

        Args:
            order_id: ID of the order to amend
            **kwargs: Fields to amend

        Returns:
            True if amendment was sent successfully
        """
        if not self.connected or not QUICKFIX_AVAILABLE:
            return False

        # Order Cancel/Replace Request would be implemented here
        logger.warning("Order amendment not implemented in skeleton")
        return False

    async def cancel_order(self, order_id: str) -> bool:
        """Cancel an existing order via FIX.

        Args:
            order_id: ID of the order to cancel

        Returns:
            True if cancellation was sent successfully
        """
        if not self.connected or not QUICKFIX_AVAILABLE:
            return False

        try:
            # Create Order Cancel Request message
            message = fix.Message()
            header = message.getHeader()
            header.setField(fix.MsgType(fix.MsgType_OrderCancelRequest))

            # Set required fields
            message.setField(fix.OrigClOrdID(order_id))
            message.setField(fix.ClOrdID(f"{order_id}_CANCEL"))

            # These would typically come from order tracking
            # For skeleton, using placeholder values
            message.setField(fix.Symbol("PLACEHOLDER"))
            message.setField(fix.Side(fix.Side_BUY))
            message.setField(fix.TransactTime())

            # Send the message
            if fix.Session.sendToTarget(message, self.session_id):
                logger.debug(f"Sent cancel for order: {order_id}")
                return True
            else:
                logger.error(f"Failed to send cancel for order: {order_id}")
                return False

        except Exception as e:
            logger.error(f"Error cancelling order: {e}")
            return False

    def _on_logon(self, session_id):
        """Called when FIX session logs on."""
        self.logged_on = True
        logger.info("FIX session logged on successfully")

    def _on_logout(self, session_id):
        """Called when FIX session logs out."""
        self.logged_on = False
        logger.info("FIX session logged out")

    def is_logged_on(self) -> bool:
        """Check if FIX session is logged on.

        Returns:
            True if logged on, False otherwise
        """
        return self.logged_on

    @staticmethod
    def is_available() -> bool:
        """Check if QuickFIX-Python is available.

        Returns:
            True if QuickFIX is available, False otherwise
        """
        return QUICKFIX_AVAILABLE
