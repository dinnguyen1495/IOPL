import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class BookConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)('update_book', self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)('update_book', self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(f"Received: {text_data_json}")

    def book_change(self, event):
        self.send(text_data=json.dumps({"type": event["type"], "book_id": event["instance"]}))

    def book_delete(self, event):
        self.send(text_data=json.dumps({"type": event["type"], "book_id": event["instance"]}))