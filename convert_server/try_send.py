from celery import Celery

broker_url = 'redis://localhost:6379/10'
backend_url = 'redis://localhost:6379/11'

client = Celery('convert_deal', backend=backend_url, broker=broker_url)


def send_deal(msg):
    client.send_task('convert_center.receive', (msg,))


if __name__ == '__main__':
    send_deal('this is a test deal')