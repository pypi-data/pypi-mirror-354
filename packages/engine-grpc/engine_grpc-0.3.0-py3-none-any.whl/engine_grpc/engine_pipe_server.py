import asyncio
import signal
import sys
from concurrent import futures
from typing import Optional, Type
import grpc
from grpc import aio
from ugrpc_pipe import ugrpc_pipe_pb2
from ugrpc_pipe import ugrpc_pipe_pb2_grpc
from compipe.utils.logging import logger


class UGrpcPipeImpl(ugrpc_pipe_pb2_grpc.UGrpcPipeServicer):
    """Enhanced gRPC service implementation with better error handling"""
    
    def CommandParser(self, request, context):
        try:
            logger.debug(f"CommandParser called with payload: {request.payload}")
            
            # Process the request here
            # This is where you would implement your actual command parsing logic
            
            status = ugrpc_pipe_pb2.Status(code=0, message="OK")
            return ugrpc_pipe_pb2.GenericResp(status=status, payload={})
            
        except Exception as e:
            logger.error(f"CommandParser error: {e}")
            status = ugrpc_pipe_pb2.Status(code=1, message=str(e))
            return ugrpc_pipe_pb2.GenericResp(status=status, payload={})


class AsyncUGrpcPipeImpl(ugrpc_pipe_pb2_grpc.UGrpcPipeServicer):
    """Async version of gRPC service implementation"""
    
    async def CommandParser(self, request, context):
        try:
            logger.debug(f"Async CommandParser called with payload: {request.payload}")
            
            # Process the request asynchronously
            # Add your async command parsing logic here
            
            status = ugrpc_pipe_pb2.Status(code=0, message="OK")
            return ugrpc_pipe_pb2.GenericResp(status=status, payload={})
            
        except Exception as e:
            logger.error(f"Async CommandParser error: {e}")
            status = ugrpc_pipe_pb2.Status(code=1, message=str(e))
            return ugrpc_pipe_pb2.GenericResp(status=status, payload={})


def run_grpc_server(
    service_impl: Type = UGrpcPipeImpl, 
    port: int = 50061, 
    max_workers: int = 10,
    use_async: bool = False
) -> None:
    """
    Run gRPC server with enhanced configuration and proper shutdown handling
    
    Args:
        service_impl: Service implementation class
        port: Port to listen on
        max_workers: Maximum number of worker threads
        use_async: Whether to use async server (experimental)
    """
    
    if not issubclass(service_impl, ugrpc_pipe_pb2_grpc.UGrpcPipeServicer):
        raise TypeError(
            f"service_impl must be a subclass of {ugrpc_pipe_pb2_grpc.UGrpcPipeServicer}")

    if use_async:
        return _run_async_server(service_impl, port)
    else:
        return _run_sync_server(service_impl, port, max_workers)


def _run_sync_server(service_impl: Type, port: int, max_workers: int) -> None:
    """Run synchronous gRPC server with proper shutdown handling"""
    
    # Create server with optimized thread pool
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers),
        options=[
            ('grpc.keepalive_time_ms', 30000),
            ('grpc.keepalive_timeout_ms', 5000),
            ('grpc.keepalive_permit_without_calls', True),
            ('grpc.http2.max_pings_without_data', 0),
            ('grpc.http2.min_time_between_pings_ms', 10000),
            ('grpc.http2.min_ping_interval_without_data_ms', 300000)
        ]
    )
    
    # Add service to server
    ugrpc_pipe_pb2_grpc.add_UGrpcPipeServicer_to_server(
        service_impl(), server)
    
    # Add port and start server
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.info(f"gRPC server started on port {port} with {max_workers} workers")
    
    def signal_handler(signum, frame):
        logger.info("Received shutdown signal, stopping server...")
        server.stop(grace=5.0)
        sys.exit(0)
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("Server interrupted by user")
        server.stop(grace=5.0)


async def _run_async_server(service_impl: Type, port: int) -> None:
    """Run asynchronous gRPC server (experimental)"""
    
    server = aio.server(options=[
        ('grpc.keepalive_time_ms', 30000),
        ('grpc.keepalive_timeout_ms', 5000),
        ('grpc.keepalive_permit_without_calls', True),
    ])
    
    ugrpc_pipe_pb2_grpc.add_UGrpcPipeServicer_to_server(service_impl(), server)
    
    listen_addr = f'[::]:{port}'
    server.add_insecure_port(listen_addr)
    
    logger.info(f"Starting async gRPC server on {listen_addr}")
    await server.start()
    
    async def serve():
        try:
            await server.wait_for_termination()
        except KeyboardInterrupt:
            logger.info("Server interrupted by user")
        finally:
            await server.stop(grace=5.0)
    
    await serve()


# Convenience function for running async server
def run_async_grpc_server(service_impl: Type = AsyncUGrpcPipeImpl, port: int = 50061):
    """Run async gRPC server using asyncio.run()"""
    asyncio.run(_run_async_server(service_impl, port))
