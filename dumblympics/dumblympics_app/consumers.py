import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Player, Race

class RaceConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.races = {}

    def connect(self):
        self.race_id = self.scope['url_route']['kwargs']['race_id']
        self.race_group_name = 'race_%s' % self.race_id
        self.races[self.race_id] = self.races.get(self.race_id, {"players": {}})

        # Join race group
        async_to_sync(self.channel_layer.group_add)(
            self.race_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave race group
        async_to_sync(self.channel_layer.group_discard)(
            self.race_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        try:
            json_data = json.loads(text_data)
            json_data["command"]
        except Exception as e:
            print("error",e)
            return
        
        if json_data.get("command") == 'hello':
            self.on_hello(json_data)
        elif json_data.get("command") == "update_score":
            self.update_score(json_data)
        
    def _broadcast_message(self, json_data):
        async_to_sync(self.channel_layer.group_send)(
            self.race_group_name,
            {
                'type': 'broadcast',
                'data': json_data
            }
        )

    def update_score(self, json_data):
        Player.objects.filter(race_id=self.race_id, uid=json_data["player_id"]).update(score=json_data["score"])
        
        leaderboard = Player.objects.filter(race_id=self.race_id).order_by('-score').values_list("nick", "score")
        self._broadcast_message({"event": "new_leaderboard", "leaderboard": [{"nickname": line[0], "score": line[1]} for line in leaderboard]})

    def on_hello(self, json_data):
        race = Race.objects.get(id=self.race_id)
        if not race.open:        
            # a guy is reconnecting
            self.send(text_data=json.dumps({
                'event': 'new_player',
                'players': {
                    player.uid: {"id": player.uid, "nickname": player.nick, "score": player.score}
                    for player in 
                    Player.objects.filter(race_id=self.race_id)
                }
            }))
            self.send(text_data=json.dumps({"event": "gooo", "start": race.start.isoformat()}))
            return 

        nick = json_data["player"]["nickname"]
        uid = json_data['player']['id']
        Player.objects.filter(nick=nick, race_id=self.race_id).update(uid=uid)
        
        self.races[self.race_id]['players'][uid] = {
            "nickname": nick,
            'id': uid,
            "score": 0,
        }
        self._broadcast_message({
            'event': 'new_player',
            'players': {
                player.uid: {"id": player.uid, "nickname": player.nick, "score": player.score}
                for player in 
                Player.objects.filter(race_id=self.race_id)
            }
        })
        if Player.objects.filter(race_id=self.race_id).count() == 2:
            self.gooo()

    def gooo(self):
        from django.utils.timezone import now
        start = now()
        Race.objects.filter(id=self.race_id).update(open=False, start=start)
        self._broadcast_message({"event": "gooo", "start":start.isoformat()})

    # Receive message from race group
    def broadcast(self, event):
        self.send(text_data=json.dumps(event['data']))

