# utils/ip_utils.py
from fastapi import Request

def get_client_real_ip(request: Request) -> str:
    """
    获取用户真实IP（兼容反向代理/直接访问）
    """
    # 1. 优先从反向代理透传的头解析（Nginx等）
    x_real_ip = request.headers.get("X-Real-IP")
    x_forwarded_for = request.headers.get("X-Forwarded-For")

    if x_real_ip:
        real_ip = x_real_ip
    elif x_forwarded_for:
        # X-Forwarded-For 可能有多个IP（逗号分隔），取第一个非内网的
        real_ip = x_forwarded_for.split(",")[0].strip()
    else:
        # 2. 无反向代理时，从client获取（可能是IPv6）
        real_ip = request.client.host if request.client else ""

    # 处理IPv6本地地址/兼容前缀
    if real_ip in ["::1", "0:0:0:0:0:0:0:1"]:
        real_ip = "127.0.0.1"  # 本地测试时的默认IP
    # 去除IPv6兼容IPv4的前缀（如 ::ffff:192.168.1.1 → 192.168.1.1）
    if real_ip.startswith("::ffff:"):
        real_ip = real_ip.replace("::ffff:", "")

    # 过滤内网IP（可选，根据业务需求）
    intranet_prefixes = ["192.168.", "10.", "172.", "127."]
    if any(real_ip.startswith(p) for p in intranet_prefixes) and not real_ip == "127.0.0.1":
        # 生产环境若拿到内网IP，可记录日志并返回空（或根据业务调整）
        return ""

    return real_ip