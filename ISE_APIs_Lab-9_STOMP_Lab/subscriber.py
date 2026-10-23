import time
import stomp


class MyListener(stomp.ConnectionListener):
    def on_message(self, frame):
        print()
        print(frame)
        for k,v in frame.headers.items():
            print('header: key %s , value %s' %(k,v))    
        message=frame.body
        print('MyListener:\nreceived a message "{}"\n'.format(message))
        global read_messages
        read_messages.append({'id': frame.headers['message-id'], 'subscription':frame.headers['subscription']})


class MyStatsListener(stomp.StatsListener):
    def on_disconnected(self):
        super(MyStatsListener, self).on_disconnected()
        print('MyStatsListener:\n{}\n'.format(self))


read_messages = []
hosts = [('198.18.133.36', 61613)]

conn = stomp.Connection(host_and_ports=hosts)
conn.set_listener('my_listener', MyListener())
conn.set_listener('stats_listener', MyStatsListener())
#conn.start()
# wait=True means that it waits until it's established a connection with the server before returning.
conn.connect(wait=True)
# id should uniquely identify the subscription
# ack = auto, client, or client-individual
# See https://stomp.github.io/stomp-specification-1.1.html#SUBSCRIBE_ack_Header
conn.subscribe(destination='/queue/test', id=1, ack='auto', persistent=True)
conn.send(body="Hi I'm an only Subscriber. I can only see sent messages", destination='/queue/test')

try:
    while True:
        time.sleep(1)
        for message in read_messages:
            conn.ack(message['id'], message['subscription'])
except KeyboardInterrupt:
    print('!!FINISH!!')
    