
# internal services
from app.configures import SpiderConfigurator, ApiConfiguration
from threading import Thread
# handle schedule
thread = Thread(target=SpiderConfigurator().run)
thread.start()
ApiConfiguration(__name__).run()

