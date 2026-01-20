from prometheus_client import Counter, Gauge, Summary, Histogram, start_http_server
import psutil
import time
class test:
    def __init__(self):
        # 定义指标
        self.request_count = Counter('request_count', 'Total number of requests')
        self.cpu_usage = Gauge('cpu_usage', 'CPU usage percentage')
        self.request_latency = Summary('request_latency_seconds', 'Request latency in seconds')
        self.response_size = Histogram('response_size_bytes', 'Response size in bytes', buckets=[100, 500, 1000, 5000, 10000])

    def simulate_metrics(self):
        print("Simulating metrics...")
        while True:
            # 模拟请求计数
            self.request_count.inc()

            # 模拟CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            self.cpu_usage.set(cpu_percent)

            # 模拟请求延迟
            with self.request_latency.time():
                time.sleep(0.1)  # 模拟处理时间

            # 模拟响应大小
            response_size_value = 200 + (8000 * psutil.cpu_percent() / 100)  # 根据CPU使用率模拟响应大小
            self.response_size.observe(response_size_value)

            time.sleep(1)  # 每秒更新一次指标
if __name__ == "__main__":
    start_http_server(9000)
    test_instance = test()
    test_instance.simulate_metrics()

def run_metrics_server():
    print("Starting Prometheus metrics server on http://localhost:9000")
    start_http_server(9000)
    test_instance = test()
    test_instance.simulate_metrics()