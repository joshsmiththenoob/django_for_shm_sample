# Custom Throttling: Create custom throttling for specific CBV(APIs) that every CBV got its request rate(frequency) individually 
from rest_framework.throttling import (AnonRateThrottle,
                                       UserRateThrottle)


# Inherit parent class to override method
class BridgeListThrottle(UserRateThrottle):
    # Define scope for request frequency setting
    scope = "bridge-list"
    

class BridgeGetThrottle(UserRateThrottle):
    scope = "bridge-get"