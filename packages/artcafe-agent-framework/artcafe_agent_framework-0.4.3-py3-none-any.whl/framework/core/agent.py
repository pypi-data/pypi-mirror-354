"""
ArtCafe Agent - Production-ready agent implementation.

This module provides an agent that uses WebSocket connection with
challenge-response authentication for secure communication.
"""

import asyncio
import json
import logging
import base64
import time
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, Callable, List
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
import websockets
from urllib.parse import urlencode

logger = logging.getLogger(__name__)


class Agent:
    """
    An agent that connects via WebSocket with challenge-response authentication.
    
    Matches the working implementation from artcafe-getting-started.
    
    Example:
        ```python
        agent = Agent(
            agent_id="my-agent",
            private_key_path="path/to/private_key.pem",
            tenant_id="tenant-123"
        )
        
        @agent.on_message("channel.team-updates")
        async def handle_update(subject, payload, envelope):
            print(f"Received on {subject}: {payload}")
            print(f"From: {envelope['source']['agent_id']}")
            
        await agent.run()
        ```
    """
    
    def __init__(
        self,
        agent_id: str,
        private_key_path: str,
        tenant_id: str = None,
        organization_id: str = None,
        api_endpoint: str = None,
        ws_endpoint: str = None,
        websocket_url: str = None,
        log_level: str = "INFO",
        capabilities: List[str] = None,
        metadata: Dict[str, Any] = None
    ):
        """
        Initialize agent with WebSocket connection parameters.
        
        Args:
            agent_id: Unique identifier for the agent
            private_key_path: Path to RSA private key file
            tenant_id: Tenant ID (preferred)
            organization_id: Organization ID (legacy, same as tenant_id)
            api_endpoint: API endpoint (unused, for compatibility)
            ws_endpoint: WebSocket endpoint URL
            websocket_url: WebSocket URL (legacy)
            log_level: Logging level
            capabilities: List of agent capabilities
            metadata: Additional agent metadata
        """
        self.agent_id = agent_id
        # Handle both tenant_id and organization_id for compatibility
        self.organization_id = tenant_id or organization_id
        if not self.organization_id:
            raise ValueError("Either tenant_id or organization_id must be provided")
        
        # Handle both ws_endpoint and websocket_url for compatibility
        self.websocket_url = ws_endpoint or websocket_url or "wss://ws.artcafe.ai"
        
        # Set log level
        if log_level:
            logger.setLevel(getattr(logging, log_level.upper()))
        self.capabilities = capabilities or []
        self.metadata = metadata or {}
        
        # Load private key
        with open(private_key_path, 'rb') as key_file:
            self.private_key = load_pem_private_key(
                key_file.read(),
                password=None
            )
        
        self._message_handlers = {}
        self._subscriptions = set()
        self._running = False
        self._websocket = None
        self._receive_task = None
    
    def on_message(self, channel: str):
        """
        Decorator for registering message handlers.
        
        The handler will receive:
        - subject: The full NATS subject (e.g., "tenant.org-123.channel.updates")
        - payload: The message payload from the envelope
        - envelope: The full message envelope with metadata
        
        Example:
            ```python
            @agent.on_message("channel.updates")
            async def handle_update(subject, payload, envelope):
                print(f"Received: {payload}")
                print(f"Message ID: {envelope['id']}")
                print(f"From agent: {envelope['source']['agent_id']}")
            ```
        """
        def decorator(func: Callable):
            self._message_handlers[channel] = func
            self._subscriptions.add(channel)
            return func
        return decorator
    
    def _sign_challenge(self, challenge: str) -> bytes:
        """Sign a challenge string with the private key."""
        message = challenge.encode('utf-8')
        digest = hashes.Hash(hashes.SHA256())
        digest.update(message)
        digest_bytes = digest.finalize()
        
        signature = self.private_key.sign(
            digest_bytes,
            padding.PKCS1v15(),
            Prehashed(hashes.SHA256())
        )
        
        return signature
    
    async def _connect(self):
        """Establish WebSocket connection with authentication."""
        # Generate a fresh challenge locally
        import uuid
        challenge = str(uuid.uuid4())
        
        # Sign the challenge
        signature = self._sign_challenge(challenge)
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        
        # Connect with auth params in URL
        params = {
            'challenge': challenge,
            'signature': signature_b64,
            'tenant_id': self.organization_id
        }
        ws_url = f"{self.websocket_url}/ws/agent/{self.agent_id}?{urlencode(params)}"
        
        self._websocket = await websockets.connect(ws_url)
        logger.info(f"Agent {self.agent_id} connected to WebSocket")
        
        # Send presence announcement
        await self._send_message({
            'type': 'presence',
            'agent_id': self.agent_id,
            'status': 'online',
            'capabilities': self.capabilities,
            'metadata': self.metadata
        })
        
        # Subscribe to channels
        subjects = []
        for channel in self._subscriptions:
            # Build full NATS subject if needed
            if not channel.startswith('tenant.'):
                subject = f"tenant.{self.organization_id}.{channel}"
            else:
                subject = channel
            subjects.append(subject)
            
        if subjects:
            await self._send_message({
                'type': 'subscribe',
                'subjects': subjects
            })
    
    async def _send_message(self, message: Dict[str, Any]):
        """Send a message through the WebSocket."""
        if self._websocket:
            await self._websocket.send(json.dumps(message))
    
    async def _receive_messages(self):
        """Receive and process messages from WebSocket."""
        try:
            async for message in self._websocket:
                data = json.loads(message)
                
                # Handle different message types
                if data.get('type') == 'message':
                    subject = data.get('subject', '')
                    envelope = data.get('message', {})
                    
                    # Extract payload from envelope
                    payload = envelope.get('payload', {})
                    
                    # Find matching handler
                    for pattern, handler in self._message_handlers.items():
                        # Check if pattern matches the subject
                        if self._subject_matches(subject, pattern):
                            try:
                                # Pass subject, payload, and full envelope to handler
                                if asyncio.iscoroutinefunction(handler):
                                    await handler(subject, payload, envelope)
                                else:
                                    handler(subject, payload, envelope)
                            except Exception as e:
                                logger.error(f"Error in handler for {pattern}: {e}")
                
                elif data.get('type') == 'error':
                    logger.error(f"Received error: {data.get('message')}")
                    
        except websockets.ConnectionClosed:
            logger.info(f"WebSocket connection closed for {self.agent_id}")
        except Exception as e:
            logger.error(f"Error receiving messages: {e}")
                    
    def _subject_matches(self, subject: str, pattern: str) -> bool:
        """Check if a subject matches a subscription pattern."""
        # Add tenant prefix if not present in pattern
        if not pattern.startswith('tenant.'):
            pattern = f"tenant.{self.organization_id}.{pattern}"
            
        # Simple wildcard matching
        if pattern.endswith('.>'):
            # Multi-level wildcard
            prefix = pattern[:-2]
            return subject.startswith(prefix)
        elif '*' in pattern:
            # Single-level wildcard
            pattern_parts = pattern.split('.')
            subject_parts = subject.split('.')
            if len(pattern_parts) != len(subject_parts):
                return False
            for p, s in zip(pattern_parts, subject_parts):
                if p != '*' and p != s:
                    return False
            return True
        else:
            # Exact match
            return subject == pattern
    
    async def connect(self):
        """Connect to the WebSocket server."""
        await self._connect()
    
    async def subscribe(self, channel: str):
        """Subscribe to a channel."""
        # Build full NATS subject if needed
        if not channel.startswith('tenant.'):
            subject = f"tenant.{self.organization_id}.{channel}"
        else:
            subject = channel
            
        self._subscriptions.add(subject)
        await self._send_message({
            'type': 'subscribe',
            'subjects': [subject]  # Use 'subjects' to be explicit about NATS
        })
    
    async def publish(self, channel: str, data: Dict[str, Any], 
                     message_type: str = "message",
                     correlation_id: str = None,
                     reply_to: str = None):
        """
        Publish a message to a channel following NATS ontology.
        
        Args:
            channel: Channel name (can be simple like "channel.broadcast" or full "tenant.x.channel.broadcast")
            data: The payload data to send
            message_type: Type of message (message, event, command, query, response)
            correlation_id: Optional correlation ID for tracking
            reply_to: Optional reply subject for request-reply pattern
        """
        # Build full NATS subject if needed
        if not channel.startswith('tenant.'):
            subject = f"tenant.{self.organization_id}.{channel}"
        else:
            subject = channel
            
        # Build standard message envelope per NATS ontology
        message = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "1.0",
            "tenant_id": self.organization_id,
            "source": {
                "agent_id": self.agent_id,
                "type": "agent"
            },
            "type": message_type,
            "payload": data
        }
        
        # Add optional fields
        if correlation_id:
            message["correlation_id"] = correlation_id
        if reply_to:
            message["reply_to"] = reply_to
            
        # Send via WebSocket
        await self._send_message({
            'type': 'publish',
            'subject': subject,  # Use 'subject' for NATS alignment
            'message': message   # Full envelope
        })
    
    async def start(self):
        """Start processing messages (without connecting)."""
        if not self._websocket:
            raise RuntimeError("Not connected. Call connect() first.")
        
        self._running = True
        await self._receive_messages()
    
    def register_command(self, command: str, handler: Callable):
        """Register a command handler."""
        self._message_handlers[command] = handler
    
    async def run(self, heartbeat_interval: int = 30):
        """
        Run the agent with automatic heartbeat.
        
        Args:
            heartbeat_interval: Seconds between heartbeats (default: 30)
        """
        self._running = True
        
        async def heartbeat_loop():
            """Send periodic heartbeats to maintain connection."""
            while self._running:
                try:
                    if self._websocket and self._websocket.state.name != 'CLOSED':
                        await self._send_message({'type': 'heartbeat'})
                        logger.debug(f"Sent heartbeat for {self.agent_id}")
                    await asyncio.sleep(heartbeat_interval)
                except Exception as e:
                    logger.error(f"Error sending heartbeat: {e}")
        
        try:
            # Connect to WebSocket
            await self._connect()
            
            # Start receiving messages
            self._receive_task = asyncio.create_task(self._receive_messages())
            
            # Start heartbeat
            heartbeat_task = asyncio.create_task(heartbeat_loop())
            
            # Wait for either task to complete
            done, pending = await asyncio.wait(
                [self._receive_task, heartbeat_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel remaining tasks
            for task in pending:
                task.cancel()
            
        except KeyboardInterrupt:
            logger.info(f"Agent {self.agent_id} shutting down...")
        finally:
            await self.stop()
    
    async def stop(self):
        """Stop the agent and clean up resources."""
        self._running = False
        
        # Send offline presence
        if self._websocket:
            try:
                await self._send_message({
                    'type': 'presence',
                    'agent_id': self.agent_id,
                    'status': 'offline'
                })
                await self._websocket.close()
            except:
                pass
        
        # Cancel receive task
        if self._receive_task:
            self._receive_task.cancel()
            try:
                await self._receive_task
            except asyncio.CancelledError:
                pass
        
        logger.info(f"Agent {self.agent_id} stopped")