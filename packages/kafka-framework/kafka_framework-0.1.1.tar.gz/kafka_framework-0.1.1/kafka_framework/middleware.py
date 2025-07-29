from typing import Callable, List, TypeVar

from .context import MessageContext

T = TypeVar('T')

MiddlewareFunc = Callable[[MessageContext, T], T]

class MiddlewareManager:
    def __init__(self):
        self._pre_middlewares: List[MiddlewareFunc] = []
        self._post_middlewares: List[MiddlewareFunc] = []
        
    def add_pre_middleware(self, middleware: MiddlewareFunc) -> None:
        """Add a middleware that runs before the handler"""
        self._pre_middlewares.append(middleware)
        
    def add_post_middleware(self, middleware: MiddlewareFunc) -> None:
        """Add a middleware that runs after the handler"""
        self._post_middlewares.append(middleware)
        
    async def process_message(self, ctx: MessageContext, handler: Callable) -> None:
        """Process a message through all middleware and the handler"""
        try:
            # Run pre-processing middlewares
            for middleware in self._pre_middlewares:
                ctx = await middleware(ctx, handler)
            
            # Run the actual handler
            await handler(ctx)
            
            # Run post-processing middlewares
            for middleware in self._post_middlewares:
                ctx = await middleware(ctx, handler)
                
        except Exception as e:
            # logger.error(f"Error in middleware processing: {str(e)}")
            raise
            
    @staticmethod
    def middleware(func: MiddlewareFunc) -> MiddlewareFunc:
        """Decorator to mark a function as middleware"""
        func._is_middleware = True
        return func
        
    @staticmethod
    def pre_middleware(func: MiddlewareFunc) -> MiddlewareFunc:
        """Decorator to mark a function as pre-processing middleware"""
        func._is_pre_middleware = True
        return func
        
    @staticmethod
    def post_middleware(func: MiddlewareFunc) -> MiddlewareFunc:
        """Decorator to mark a function as post-processing middleware"""
        func._is_post_middleware = True
        return func
