
from os import times
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from asgiref.sync import async_to_sync,sync_to_async
import json
from .models import *
import time


class ImportBatches(WebsocketConsumer):
    def connect(self):
        self.room_name =  'import' #self.scope['url_route']['kwargs']['batch_id']
        self.channel_name = 'import'
        self.room_group_name = 'import'
        print(self.room_group_name)
        print('Channles Connect')
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name, 
        )
        self.accept()


        self.send(text_data=json.dumps({
                'payload': f"connected from second "
        }))
        
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    def receive(self, text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'import_status',
                'payload': text_data
            }
        )

    def import_status(self, event):
        print(event)
        data = json.loads(event['value'])
        self.send(text_data=json.dumps({
            'payload': data
        }))
        

class OrderProgress(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = 'order'
        self.room_group_name = 'order'
        print(self.room_group_name)
        
        await (self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        #channel_layer = get_channel_layer()

        # await (channel_layer.group_send)(
        #     'order' ,{
        #         'type': 'order_status',
        #         'value': json.dumps({'batch' : 'created'})
        #     }
        # )
    
        await self.accept()
        
        await self.send(text_data=json.dumps({
            'payload': "connected"
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        await (self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'order_status',
                'payload': text_data
            }
        )

    # Receive message from room group
    async def order_status(self, event):
        print(event)
        data = json.loads(event['value'])
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'payload': data
        }))