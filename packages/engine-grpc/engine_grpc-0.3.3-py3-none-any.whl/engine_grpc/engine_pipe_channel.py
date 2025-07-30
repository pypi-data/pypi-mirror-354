from __future__ import annotations
import os
import asyncio
import atexit
from dataclasses import dataclass
from typing import Dict, Optional
from compipe.utils.singleton import Singleton
from compipe.runtime_env import Environment as env
from compipe.utils.logging import logger
from grpclib.client import Channel
from grpclib.config import Configuration
from ugrpc_pipe import UGrpcPipeStub

from .engine_pipe_abstract import EngineAbstract


class GrpcChannelPool(metaclass=Singleton):
    """Singleton channel pool for efficient connection reuse"""
    _channels: Dict[str, Channel] = {}
    _stubs: Dict[str, UGrpcPipeStub] = {}
    
    def __init__(self):
        atexit.register(self.cleanup_all)
    
    def get_channel(self, host: str, port: int, config: Configuration, loop: asyncio.AbstractEventLoop) -> Channel:
        """Get or create a channel for the given host:port"""
        key = f"{host}:{port}"
        
        if key not in self._channels or self._is_channel_closed(self._channels[key]):
            self._channels[key] = Channel(host=host, port=port, config=config, loop=loop)
            logger.debug(f"Created new gRPC channel: {key}")
        
        return self._channels[key]
    
    def get_stub(self, channel: Channel) -> UGrpcPipeStub:
        """Get or create a stub for the given channel"""
        channel_key = f"{channel._host}:{channel._port}"
        
        if channel_key not in self._stubs or self._is_channel_closed(channel):
            self._stubs[channel_key] = UGrpcPipeStub(channel=channel)
            logger.debug(f"Created new gRPC stub: {channel_key}")
        
        return self._stubs[channel_key]
    
    def _is_channel_closed(self, channel: Channel) -> bool:
        """Check if a channel is closed, handling different grpclib versions"""
        try:
            # In newer versions of grpclib, check if channel is closed
            return hasattr(channel, 'closed') and channel.closed
        except AttributeError:
            # For older versions, assume channel is open if it exists
            return False
    
    async def close_channel(self, host: str, port: int):
        """Close a specific channel"""
        key = f"{host}:{port}"
        if key in self._channels and not self._is_channel_closed(self._channels[key]):
            await self._channels[key].close()
            del self._channels[key]
            if key in self._stubs:
                del self._stubs[key]
            logger.debug(f"Closed gRPC channel: {key}")
    
    def cleanup_all(self):
        """Cleanup all channels (called on exit)"""
        for key, channel in self._channels.items():
            if not self._is_channel_closed(channel):
                try:
                    # Use asyncio.run to handle cleanup in sync context
                    if hasattr(channel, 'close') and callable(channel.close):
                        close_result = channel.close()
                        # Only use asyncio.run if close() returns a coroutine
                        if asyncio.iscoroutine(close_result):
                            asyncio.run(close_result)
                except Exception as e:
                    logger.warning(f"Error closing channel {key}: {e}")
        self._channels.clear()
        self._stubs.clear()
        logger.debug("Cleaned up all gRPC channels")


@dataclass
class GrpcChannelConfig:
    description: str = "message_length = 100*1024*1024"
    channel: str = None
    max_msg_length: int = 104857600

    @classmethod
    def retrieve_grpc_cfg(cls, engine: str) -> GrpcChannelConfig:
        if (grpc_cfg_json := env().get_value_by_path(['grpc', engine], None)) == None:
            grpc_cfg_json = {
                "description": "message_length = 100*1024*1024",
                "max_msg_length": 104857600
            }

        return GrpcChannelConfig(**grpc_cfg_json)


@dataclass
class base_channel(object):
    """Base class for gRPC channel management with proper resource cleanup"""
    
    engine: EngineAbstract
    channel: str = None
    
    def __post_init__(self):
        self.grpc_cfg: GrpcChannelConfig = GrpcChannelConfig.retrieve_grpc_cfg(
            engine=self.engine.engine_platform)
        
        # Determine channel address
        if self.engine.channel is not None:
            self.channel = self.engine.channel
        elif (channel := os.environ.get(f"{self.engine.engine_platform.upper()}_GRPC_CHANNEL", None)) is not None:
            self.channel = channel
        else:
            self.channel = self.grpc_cfg.channel
        
        if ':' not in self.channel:
            raise ValueError(
                'The specified channel content is invalid. Only accept format <ip>:<port> e.g., 127.0.0.1:50051')
        
        # Parse host and port
        self.host, port_str = self.channel.split(':')
        self.port = int(port_str)
        
        # Create configuration
        self.cfg = Configuration(
            http2_stream_window_size=self.grpc_cfg.max_msg_length,
            http2_connection_window_size=self.grpc_cfg.max_msg_length
        )
        
        self.pool = GrpcChannelPool()
        self.grpc_channel: Optional[Channel] = None
        self.stub: Optional[UGrpcPipeStub] = None
    
    def __enter__(self):
        raise NotImplementedError
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Channels are managed by the pool, don't close them here
        # The pool will handle cleanup when appropriate
        pass


class general_channel(base_channel):
    """Channel manager with proper asyncio event loop handling"""
    
    def __post_init__(self):
        # Properly handle event loop creation and management
        self._setup_event_loop()
        super().__post_init__()
    
    def _setup_event_loop(self):
        """Setup event loop with proper error handling"""
        try:
            # Try to get the current event loop
            loop = asyncio.get_running_loop()
            self.engine.event_loop = loop
        except RuntimeError:
            try:
                # If no running loop, try to get the event loop for current thread
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    raise RuntimeError("Event loop is closed")
                self.engine.event_loop = loop
            except RuntimeError:
                # Create a new event loop if none exists or is closed
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                self.engine.event_loop = loop
                logger.debug("Created new event loop for gRPC channel")
    
    def __enter__(self):
        # Get or create channel and stub from pool
        self.grpc_channel = self.pool.get_channel(
            self.host, self.port, self.cfg, self.engine.event_loop
        )
        self.stub = self.pool.get_stub(self.grpc_channel)
        self.engine.stub = self.stub
        
        logger.debug(f"Using gRPC channel: {self.channel}")
        return self
    
    async def aclose(self):
        """Async cleanup method for proper resource management"""
        if self.grpc_channel and not self.grpc_channel.closed:
            await self.pool.close_channel(self.host, self.port)
