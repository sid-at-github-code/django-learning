from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from accounts.models import User
from django.contrib.auth.models import AnonymousUser


class SessionAuthMiddleware(BaseMiddleware):
    """
    Custom middleware to authenticate WebSocket connections using session data
    """
    
    async def __call__(self, scope, receive, send):
        # Get session data from the scope
        session = scope.get('session', {})
        user_id = session.get('user_id')
        
        if user_id:
            # Get user from database
            user = await self.get_user(user_id)
            scope['user'] = user
        else:
            scope['user'] = AnonymousUser()
        
        return await super().__call__(scope, receive, send)
    
    @database_sync_to_async
    def get_user(self, user_id):
        """Get user from database by ID"""
        try:
            return User.objects.get(id=user_id)
        except (User.DoesNotExist, ValueError, TypeError):
            return AnonymousUser()
