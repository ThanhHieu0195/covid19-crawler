
# internal services
from app.configures import SpiderConfigurator, ApiConfiguration
from threading import Thread
import argparse

# handle args

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='0.0.0.0')
parser.add_argument('--port', type=int, default=331)
parser.add_argument('--debug', type=bool, default=False)
parser.add_argument('--time-exec', type=int, default=1)
args = parser.parse_args()

# handle schedule
thread = Thread(target=SpiderConfigurator(args).run)
thread.start()
ApiConfiguration(__name__).run(args)

