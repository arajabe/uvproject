from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.utils.audit_events import set_audit_user

class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Example: get user_id from header (or JWT/session)
        print("request.headers")
        print(request.headers.keys)
        #user_id = request.headers.get("X-User-Id",)

        #set_audit_user(user_id)  # inject user into audit context
        print("AuditMiddleware")
       
        response = await call_next(request)
        return response

