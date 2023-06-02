import socketio

sio = socketio.Server(async_mode='threading')

@sio.event
def connect(sid, environ):
    print('Client connected:', sid)

@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

@sio.event
def my_event(sid, data):
    print('Received data from client:', data)
    sio.emit('my_response', {'response': 'OK'}, room=sid)
