# import json
# from webbrowser import get
# from channels.consumer import AsyncConsumer
# from channels.db import database_sync_to_async
# from django.contrib.auth import get_user_model
# User =get_user_model()

# class ChatConsumer(AsyncConsumer):
#     async def websocket_connect(self,event):
#         print("connected",event)
#     async def websocket_recive(self,event):
#         print("receved",event)
#     async def websocket_disconnect(self,event):
#         print("disconnect",event)