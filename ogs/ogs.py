import requests as rq
import socketio

HOST = "https://online-go.com/"

class Message:
	data = {	"access_token": "",
						"expires_in": 0,
						"token_type": "",
						"scope": "",
						"refresh_token": ""	}

	def __init__(self, user: str, pwd: str, client_id: str):
		data = {	'grant_type': 'password',
							'username': user,
							'password': pwd,
							'client_id': client_id	}
		res = rq.post( HOST + 'oauth2/token/', data	).json()
		for item in res:
			self.data[item] = res[item]

sio = socketio.Client()

def connect_to_host():
	@sio.event
	def connect():
		print("sio connected")
	sio.connect( HOST + 'socket.io/', transports='websocket')

def connect_to_game(player_id: str, game_id: str):
	sio.emit('game/connect', player_id, game_id, 'true')

print("Enter username:")
user = input()
print("Enter password:")
pwd = input()

auth = Message(	user, 
								pwd, 
								"qhmPg1CAmR13T46CZfnf9cQDBkAqOOYVG5kbk53t"	)
print( auth.data )
user = rq.get( HOST + 'api/v1/me/', data=auth.data )
games = rq.get( HOST + 'api/v1/me/games/', data=auth.data )
results = games.json()["results"]
for result in results:
	print( result.get("name"), result.get("outcome"), result.get('id'))
	if( result.get("outcome") == "" ):
		game = result.get("id")
if 'game' not in locals():
	raise Exception( 'Unable to locate valid game.' )
connect_to_host()
connect_to_game( user.get('id'), game )
auth.data["move"] = input()
resp = rq.post( HOST + f'api/v1/games/{game}/move/', data=auth.data )
