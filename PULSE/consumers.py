import json
from channels.generic.websocket import AsyncWebsocketConsumer

class FeedbackConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "feedback_updates"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # This server only pushes, does not handle incoming messages from client
        pass

    async def feedback_update(self, event):
        # Send the feedback update to WebSocket
        await self.send(text_data=json.dumps(event["data"]))
