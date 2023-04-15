from kubernetes import client, config
import time
from app import predictions as predicted_workload

# Constants
NAMESPACE = "default"
DEPLOYMENT_NAME = "webapp"
CPU_THRESHOLD = 80
RRS = 0.1  # Remove 10% of the surplus pods in case of scaling in
POD_NAME = "mypod"
INTERVAL = 60.0  # seconds


# Initialize Kubernetes client
config.load_kube_config()
api = client.AppsV1Api()

# Helper function to get CPU and memory resources of a pod
def get_pod_resources():
    api_response = api.read_namespaced_pod(name=POD_NAME, namespace=NAMESPACE)
    cpu_capacity =api_response.spec.containers[0].resources.limits["cpu"]
    memory_capacity = api_response.spec.containers[0].resources.limits["memory"]
    return cpu_capacity, memory_capacity

# Function to calculate maximum workload
def calculate_max_workload():
    cpu_capacity, memory_capacity = get_pod_resources()
    cpu_cores = int(cpu_capacity[:-1])# remove the 'm' suffix
    memory_mb = int(memory_capacity[:-2])# remove the 'Mi' suffix
    cpu_utilization = 1  # assume maximum CPU utilization
    memory_usage_per_unit = 1  # assume constant memory usage per unit of workload
    max_workload_cpu = cpu_cores * cpu_utilization
    max_workload_memory = memory_mb / memory_usage_per_unit
    max_workload = min(max_workload_cpu, max_workload_memory)
    return max_workload
def pods_minimum():
    api_response = api.read_deployment(name=DEPLOYMENT_NAME, namespace=NAMESPACE)
    min_replicas=api_response.spec.replicas
    return min_replicas




# Helper function to get the current number of replicas
def get_replica_count():
    deployment = api.read_namespaced_deployment(name=DEPLOYMENT_NAME, namespace=NAMESPACE)
    return deployment.spec.replicas

# Helper function to scale up
def scale_up(replicas):
    api.patch_namespaced_deployment_scale(
        name=DEPLOYMENT_NAME,
        namespace=NAMESPACE,
        body={"spec": {"replicas": replicas}}
    )
    print(f"Scaled up to {replicas} replicas")

# Helper function to scale down
def scale_down(replicas):
    api.patch_namespaced_deployment_scale(
        name=DEPLOYMENT_NAME,
        namespace=NAMESPACE,
        body={"spec": {"replicas": replicas}}
    )
    print(f"Scaled down to {replicas} replicas")

# Main loop
while True:
    max_workload_per_pod = calculate_max_workload()
    
    future_pods=predicted_workload/max_workload_per_pod
    current_pods=get_replica_count()
    if future_pods>current_pods:
        scale_up(future_pods)
    elif future_pods<current_pods:
        future_pods=max(future_pods,pods_minimum)
        pods_surplus=(current_pods-future_pods)*RRS
        future_pods=current_pods-pods_surplus
        scale_down(future_pods)
    else:
        print("No scaling required")
    time.sleep(INTERVAL)
    
    


    
   
    
