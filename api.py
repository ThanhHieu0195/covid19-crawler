
# internal services
from app.configures import SpiderConfigurator, ApiConfiguration

ApiConfiguration(__name__).run()
# handle schedule
SpiderConfigurator().run()