"""
WebSocket implementation for real-time communication.
"""

import asyncio
import json
from typing import Dict, List, Set, Any, Optional
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.websockets import WebSocketState

from ..utils.logger import get_logger
from ..utils.exceptions import WebSocketException

logger = get_logger(__name__)


class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        """Initialize connection manager."""
        self.active_connections: Dict[str, WebSocket] = {}
        self.connection_metadata: Dict[str, Dict[str, Any]] = {}
        self.subscriptions: Dict[str, Set[str]] = {}  # topic -> set of connection_ids
        self.user_connections: Dict[str, Set[str]] = {}  # user_id -> set of connection_ids
        
    async def connect(self, websocket: WebSocket, connection_id: str, user_id: Optional[str] = None) -> None:
        """Accept and register a new WebSocket connection."""
        try:
            await websocket.accept()
            
            self.active_connections[connection_id] = websocket
            self.connection_metadata[connection_id] = {
                "user_id": user_id,
                "connected_at": datetime.utcnow(),
                "last_ping": datetime.utcnow(),
                "subscriptions": set()
            }
            
            if user_id:
                if user_id not in self.user_connections:
                    self.user_connections[user_id] = set()
                self.user_connections[user_id].add(connection_id)
            
            logger.info(f"WebSocket connection established: {connection_id}")
            
            # Send welcome message
            await self.send_personal_message({
                "type": "connection_established",
                "connection_id": connection_id,
                "timestamp": datetime.utcnow().isoformat(),
                "message": "Connected to Nivora AI WebSocket"
            }, connection_id)
            
        except Exception as e:
            logger.error(f"Failed to establish WebSocket connection {connection_id}: {e}")
            raise WebSocketException(f"Connection failed: {e}")
    
    async def disconnect(self, connection_id: str) -> None:
        """Disconnect and cleanup a WebSocket connection."""
        try:
            # Remove from active connections
            if connection_id in self.active_connections:
                del self.active_connections[connection_id]
            
            # Cleanup metadata
            metadata = self.connection_metadata.get(connection_id, {})
            user_id = metadata.get("user_id")
            
            if connection_id in self.connection_metadata:
                del self.connection_metadata[connection_id]
            
            # Cleanup user connections
            if user_id and user_id in self.user_connections:
                self.user_connections[user_id].discard(connection_id)
                if not self.user_connections[user_id]:
                    del self.user_connections[user_id]
            
            # Cleanup subscriptions
            for topic, connections in self.subscriptions.items():
                connections.discard(connection_id)
            
            # Remove empty subscription topics
            self.subscriptions = {
                topic: connections for topic, connections in self.subscriptions.items()
                if connections
            }
            
            logger.info(f"WebSocket connection disconnected: {connection_id}")
            
        except Exception as e:
            logger.error(f"Error during WebSocket disconnect {connection_id}: {e}")
    
    async def send_personal_message(self, message: Dict[str, Any], connection_id: str) -> bool:
        """Send a message to a specific connection."""
        try:
            websocket = self.active_connections.get(connection_id)
            if not websocket:
                logger.warning(f"Connection {connection_id} not found")
                return False
            
            if websocket.client_state == WebSocketState.DISCONNECTED:
                await self.disconnect(connection_id)
                return False
            
            await websocket.send_text(json.dumps(message, default=str))
            return True
            
        except Exception as e:
            logger.error(f"Failed to send message to {connection_id}: {e}")
            await self.disconnect(connection_id)
            return False
    
    async def send_to_user(self, message: Dict[str, Any], user_id: str) -> int:
        """Send a message to all connections of a specific user."""
        sent_count = 0
        user_connections = self.user_connections.get(user_id, set())
        
        for connection_id in list(user_connections):
            if await self.send_personal_message(message, connection_id):
                sent_count += 1
        
        return sent_count
    
    async def broadcast_to_topic(self, message: Dict[str, Any], topic: str) -> int:
        """Broadcast a message to all connections subscribed to a topic."""
        sent_count = 0
        topic_connections = self.subscriptions.get(topic, set())
        
        for connection_id in list(topic_connections):
            if await self.send_personal_message(message, connection_id):
                sent_count += 1
        
        return sent_count
    
    async def broadcast_to_all(self, message: Dict[str, Any]) -> int:
        """Broadcast a message to all active connections."""
        sent_count = 0
        
        for connection_id in list(self.active_connections.keys()):
            if await self.send_personal_message(message, connection_id):
                sent_count += 1
        
        return sent_count
    
    async def subscribe(self, connection_id: str, topic: str) -> bool:
        """Subscribe a connection to a topic."""
        try:
            if connection_id not in self.active_connections:
                return False
            
            if topic not in self.subscriptions:
                self.subscriptions[topic] = set()
            
            self.subscriptions[topic].add(connection_id)
            
            # Update connection metadata
            if connection_id in self.connection_metadata:
                self.connection_metadata[connection_id]["subscriptions"].add(topic)
            
            logger.info(f"Connection {connection_id} subscribed to topic: {topic}")
            
            # Send confirmation
            await self.send_personal_message({
                "type": "subscription_confirmed",
                "topic": topic,
                "timestamp": datetime.utcnow().isoformat()
            }, connection_id)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to subscribe {connection_id} to {topic}: {e}")
            return False
    
    async def unsubscribe(self, connection_id: str, topic: str) -> bool:
        """Unsubscribe a connection from a topic."""
        try:
            if topic in self.subscriptions:
                self.subscriptions[topic].discard(connection_id)
                
                # Remove empty topics
                if not self.subscriptions[topic]:
                    del self.subscriptions[topic]
            
            # Update connection metadata
            if connection_id in self.connection_metadata:
                self.connection_metadata[connection_id]["subscriptions"].discard(topic)
            
            logger.info(f"Connection {connection_id} unsubscribed from topic: {topic}")
            
            # Send confirmation
            await self.send_personal_message({
                "type": "unsubscription_confirmed",
                "topic": topic,
                "timestamp": datetime.utcnow().isoformat()
            }, connection_id)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to unsubscribe {connection_id} from {topic}: {e}")
            return False
    
    async def ping_connections(self) -> None:
        """Send ping to all active connections to keep them alive."""
        ping_message = {
            "type": "ping",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        disconnected_connections = []
        
        for connection_id, websocket in self.active_connections.items():
            try:
                if websocket.client_state == WebSocketState.DISCONNECTED:
                    disconnected_connections.append(connection_id)
                    continue
                
                await websocket.send_text(json.dumps(ping_message, default=str))
                
                # Update last ping time
                if connection_id in self.connection_metadata:
                    self.connection_metadata[connection_id]["last_ping"] = datetime.utcnow()
                
            except Exception as e:
                logger.warning(f"Ping failed for connection {connection_id}: {e}")
                disconnected_connections.append(connection_id)
        
        # Cleanup disconnected connections
        for connection_id in disconnected_connections:
            await self.disconnect(connection_id)
    
    async def disconnect_all(self) -> None:
        """Disconnect all active connections."""
        connection_ids = list(self.active_connections.keys())
        
        for connection_id in connection_ids:
            try:
                websocket = self.active_connections[connection_id]
                await websocket.close()
            except Exception as e:
                logger.error(f"Error closing connection {connection_id}: {e}")
            
            await self.disconnect(connection_id)
        
        logger.info("All WebSocket connections disconnected")
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics."""
        now = datetime.utcnow()
        
        stats = {
            "total_connections": len(self.active_connections),
            "unique_users": len(self.user_connections),
            "total_subscriptions": sum(len(connections) for connections in self.subscriptions.values()),
            "topics": list(self.subscriptions.keys()),
            "connections": []
        }
        
        for connection_id, metadata in self.connection_metadata.items():
            connected_duration = (now - metadata["connected_at"]).total_seconds()
            last_ping_ago = (now - metadata["last_ping"]).total_seconds()
            
            stats["connections"].append({
                "connection_id": connection_id,
                "user_id": metadata["user_id"],
                "connected_duration": connected_duration,
                "last_ping_ago": last_ping_ago,
                "subscriptions": list(metadata["subscriptions"])
            })
        
        return stats


# Global connection manager instance
websocket_manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket):
    """Main WebSocket endpoint handler."""
    import uuid
    
    connection_id = str(uuid.uuid4())
    user_id = None
    
    try:
        # Connect
        await websocket_manager.connect(websocket, connection_id)
        
        # Start ping task for this connection
        ping_task = asyncio.create_task(periodic_ping())
        
        # Message handling loop
        while True:
            try:
                # Receive message
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Handle different message types
                await handle_websocket_message(message, connection_id, websocket)
                
            except WebSocketDisconnect:
                logger.info(f"WebSocket client disconnected: {connection_id}")
                break
            except json.JSONDecodeError:
                await websocket_manager.send_personal_message({
                    "type": "error",
                    "message": "Invalid JSON format",
                    "timestamp": datetime.utcnow().isoformat()
                }, connection_id)
            except Exception as e:
                logger.error(f"WebSocket message handling error: {e}")
                await websocket_manager.send_personal_message({
                    "type": "error",
                    "message": "Message processing failed",
                    "timestamp": datetime.utcnow().isoformat()
                }, connection_id)
    
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
    
    finally:
        # Cleanup
        if ping_task:
            ping_task.cancel()
        await websocket_manager.disconnect(connection_id)


async def handle_websocket_message(message: Dict[str, Any], connection_id: str, websocket: WebSocket) -> None:
    """Handle incoming WebSocket messages."""
    try:
        message_type = message.get("type")
        
        if message_type == "authenticate":
            await handle_authentication(message, connection_id)
        elif message_type == "subscribe":
            await handle_subscription(message, connection_id)
        elif message_type == "unsubscribe":
            await handle_unsubscription(message, connection_id)
        elif message_type == "agent_status":
            await handle_agent_status_request(message, connection_id)
        elif message_type == "deployment_status":
            await handle_deployment_status_request(message, connection_id)
        elif message_type == "pong":
            # Client responded to ping
            await handle_pong(message, connection_id)
        else:
            await websocket_manager.send_personal_message({
                "type": "error",
                "message": f"Unknown message type: {message_type}",
                "timestamp": datetime.utcnow().isoformat()
            }, connection_id)
    
    except Exception as e:
        logger.error(f"Error handling WebSocket message: {e}")
        await websocket_manager.send_personal_message({
            "type": "error",
            "message": "Failed to process message",
            "timestamp": datetime.utcnow().isoformat()
        }, connection_id)


async def handle_authentication(message: Dict[str, Any], connection_id: str) -> None:
    """Handle authentication message."""
    try:
        api_key = message.get("api_key")
        user_id = message.get("user_id")
        
        # In production, validate API key
        # For now, accept any non-empty key
        if api_key:
            # Update connection metadata with user_id
            if connection_id in websocket_manager.connection_metadata:
                websocket_manager.connection_metadata[connection_id]["user_id"] = user_id
            
            # Add to user connections
            if user_id:
                if user_id not in websocket_manager.user_connections:
                    websocket_manager.user_connections[user_id] = set()
                websocket_manager.user_connections[user_id].add(connection_id)
            
            await websocket_manager.send_personal_message({
                "type": "authentication_success",
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }, connection_id)
        else:
            await websocket_manager.send_personal_message({
                "type": "authentication_failed",
                "message": "Invalid or missing API key",
                "timestamp": datetime.utcnow().isoformat()
            }, connection_id)
    
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        await websocket_manager.send_personal_message({
            "type": "authentication_failed",
            "message": "Authentication processing failed",
            "timestamp": datetime.utcnow().isoformat()
        }, connection_id)


async def handle_subscription(message: Dict[str, Any], connection_id: str) -> None:
    """Handle subscription message."""
    try:
        topic = message.get("topic")
        
        if not topic:
            await websocket_manager.send_personal_message({
                "type": "error",
                "message": "Topic is required for subscription",
                "timestamp": datetime.utcnow().isoformat()
            }, connection_id)
            return
        
        # Validate topic format
        valid_topics = [
            "agent_updates",
            "deployment_updates", 
            "monitoring_alerts",
            "cross_chain_events",
            "payment_notifications",
            "system_notifications"
        ]
        
        # Allow agent-specific and deployment-specific topics
        if not (topic in valid_topics or 
                topic.startswith("agent:") or 
                topic.startswith("deployment:") or
                topic.startswith("user:")):
            await websocket_manager.send_personal_message({
                "type": "error",
                "message": f"Invalid topic: {topic}",
                "timestamp": datetime.utcnow().isoformat()
            }, connection_id)
            return
        
        success = await websocket_manager.subscribe(connection_id, topic)
        
        if not success:
            await websocket_manager.send_personal_message({
                "type": "error",
                "message": f"Failed to subscribe to topic: {topic}",
                "timestamp": datetime.utcnow().isoformat()
            }, connection_id)
    
    except Exception as e:
        logger.error(f"Subscription error: {e}")
        await websocket_manager.send_personal_message({
            "type": "error",
            "message": "Subscription processing failed",
            "timestamp": datetime.utcnow().isoformat()
        }, connection_id)


async def handle_unsubscription(message: Dict[str, Any], connection_id: str) -> None:
    """Handle unsubscription message."""
    try:
        topic = message.get("topic")
        
        if not topic:
            await websocket_manager.send_personal_message({
                "type": "error",
                "message": "Topic is required for unsubscription",
                "timestamp": datetime.utcnow().isoformat()
            }, connection_id)
            return
        
        success = await websocket_manager.unsubscribe(connection_id, topic)
        
        if not success:
            await websocket_manager.send_personal_message({
                "type": "error",
                "message": f"Failed to unsubscribe from topic: {topic}",
                "timestamp": datetime.utcnow().isoformat()
            }, connection_id)
    
    except Exception as e:
        logger.error(f"Unsubscription error: {e}")
        await websocket_manager.send_personal_message({
            "type": "error",
            "message": "Unsubscription processing failed",
            "timestamp": datetime.utcnow().isoformat()
        }, connection_id)


async def handle_agent_status_request(message: Dict[str, Any], connection_id: str) -> None:
    """Handle agent status request."""
    try:
        agent_id = message.get("agent_id")
        
        if not agent_id:
            await websocket_manager.send_personal_message({
                "type": "error",
                "message": "Agent ID is required",
                "timestamp": datetime.utcnow().isoformat()
            }, connection_id)
            return
        
        # Get agent status from storage
        from .routes.agents import agents_storage
        
        agent = agents_storage.get(agent_id)
        if not agent:
            await websocket_manager.send_personal_message({
                "type": "agent_status_response",
                "agent_id": agent_id,
                "error": "Agent not found",
                "timestamp": datetime.utcnow().isoformat()
            }, connection_id)
            return
        
        status_info = agent.get_status_info()
        await websocket_manager.send_personal_message({
            "type": "agent_status_response",
            "agent_id": agent_id,
            "status": status_info,
            "timestamp": datetime.utcnow().isoformat()
        }, connection_id)
    
    except Exception as e:
        logger.error(f"Agent status request error: {e}")
        await websocket_manager.send_personal_message({
            "type": "error",
            "message": "Failed to get agent status",
            "timestamp": datetime.utcnow().isoformat()
        }, connection_id)


async def handle_deployment_status_request(message: Dict[str, Any], connection_id: str) -> None:
    """Handle deployment status request."""
    try:
        deployment_id = message.get("deployment_id")
        
        if not deployment_id:
            await websocket_manager.send_personal_message({
                "type": "error",
                "message": "Deployment ID is required",
                "timestamp": datetime.utcnow().isoformat()
            }, connection_id)
            return
        
        # In production, get deployment status from deployment manager
        await websocket_manager.send_personal_message({
            "type": "deployment_status_response",
            "deployment_id": deployment_id,
            "status": "active",  # Placeholder
            "timestamp": datetime.utcnow().isoformat()
        }, connection_id)
    
    except Exception as e:
        logger.error(f"Deployment status request error: {e}")
        await websocket_manager.send_personal_message({
            "type": "error",
            "message": "Failed to get deployment status",
            "timestamp": datetime.utcnow().isoformat()
        }, connection_id)


async def handle_pong(message: Dict[str, Any], connection_id: str) -> None:
    """Handle pong response from client."""
    # Update last ping time
    if connection_id in websocket_manager.connection_metadata:
        websocket_manager.connection_metadata[connection_id]["last_ping"] = datetime.utcnow()


async def periodic_ping():
    """Periodic ping task to keep connections alive."""
    while True:
        try:
            await asyncio.sleep(30)  # Ping every 30 seconds
            await websocket_manager.ping_connections()
        except asyncio.CancelledError:
            break
        except Exception as e:
            logger.error(f"Periodic ping error: {e}")


# Utility functions for broadcasting updates
async def broadcast_agent_update(agent_id: str, update_data: Dict[str, Any]) -> None:
    """Broadcast agent update to subscribers."""
    message = {
        "type": "agent_update",
        "agent_id": agent_id,
        "data": update_data,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Broadcast to general agent updates topic
    await websocket_manager.broadcast_to_topic(message, "agent_updates")
    
    # Broadcast to agent-specific topic
    await websocket_manager.broadcast_to_topic(message, f"agent:{agent_id}")


async def broadcast_deployment_update(deployment_id: str, update_data: Dict[str, Any]) -> None:
    """Broadcast deployment update to subscribers."""
    message = {
        "type": "deployment_update",
        "deployment_id": deployment_id,
        "data": update_data,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Broadcast to general deployment updates topic
    await websocket_manager.broadcast_to_topic(message, "deployment_updates")
    
    # Broadcast to deployment-specific topic
    await websocket_manager.broadcast_to_topic(message, f"deployment:{deployment_id}")


async def broadcast_monitoring_alert(alert_data: Dict[str, Any]) -> None:
    """Broadcast monitoring alert to subscribers."""
    message = {
        "type": "monitoring_alert",
        "data": alert_data,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    await websocket_manager.broadcast_to_topic(message, "monitoring_alerts")


async def broadcast_cross_chain_event(event_data: Dict[str, Any]) -> None:
    """Broadcast cross-chain event to subscribers."""
    message = {
        "type": "cross_chain_event",
        "data": event_data,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    await websocket_manager.broadcast_to_topic(message, "cross_chain_events")


async def broadcast_payment_notification(payment_data: Dict[str, Any]) -> None:
    """Broadcast payment notification to subscribers."""
    message = {
        "type": "payment_notification",
        "data": payment_data,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    await websocket_manager.broadcast_to_topic(message, "payment_notifications")


async def send_user_notification(user_id: str, notification_data: Dict[str, Any]) -> None:
    """Send notification to a specific user."""
    message = {
        "type": "user_notification",
        "data": notification_data,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    await websocket_manager.send_to_user(message, user_id)
