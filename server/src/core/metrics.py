import time
from typing import Dict, Optional
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from fastapi.responses import PlainTextResponse


http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

http_requests_active = Gauge(
    'http_requests_active',
    'Currently active HTTP requests'
)


class MetricsMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        
        if request.url.path == "/metrics":
            await self.app(scope, receive, send)
            return

        method = request.method
        path = request.url.path
        
        endpoint = self._get_endpoint_name(path)
        
        http_requests_active.inc()
        start_time = time.time()
        
        async def send_with_metrics(message):
            if message["type"] == "http.response.start":
                duration = time.time() - start_time
                status_code = str(message["status"])
                
                http_requests_total.labels(
                    method=method,
                    endpoint=endpoint,
                    status_code=status_code
                ).inc()
                
                http_request_duration_seconds.labels(
                    method=method,
                    endpoint=endpoint
                ).observe(duration)
                
                http_requests_active.dec()
            
            await send(message)
        
        await self.app(scope, receive, send_with_metrics)

    def _get_endpoint_name(self, path: str) -> str:
        return path


async def metrics_endpoint():
    return PlainTextResponse(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
