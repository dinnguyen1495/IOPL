import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer


class BookConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('update_book', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('update_book', self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(f"Received: {text_data_json}")

    async def book_change(self, event):
        await self.send(text_data=json.dumps({"type": event["type"], "book_id": event["instance"]}))

    async def book_delete(self, event):
        await self.send(text_data=json.dumps({"type": event["type"], "book_id": event["instance"]}))