import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for handling chat connections"""

    async def connect(self):
        """Handle WebSocket connection"""
        self.room_name = self.scope['url_route']['kwargs'].get('room_name', 'general')
        self.room_group_name = f'chat_{self.room_name}'
        self.username = None

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send initial message history
        messages = await self.get_message_history()
        await self.send(text_data=json.dumps({
            'type': 'message_history',
            'messages': messages
        }))

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Send user offline status
        if self.username:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_status',
                    'username': self.username,
                    'status': 'offline',
                    'timestamp': timezone.now().isoformat()
                }
            )

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'chat_message':
            # Handle chat message
            username = data.get('username', 'Anonymous')
            message = data.get('message', '')

            # Store username for this connection
            if not self.username:
                self.username = username
                # Send user online status
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'user_status',
                        'username': username,
                        'status': 'online',
                        'timestamp': timezone.now().isoformat()
                    }
                )

            # Save message to database
            saved_message = await self.save_message(username, message, self.room_name)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': saved_message
                }
            )

        elif message_type == 'typing':
            # Handle typing indicator
            username = data.get('username', 'Anonymous')
            is_typing = data.get('is_typing', False)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'username': username,
                    'is_typing': is_typing,
                    'timestamp': timezone.now().isoformat()
                }
            )

        elif message_type == 'user_join':
            # Handle user joining
            username = data.get('username', 'Anonymous')
            self.username = username

            # Send user online status
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_status',
                    'username': username,
                    'status': 'online',
                    'timestamp': timezone.now().isoformat()
                }
            )

    async def chat_message(self, event):
        """Send chat message to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message']
        }))

    async def typing_indicator(self, event):
        """Send typing indicator to WebSocket"""
        # Don't send typing indicator back to the sender
        if event['username'] != self.username:
            await self.send(text_data=json.dumps({
                'type': 'typing_indicator',
                'username': event['username'],
                'is_typing': event['is_typing'],
                'timestamp': event['timestamp']
            }))

    async def user_status(self, event):
        """Send user status to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'user_status',
            'username': event['username'],
            'status': event['status'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def save_message(self, username, message, room):
        """Save message to database"""
        msg = Message.objects.create(
            username=username,
            content=message,
            room=room
        )
        return msg.to_dict()

    @database_sync_to_async
    def get_message_history(self):
        """Get last 50 messages from database"""
        messages = Message.objects.filter(room=self.room_name).order_by('-timestamp')[:50]
        # Reverse to show oldest first
        return [msg.to_dict() for msg in reversed(messages)]
