

import asyncio
import functools
import wrapt
from compipe.utils.logging import logger

from .engine_pipe_abstract import EngineAbstract
from .engine_pipe_channel import general_channel


def grpc_call_general(channel: str = None):
    """
    Enhanced gRPC call decorator with proper async handling and resource management
    """
    @wrapt.decorator
    def wrapper(wrapped, engine_impl: EngineAbstract, args, kwds):
        """Simplifies the creation of grpc channels and facilitates the marking of grpc command interfaces
        """
        channel_manager = None
        try:
            # Create channel manager
            channel_manager = general_channel(engine=engine_impl, channel=channel)
            
            # Use context manager for proper resource management
            with channel_manager:
                resp = wrapped(**kwds)
                
                # Check the status code if the resp is an instance of GenericResp
                if hasattr(resp, 'status') and resp.status.code != 0:
                    logger.error(f"gRPC call failed: {resp.status.message}")
                    logger.error(f"Call parameters: {kwds}")
                
                return resp
                
        except Exception as e:
            logger.error(f"gRPC call error: {e}")
            logger.error(f"Function: {wrapped.__name__}, Args: {kwds}")
            raise
        finally:
            # Cleanup is handled by the context manager and channel pool
            pass

    return wrapper


def async_grpc_call(channel: str = None):
    """
    Async version of gRPC call decorator for future async operations
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(engine_impl: EngineAbstract, *args, **kwargs):
            channel_manager = general_channel(engine=engine_impl, channel=channel)
            
            try:
                with channel_manager:
                    result = await func(engine_impl, *args, **kwargs)
                    
                    if hasattr(result, 'status') and result.status.code != 0:
                        logger.error(f"Async gRPC call failed: {result.status.message}")
                        logger.error(f"Call parameters: {kwargs}")
                    
                    return result
            finally:
                # Proper async cleanup if needed
                if hasattr(channel_manager, 'aclose'):
                    await channel_manager.aclose()
                    
        return wrapper
    return decorator
