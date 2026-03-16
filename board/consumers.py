import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Board, Stroke
from .serializers import StrokeSerializers

class BoardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.board_slug = self.scope['url_route']['kwargs']['board_slug']
        self.room_group_name = f'board_{self.board_slug}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        saved_stroke = await self.save_stroke(data)

        if saved_stroke:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'draw_event',
                    'data': saved_stroke
                }
            )

    async def draw_event(self, event):
        await self.send(text_data=json.dumps(event['data']))

    @database_sync_to_async
    def save_stroke(self, data):
        try:
            board = Board.objects.get(slug=self.board_slug)
            user = self.scope["user"]
            serializer = StrokeSerializers(data={'board': board.id, 'data': data.get('stroke_data')})
            if serializer.is_valid():
                serializer.save(user=user if user.is_authenticated else None)
                return serializer.data
        except Board.DoesNotExist:
            return None
        return None
