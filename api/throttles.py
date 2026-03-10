from rest_framework.throttling import UserRateThrottle

class TieredRateThrottle(UserRateThrottle):
    """
    Custom throttle that grants unlimited access to Premium users (staff/superusers)
    while strictly limiting Free users.
    """
    def allow_request(self, request, view):
        # 1. If the user is Premium, bypass the throttle completely
        if request.user.is_authenticated and request.user.is_staff:
            return True 
        
        # 2. If the user is Free, enforce the standard 5/minute limit
        return super().allow_request(request, view)