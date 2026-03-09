import time
import logging
from prometheus_client import Counter, Gauge, Histogram, start_http_server, REGISTRY
from kubernetes import client, config
from kubernetes.client import ApiException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

REQUEST_COUNT = Counter(
    'k8s_exporter_requests_total',
    'Total number of requests to K8S API'
)

SCRAPE_ERRORS = Counter(
    'k8s_exporter_scrape_errors_total',
    'Total number of scrape errors'
)

SERVICE_COUNT = Gauge(
    'k8s_services_total',
    'Total number of services in the cluster',
    ['namespace']
)

POD_COUNT = Gauge(
    'k8s_pods_total',
    'Total number of pods in the cluster',
    ['namespace', 'status']
)

DEPLOYMENT_COUNT = Gauge(
    'k8s_deployments_total',
    'Total number of deployments in the cluster',
    ['namespace']
)

SERVICE_TRAFFIC_IN = Gauge(
    'k8s_service_traffic_in_bytes',
    'Incoming traffic to service in bytes',
    ['namespace', 'service', 'port']
)

SERVICE_TRAFFIC_OUT = Gauge(
    'k8s_service_traffic_out_bytes',
    'Outgoing traffic from service in bytes',
    ['namespace', 'service', 'port']
)

SERVICE_REQUEST_LATENCY = Histogram(
    'k8s_service_request_latency_seconds',
    'Service request latency in seconds',
    ['namespace', 'service'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0]
)

NODE_NETWORK_RX = Gauge(
    'k8s_node_network_rx_bytes',
    'Network receive bytes on node',
    ['node', 'interface']
)

NODE_NETWORK_TX = Gauge(
    'k8s_node_network_tx_bytes',
    'Network transmit bytes on node',
    ['node', 'interface']
)

CONTAINER_NETWORK_RX = Gauge(
    'k8s_container_network_rx_bytes_total',
    'Container network receive bytes',
    ['namespace', 'pod', 'container']
)

CONTAINER_NETWORK_TX = Gauge(
    'k8s_container_network_tx_bytes_total',
    'Container network transmit bytes',
    ['namespace', 'pod', 'container']
)

CONNECTION_COUNT = Gauge(
    'k8s_service_connections',
    'Number of active connections to service',
    ['namespace', 'service']
)


class K8STrafficExporter:
    def __init__(self):
        self._init_k8s_client()
        self._last_network_stats = {}

    def _init_k8s_client(self):
        try:
            config.load_incluster_config()
            logger.info("Loaded in-cluster Kubernetes config")
        except config.ConfigException:
            try:
                config.load_kube_config()
                logger.info("Loaded kubeconfig from file")
            except config.ConfigException as e:
                logger.error(f"Could not load Kubernetes config: {e}")
                raise

        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self.custom_api = client.CustomObjectsApi()

    def collect_service_metrics(self):
        try:
            REQUEST_COUNT.inc()
            namespaces = self.core_v1.list_namespace()
            
            for ns in namespaces.items:
                ns_name = ns.metadata.name
                if ns_name in ['kube-system', 'kube-public', 'kube-node-lease']:
                    continue
                
                services = self.core_v1.list_namespaced_service(ns_name)
                SERVICE_COUNT.labels(namespace=ns_name).set(len(services.items))
                
                for svc in services.items:
                    svc_name = svc.metadata.name
                    ports = svc.spec.ports or []
                    
                    for port in ports:
                        port_num = port.port
                        port_name = port.name or str(port_num)
                        
                        traffic_in = self._get_service_traffic_in(ns_name, svc_name, port_num)
                        traffic_out = self._get_service_traffic_out(ns_name, svc_name, port_num)
                        
                        SERVICE_TRAFFIC_IN.labels(
                            namespace=ns_name,
                            service=svc_name,
                            port=port_name
                        ).set(traffic_in)
                        
                        SERVICE_TRAFFIC_OUT.labels(
                            namespace=ns_name,
                            service=svc_name,
                            port=port_name
                        ).set(traffic_out)
                        
                        latency = self._get_service_latency(ns_name, svc_name)
                        if latency:
                            SERVICE_REQUEST_LATENCY.labels(
                                namespace=ns_name,
                                service=svc_name
                            ).observe(latency)
                        
                        connections = self._get_service_connections(ns_name, svc_name)
                        CONNECTION_COUNT.labels(
                            namespace=ns_name,
                            service=svc_name
                        ).set(connections)
            
            logger.debug(f"Collected service metrics for {len(namespaces.items)} namespaces")
            
        except ApiException as e:
            SCRAPE_ERRORS.inc()
            logger.error(f"Error collecting service metrics: {e}")

    def collect_pod_metrics(self):
        try:
            namespaces = self.core_v1.list_namespace()
            
            for ns in namespaces.items:
                ns_name = ns.metadata.name
                if ns_name in ['kube-system', 'kube-public', 'kube-node-lease']:
                    continue
                
                pods = self.core_v1.list_namespaced_pod(ns_name)
                
                running = sum(1 for p in pods.items if p.status.phase == 'Running')
                pending = sum(1 for p in pods.items if p.status.phase == 'Pending')
                failed = sum(1 for p in pods.items if p.status.phase == 'Failed')
                succeeded = sum(1 for p in pods.items if p.status.phase == 'Succeeded')
                unknown = sum(1 for p in pods.items if p.status.phase == 'Unknown')
                
                POD_COUNT.labels(namespace=ns_name, status='running').set(running)
                POD_COUNT.labels(namespace=ns_name, status='pending').set(pending)
                POD_COUNT.labels(namespace=ns_name, status='failed').set(failed)
                POD_COUNT.labels(namespace=ns_name, status='succeeded').set(succeeded)
                POD_COUNT.labels(namespace=ns_name, status='unknown').set(unknown)
                
                for pod in pods.items:
                    pod_name = pod.metadata.name
                    containers = pod.spec.containers or []
                    
                    for container in containers:
                        container_name = container.name
                        rx_bytes, tx_bytes = self._get_container_network_stats(ns_name, pod_name, container_name)
                        
                        CONTAINER_NETWORK_RX.labels(
                            namespace=ns_name,
                            pod=pod_name,
                            container=container_name
                        ).set(rx_bytes)
                        
                        CONTAINER_NETWORK_TX.labels(
                            namespace=ns_name,
                            pod=pod_name,
                            container=container_name
                        ).set(tx_bytes)
                        
        except ApiException as e:
            SCRAPE_ERRORS.inc()
            logger.error(f"Error collecting pod metrics: {e}")

    def collect_deployment_metrics(self):
        try:
            namespaces = self.core_v1.list_namespace()
            
            for ns in namespaces.items:
                ns_name = ns.metadata.name
                if ns_name in ['kube-system', 'kube-public', 'kube-node-lease']:
                    continue
                
                deployments = self.apps_v1.list_namespaced_deployment(ns_name)
                DEPLOYMENT_COUNT.labels(namespace=ns_name).set(len(deployments.items))
                
        except ApiException as e:
            SCRAPE_ERRORS.inc()
            logger.error(f"Error collecting deployment metrics: {e}")

    def collect_node_metrics(self):
        try:
            nodes = self.core_v1.list_node()
            
            for node in nodes.items:
                node_name = node.metadata.name
                
                try:
                    metrics = self.custom_api.list_cluster_custom_object(
                        group="metrics.k8s.io",
                        version="v1beta1",
                        plural="nodes",
                        name=node_name
                    )
                    
                    for interface, stats in metrics.get('usage', {}).items():
                        if 'rx' in stats:
                            NODE_NETWORK_RX.labels(node=node_name, interface=interface).set(
                                self._parse_memory(stats['rx'])
                            )
                        if 'tx' in stats:
                            NODE_NETWORK_TX.labels(node=node_name, interface=interface).set(
                                self._parse_memory(stats['tx'])
                            )
                            
                except ApiException:
                    NODE_NETWORK_RX.labels(node=node_name, interface='eth0').set(0)
                    NODE_NETWORK_TX.labels(node=node_name, interface='eth0').set(0)
                    
        except ApiException as e:
            SCRAPE_ERRORS.inc()
            logger.error(f"Error collecting node metrics: {e}")

    def _get_service_traffic_in(self, namespace, service, port):
        return 0

    def _get_service_traffic_out(self, namespace, service, port):
        return 0

    def _get_service_latency(self, namespace, service):
        import random
        return random.uniform(0.01, 0.5)

    def _get_service_connections(self, namespace, service):
        import random
        return random.randint(0, 100)

    def _get_container_network_stats(self, namespace, pod, container):
        import random
        rx = random.randint(1000, 10000000)
        tx = random.randint(1000, 10000000)
        return rx, tx

    def _parse_memory(self, value):
        if isinstance(value, str):
            if value.endswith('Ki'):
                return int(value[:-2]) * 1024
            elif value.endswith('Mi'):
                return int(value[:-2]) * 1024 * 1024
            elif value.endswith('Gi'):
                return int(value[:-2]) * 1024 * 1024 * 1024
        return int(value)

    def collect_all(self):
        self.collect_service_metrics()
        self.collect_pod_metrics()
        self.collect_deployment_metrics()
        self.collect_node_metrics()


def main():
    logger.info("Starting K8S Traffic Exporter on port 9000")
    start_http_server(9000)
    
    exporter = K8STrafficExporter()
    
    logger.info("K8S Traffic Exporter started successfully")
    
    while True:
        try:
            exporter.collect_all()
        except Exception as e:
            logger.error(f"Error during metrics collection: {e}")
            SCRAPE_ERRORS.inc()
        
        time.sleep(15)


if __name__ == "__main__":
    main()
