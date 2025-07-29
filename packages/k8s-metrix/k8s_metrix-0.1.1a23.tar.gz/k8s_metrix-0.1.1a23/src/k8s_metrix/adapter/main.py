from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from k8s_metrix import K8sMetrix
import logging
from contextlib import asynccontextmanager
from logging import getLogger
from fastapi.openapi.utils import get_openapi
from k8s_metrix.backends import FsBackend
from k8s_metrix.backends import BaseBackend
from rich.logging import RichHandler
import os
from datetime import datetime, timedelta
import asyncio

logging.basicConfig(level=logging.DEBUG, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])


logger = getLogger(__name__)
BACKEND = os.getenv("METRIX_BACKEND", "fs").lower()

# Store previous counter values for rate calculation
# Format: {metric_key: [{"value": value, "timestamp": timestamp}, ...]}
# Keep last 60 seconds of data points
counter_history: Dict[str, List[Dict[str, Any]]] = {}

backend: BaseBackend
if BACKEND == "fs":
    logger.debug("[metrix-server]: Using file system backend for storing metrics")
    backend = FsBackend(path="metrix_data")
else:
    logger.error(f"[metrix-server]: Unsupported backend '{BACKEND}'. Only 'fs' is supported.")
    raise ValueError(f"Unsupported backend '{BACKEND}'. Only 'fs' is supported.")

# Pydantic models for request validation
class MetricData(BaseModel):
    name: str
    value: int
    timestamp: str
    metric_type: str = "gauge"  # "counter" or "gauge"
    additional_info: Dict[str, Any] = {}


class MetricsPayload(BaseModel):
    pod_name: str
    pod_namespace: str
    service_name: str
    node_name: str
    metrics: List[MetricData]
    timestamp: str



@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Example lifespan function that can be registered with the LifeSpanManager.
    This function will be called during the startup and shutdown of the FastAPI app.
    """
    logger.debug("[metrix-server]: starting lifespan function")
    await backend.init_backend()
    yield
    logger.debug("[metrix-server]: shutting down lifespan function")


app = FastAPI(docs_url="/", lifespan=lifespan)


@app.post("/metrics")
async def receive_metrics(payload: MetricsPayload):
    """
    Endpoint to receive metrics from K8sMetrix clients.
    
    Args:
        payload: The metrics payload containing pod info and metrics data
    """
    try:
        logger.debug(f"[metrix-server]: Received {len(payload.metrics)} metrics from pod "
                    f"{payload.pod_name} in namespace {payload.pod_namespace}")  # fmt: skip
        
        for metric in payload.metrics:
            await process_metric(metric, payload)
        
        return {"status": "success", "processed_metrics": len(payload.metrics)}
        
    except Exception as e:
        logger.error(f"[metrix-server]: Error processing metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing metrics: {str(e)}")


@app.get("/apis/custom.metrics.k8s.io/v1beta2")
async def get_all_metrics():
    """
    Endpoint to retrieve all metrics in Kubernetes custom metrics API format.
    """
    logger.debug("[metrix-server]: retrieving all metrics")
    keys = await backend.list_all_metrics()

    resources = []
    for key in keys:
        parts = key.split("/")
        
        if len(parts) >= 4:
            # Parse the metric key: resource_type/namespace/resource_name/metric_name
            resource_type = parts[0]  # service, pod, or no_resource_type
            metric_name = parts[3]
            
            if resource_type == "service":
                k8s_resource = "services"
            elif resource_type == "pod":
                k8s_resource = "pods"
            else:
                k8s_resource = "pods"

            resource_entry = {
                "name": f"{k8s_resource}/{metric_name}",
                "singularName": "",
                "namespaced": True,
                "kind": "MetricValueList",
                "verbs": ["get"]
            }
            if not any(r["name"] == resource_entry["name"] for r in resources):
                resources.append(resource_entry)

    logger.debug(f"[metrix-server]: Found {len(resources)} unique metrics")
    return {
        "kind": "APIResourceList",
        "apiVersion": "v1",
        "groupVersion": "custom.metrics.k8s.io/v1beta2",
        "resources": resources
    }

@app.get("/apis/custom.metrics.k8s.io/v1beta2/namespaces/{namespace}/{resource_type}/{resource_name}/{metric_name}")
async def get_metric_value(namespace: str, resource_type: str, resource_name: str, metric_name: str):
    """
    Endpoint to retrieve a specific metric value for a given resource.
    
    Args:
        resource_type: Type of the resource (e.g., pods, services)
        namespace: Namespace of the resource
        resource_name: Name of the resource
        metric_name: Name of the metric to retrieve
    """
    logger.debug(f"[metrix-server]: Retrieving metric '{metric_name}' for {resource_type} "
                 f"{resource_name} in namespace {namespace}")
    if resource_type == "pods":
        values = await backend.retrieve(
            name=metric_name,
            pod=resource_name,
            namespace=namespace
        )
    elif resource_type == "services":
        values = await backend.retrieve(
            name=metric_name,
            service=resource_name,
            namespace=namespace
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported resource type '{resource_type}'")
    if not values:
        raise HTTPException(status_code=404, detail=f"Metric '{metric_name}' not found for {resource_type} "
                                                    f"{resource_name} in namespace {namespace}")
    
    return {
        "kind": "MetricValueList",
        "apiVersion": "custom.metrics.k8s.io/v1beta2",
        "metadata": {},
        "items": [
            {
                "describedObject": {
                    "kind": resource_type.capitalize(),
                    "namespace": namespace,
                    "name": resource_name,
                    "apiVersion": "v1"
                },
                "metric": {
                    "name": metric_name
                },
                "timestamp": values.get("timestamp", ""),
                "windowSeconds": 60,
                "value": str(values.get("value", 0))
            }
        ]
    }

# Service example response for the above endpoint:
# {
#   "kind": "MetricValueList",
#   "apiVersion": "custom.metrics.k8s.io/v1beta2",
#   "metadata": {},
#   "items": [
#     {
#       "describedObject": {
#         "kind": "Service",
#         "namespace": "default",
#         "name": "my-backend-service",
#         "apiVersion": "v1"
#       },
#       "metric": {
#         "name": "http_request_rate"
#       },
#       "timestamp": "2025-06-07T18:30:00Z",
#       "windowSeconds": 60,
#       "value": "300"
#     }
#   ]
# }
# Pod example response for the above endpoint:
# {
#   "kind": "MetricValueList",
#   "apiVersion": "custom.metrics.k8s.io/v1beta2",
#   "metadata": {},
#   "items": [
#     {
#       "describedObject": {
#         "kind": "Pod",
#         "namespace": "default",
#         "name": "my-pod-123",
#         "apiVersion": "v1"
#       },
#       "metric": {
#         "name": "my_custom_metric"
#       },
#       "timestamp": "2025-06-07T18:30:00Z",
#       "windowSeconds": 60,
#       "value": "42"
#     }
#   ]
# }

@app.get("/openapi/v2")
async def openapi():
    """
    Custom OpenAPI schema endpoint.
    """
    openapi_schema = get_openapi(
        title="K8s Metrix API",
        version="1.0.0",
        description="API for K8s Metrix",
        routes=app.routes,
    )
    return openapi_schema

@app.get("/apis")
async def get_apis():
    """
    Endpoint to retrieve all APIs.
    """
    return {
        "kind": "APIResourceList",
        "apiVersion": "v1",
        "groupVersion": "custom.metrics.k8s.io/v1beta2",
        "resources": [
            {
                "name": "metrics",
                "singularName": "",
                "namespaced": True,
                "kind": "MetricValueList",
                "verbs": ["get"]
            }
        ]
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "k8s-metrix-adapter"}

async def process_metric(metric: MetricData, payload: MetricsPayload):
    """
    Process a single metric based on its type.
    
    Args:
        metric: The metric data to process
        payload: The full payload containing pod/service information
    """
    metric_key = f"pod/{payload.pod_namespace}/{payload.pod_name}/{metric.name}"
    
    if metric.metric_type == "counter":
        # Handle counter metrics - calculate rate and save as _per_second
        await process_counter_metric(metric, payload, metric_key)
    else:
        # Handle gauge metrics - store as-is
        await process_gauge_metric(metric, payload, metric_key)


async def process_counter_metric(metric: MetricData, payload: MetricsPayload, metric_key: str):
    """
    Process counter metrics by calculating average per-second rate over the past 60 seconds.
    Average = sum of all increments in past 60 seconds / 60
    """
    global counter_history
    
    current_timestamp = datetime.fromisoformat(metric.timestamp.replace('Z', '+00:00'))
    current_value = metric.value
    
    # Initialize history for this metric if not exists
    if metric_key not in counter_history:
        counter_history[metric_key] = []
    
    # Add current data point
    counter_history[metric_key].append({
        "value": current_value,
        "timestamp": current_timestamp
    })
    
    # Remove data points older than 60 seconds
    cutoff_time = current_timestamp - timedelta(seconds=60)
    counter_history[metric_key] = [
        data_point for data_point in counter_history[metric_key]
        if data_point["timestamp"] >= cutoff_time
    ]
    
    # Calculate sum of all increments in past 60 seconds, divide by 60
    if len(counter_history[metric_key]) >= 2:
        data_points = counter_history[metric_key]
 
        # Sum all increments between consecutive data points
        total_increments = 0
        for i in range(1, len(data_points)):
            increment = max(0, data_points[i]["value"] - data_points[i-1]["value"])
            total_increments += increment

        # Average per second = total increments / 60 seconds
        avg_per_second = total_increments / 60
        
        # Store the average rate with _per_second suffix
        per_second_name = f"{metric.name}_per_second"
        await backend.record(
            name=per_second_name,
            value=avg_per_second,
            service=payload.service_name,
            pod=payload.pod_name,
            namespace=payload.pod_namespace
        )
        
        logger.debug(f"[metrix-server]: Calculated {per_second_name} = {avg_per_second:.2f} "
                    f"(total_increments: {total_increments}, data_points: {len(data_points)})")  # fmt: skip


async def process_gauge_metric(metric: MetricData, payload: MetricsPayload, metric_key: str):
    """
    Process gauge metrics by storing them as-is.
    """
    await backend.record(
        name=metric.name,
        value=metric.value,
        service=payload.service_name,
        pod=payload.pod_name,
        namespace=payload.pod_namespace
    )
    
    logger.debug(f"[metrix-server]: Stored gauge metric {metric_key} = {metric.value}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)