# middleware.py
import time
from django.utils.deprecation import MiddlewareMixin

class TimingMiddleware(MiddlewareMixin):
    """记录请求信息和IP的中间件"""

    def get_client_ip(self, request):
        """提取客户端IP"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

    def process_request(self, request):
        # 记录请求开始时间和IP
        request.start_time = time.time()
        request.client_ip = self.get_client_ip(request)

        # 也可以记录其他信息
        request.user_agent = request.META.get('HTTP_USER_AGENT', '')
        request.referer = request.META.get('HTTP_REFERER', '')

        return None

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time

            # 获取IP
            ip = getattr(request, 'client_ip', 'unknown')

            # 添加到响应头（可选）
            response['X-Client-IP'] = ip
            response['X-Request-Time'] = f'{duration:.3f}s'

            # 打印到控制台
            print(
                f"IP: {ip} | "
                f"方法: {request.method} | "
                f"路径: {request.path} | "
                f"用时: {duration:.3f}s | "
                f"状态码: {response.status_code}"
            )


        return response