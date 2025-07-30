import logging
from fastmcp import FastMCP
from pydantic import BaseModel
from kubernetes import client, config
from typing import Dict, Any, List
from kubernetes.stream import stream

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load kubeconfig (assume local for now)
try:
    config.load_kube_config()
    k8s_core = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()
    networking_v1 = client.NetworkingV1Api()
    logger.info("Kubernetes client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Kubernetes client: {e}")
    k8s_core = None
    apps_v1 = None
    networking_v1 = None

mcp = FastMCP("K8s MCP Server")

@mcp.resource("resource://k8s/metadata")
def metadata_resource() -> Dict[str, Any]:
    return {
        "name": "Kubernetes Integration",
        "version": "0.1.0",
        "description": "Integration with Kubernetes for cluster investigation",
        "capabilities": ["list_namespaces"]
    }

class ListNamespacesParams(BaseModel):
    pass  # No params needed for this tool

@mcp.tool("list_namespaces")
def list_namespaces(params: ListNamespacesParams) -> Dict[str, Any]:
    if not k8s_core:
        return {"error": "Kubernetes client not configured"}
    try:
        ns_list = k8s_core.list_namespace()
        namespaces = [item.metadata.name for item in ns_list.items]
        return {"namespaces": namespaces}
    except Exception as e:
        logger.error(f"Error listing namespaces: {e}")
        return {"error": str(e)}

class ListResourcesParams(BaseModel):
    resource_type: str  # e.g., "pods", "services", "deployments", etc.
    namespace: str = None

@mcp.tool("list_resources")
def list_resources(params: ListResourcesParams) -> Dict[str, Any]:
    try:
        rt = params.resource_type.lower()
        ns = params.namespace
        if rt == "pods":
            if ns:
                pods = k8s_core.list_namespaced_pod(ns)
            else:
                pods = k8s_core.list_pod_for_all_namespaces()
            return {"pods": [{"name": p.metadata.name, "namespace": p.metadata.namespace, "status": p.status.phase} for p in pods.items]}
        elif rt == "services":
            if ns:
                svcs = k8s_core.list_namespaced_service(ns)
            else:
                svcs = k8s_core.list_service_for_all_namespaces()
            return {"services": [{"name": s.metadata.name, "namespace": s.metadata.namespace, "type": s.spec.type, "cluster_ip": s.spec.cluster_ip} for s in svcs.items]}
        elif rt == "deployments":
            if ns:
                deps = apps_v1.list_namespaced_deployment(ns)
            else:
                deps = apps_v1.list_deployment_for_all_namespaces()
            return {"deployments": [{"name": d.metadata.name, "namespace": d.metadata.namespace, "replicas": d.status.replicas, "available_replicas": d.status.available_replicas} for d in deps.items]}
        elif rt == "nodes":
            nodes = k8s_core.list_node()
            return {"nodes": [{"name": n.metadata.name, "labels": n.metadata.labels, "status": n.status.conditions[-1].type if n.status.conditions else None} for n in nodes.items]}
        elif rt == "configmaps":
            if ns:
                cms = k8s_core.list_namespaced_config_map(ns)
            else:
                cms = k8s_core.list_config_map_for_all_namespaces()
            return {"configmaps": [{"name": cm.metadata.name, "namespace": cm.metadata.namespace} for cm in cms.items]}
        elif rt == "events":
            if ns:
                events = k8s_core.list_namespaced_event(ns)
            else:
                events = k8s_core.list_event_for_all_namespaces()
            return {"events": [{"name": e.metadata.name, "namespace": e.metadata.namespace, "type": e.type, "reason": e.reason, "message": e.message} for e in events.items]}
        elif rt == "secrets":
            if ns:
                secrets = k8s_core.list_namespaced_secret(ns)
            else:
                secrets = k8s_core.list_secret_for_all_namespaces()
            return {"secrets": [{"name": s.metadata.name, "namespace": s.metadata.namespace, "type": s.type} for s in secrets.items]}
        elif rt == "persistentvolumes":
            pvs = k8s_core.list_persistent_volume()
            return {"persistent_volumes": [{"name": pv.metadata.name, "capacity": pv.spec.capacity, "access_modes": pv.spec.access_modes, "status": pv.status.phase} for pv in pvs.items]}
        elif rt == "persistentvolumeclaims":
            if ns:
                pvcs = k8s_core.list_namespaced_persistent_volume_claim(ns)
            else:
                pvcs = k8s_core.list_persistent_volume_claim_for_all_namespaces()
            return {"persistent_volume_claims": [{"name": pvc.metadata.name, "namespace": pvc.metadata.namespace, "status": pvc.status.phase} for pvc in pvcs.items]}
        elif rt == "jobs":
            batch_v1 = client.BatchV1Api()
            if ns:
                jobs = batch_v1.list_namespaced_job(ns)
            else:
                jobs = batch_v1.list_job_for_all_namespaces()
            return {"jobs": [{"name": j.metadata.name, "namespace": j.metadata.namespace, "status": j.status.succeeded if j.status else None} for j in jobs.items]}
        elif rt == "cronjobs":
            batch_v1 = client.BatchV1Api()
            if ns:
                cronjobs = batch_v1.list_namespaced_cron_job(ns)
            else:
                cronjobs = batch_v1.list_cron_job_for_all_namespaces()
            return {"cronjobs": [{"name": cj.metadata.name, "namespace": cj.metadata.namespace, "schedule": cj.spec.schedule} for cj in cronjobs.items]}
        elif rt == "ingresses":
            if ns:
                ingresses = networking_v1.list_namespaced_ingress(ns)
            else:
                ingresses = networking_v1.list_ingress_for_all_namespaces()
            return {"ingresses": [{"name": ing.metadata.name, "namespace": ing.metadata.namespace, "hosts": [rule.host for rule in (ing.spec.rules or [])]} for ing in ingresses.items]}
        elif rt == "networkpolicies":
            if ns:
                nps = networking_v1.list_namespaced_network_policy(ns)
            else:
                nps = networking_v1.list_network_policy_for_all_namespaces()
            return {"network_policies": [{"name": np.metadata.name, "namespace": np.metadata.namespace} for np in nps.items]}
        elif rt == "statefulsets":
            if ns:
                sts = apps_v1.list_namespaced_stateful_set(ns)
            else:
                sts = apps_v1.list_stateful_set_for_all_namespaces()
            return {"statefulsets": [{"name": s.metadata.name, "namespace": s.metadata.namespace, "replicas": s.status.replicas, "ready_replicas": s.status.ready_replicas} for s in sts.items]}
        elif rt == "daemonsets":
            if ns:
                dss = apps_v1.list_namespaced_daemon_set(ns)
            else:
                dss = apps_v1.list_daemon_set_for_all_namespaces()
            return {"daemonsets": [{"name": ds.metadata.name, "namespace": ds.metadata.namespace, "desired_number_scheduled": ds.status.desired_number_scheduled, "number_ready": ds.status.number_ready} for ds in dss.items]}
        elif rt == "serviceaccounts":
            if ns:
                sas = k8s_core.list_namespaced_service_account(ns)
            else:
                sas = k8s_core.list_service_account_for_all_namespaces()
            return {"service_accounts": [{"name": sa.metadata.name, "namespace": sa.metadata.namespace} for sa in sas.items]}
        elif rt == "roles":
            rbac_v1 = client.RbacAuthorizationV1Api()
            if ns:
                roles = rbac_v1.list_namespaced_role(ns)
            else:
                roles = rbac_v1.list_role_for_all_namespaces()
            return {"roles": [{"name": r.metadata.name, "namespace": r.metadata.namespace} for r in roles.items]}
        elif rt == "rolebindings":
            rbac_v1 = client.RbacAuthorizationV1Api()
            if ns:
                rbs = rbac_v1.list_namespaced_role_binding(ns)
            else:
                rbs = rbac_v1.list_role_binding_for_all_namespaces()
            return {"role_bindings": [{"name": rb.metadata.name, "namespace": rb.metadata.namespace} for rb in rbs.items]}
        elif rt == "clusterroles":
            rbac_v1 = client.RbacAuthorizationV1Api()
            crs = rbac_v1.list_cluster_role()
            return {"cluster_roles": [{"name": cr.metadata.name} for cr in crs.items]}
        elif rt == "clusterrolebindings":
            rbac_v1 = client.RbacAuthorizationV1Api()
            crbs = rbac_v1.list_cluster_role_binding()
            return {"cluster_role_bindings": [{"name": crb.metadata.name} for crb in crbs.items]}
        else:
            return {"error": f"Unsupported resource_type: {params.resource_type}"}
    except Exception as e:
        logger.error(f"Error in list_resources: {e}")
        return {"error": str(e)}

class DescribeResourceParams(BaseModel):
    resource_type: str  # e.g., "pod", "service", "deployment", etc.
    name: str
    namespace: str = None

@mcp.tool("describe_resource")
def describe_resource(params: DescribeResourceParams) -> Dict[str, Any]:
    try:
        rt = params.resource_type.lower()
        ns = params.namespace
        name = params.name
        if rt == "pod":
            pod = k8s_core.read_namespaced_pod(name, ns)
            return {"name": pod.metadata.name, "namespace": pod.metadata.namespace, "labels": pod.metadata.labels, "annotations": pod.metadata.annotations, "status": pod.status.phase, "node": pod.spec.node_name, "containers": [c.name for c in pod.spec.containers]}
        elif rt == "service":
            svc = k8s_core.read_namespaced_service(name, ns)
            return {"name": svc.metadata.name, "namespace": svc.metadata.namespace, "labels": svc.metadata.labels, "annotations": svc.metadata.annotations, "type": svc.spec.type, "cluster_ip": svc.spec.cluster_ip, "ports": [{"port": p.port, "protocol": p.protocol, "target_port": p.target_port} for p in svc.spec.ports], "selector": svc.spec.selector}
        elif rt == "deployment":
            dep = apps_v1.read_namespaced_deployment(name, ns)
            return {"name": dep.metadata.name, "namespace": dep.metadata.namespace, "labels": dep.metadata.labels, "annotations": dep.metadata.annotations, "replicas": dep.status.replicas, "available_replicas": dep.status.available_replicas, "strategy": dep.spec.strategy.type, "containers": [c.name for c in dep.spec.template.spec.containers]}
        elif rt == "node":
            node = k8s_core.read_node(name)
            return {"name": node.metadata.name, "labels": node.metadata.labels, "annotations": node.metadata.annotations, "status": [{"type": c.type, "status": c.status, "reason": c.reason, "message": c.message} for c in node.status.conditions] if node.status.conditions else [], "addresses": [{"type": a.type, "address": a.address} for a in node.status.addresses] if node.status.addresses else []}
        elif rt == "configmap":
            cm = k8s_core.read_namespaced_config_map(name, ns)
            return {"name": cm.metadata.name, "namespace": cm.metadata.namespace, "labels": cm.metadata.labels, "annotations": cm.metadata.annotations, "data": cm.data}
        elif rt == "secret":
            s = k8s_core.read_namespaced_secret(name, ns)
            return {"name": s.metadata.name, "namespace": s.metadata.namespace, "type": s.type, "labels": s.metadata.labels, "annotations": s.metadata.annotations, "data_keys": list(s.data.keys()) if s.data else []}
        elif rt == "persistentvolume":
            pv = k8s_core.read_persistent_volume(name)
            return {"name": pv.metadata.name, "capacity": pv.spec.capacity, "access_modes": pv.spec.access_modes, "status": pv.status.phase, "labels": pv.metadata.labels, "annotations": pv.metadata.annotations}
        elif rt == "persistentvolumeclaim":
            pvc = k8s_core.read_namespaced_persistent_volume_claim(name, ns)
            return {"name": pvc.metadata.name, "namespace": pvc.metadata.namespace, "status": pvc.status.phase, "labels": pvc.metadata.labels, "annotations": pvc.metadata.annotations, "access_modes": pvc.spec.access_modes, "resources": pvc.spec.resources.requests}
        elif rt == "job":
            batch_v1 = client.BatchV1Api()
            job = batch_v1.read_namespaced_job(name, ns)
            return {"name": job.metadata.name, "namespace": job.metadata.namespace, "labels": job.metadata.labels, "annotations": job.metadata.annotations, "status": job.status.succeeded if job.status else None, "active": job.status.active if job.status else None, "conditions": [{"type": c.type, "status": c.status, "reason": c.reason, "message": c.message} for c in (job.status.conditions or [])]}
        elif rt == "cronjob":
            batch_v1 = client.BatchV1Api()
            cj = batch_v1.read_namespaced_cron_job(name, ns)
            return {"name": cj.metadata.name, "namespace": cj.metadata.namespace, "labels": cj.metadata.labels, "annotations": cj.metadata.annotations, "schedule": cj.spec.schedule, "suspend": cj.spec.suspend, "active": [a.name for a in (cj.status.active or [])]}
        elif rt == "ingress":
            ing = networking_v1.read_namespaced_ingress(name, ns)
            return {"name": ing.metadata.name, "namespace": ing.metadata.namespace, "labels": ing.metadata.labels, "annotations": ing.metadata.annotations, "hosts": [rule.host for rule in (ing.spec.rules or [])], "tls": [t.secret_name for t in (ing.spec.tls or [])]}
        elif rt == "networkpolicy":
            np = networking_v1.read_namespaced_network_policy(name, ns)
            return {"name": np.metadata.name, "namespace": np.metadata.namespace, "labels": np.metadata.labels, "annotations": np.metadata.annotations, "pod_selector": np.spec.pod_selector.match_labels if np.spec.pod_selector else {}, "policy_types": np.spec.policy_types}
        elif rt == "statefulset":
            sts = apps_v1.read_namespaced_stateful_set(name, ns)
            return {"name": sts.metadata.name, "namespace": sts.metadata.namespace, "labels": sts.metadata.labels, "annotations": sts.metadata.annotations, "replicas": sts.status.replicas, "ready_replicas": sts.status.ready_replicas, "containers": [c.name for c in sts.spec.template.spec.containers]}
        elif rt == "daemonset":
            ds = apps_v1.read_namespaced_daemon_set(name, ns)
            return {"name": ds.metadata.name, "namespace": ds.metadata.namespace, "labels": ds.metadata.labels, "annotations": ds.metadata.annotations, "desired_number_scheduled": ds.status.desired_number_scheduled, "number_ready": ds.status.number_ready, "containers": [c.name for c in ds.spec.template.spec.containers]}
        elif rt == "serviceaccount":
            sa = k8s_core.read_namespaced_service_account(name, ns)
            return {"name": sa.metadata.name, "namespace": sa.metadata.namespace, "labels": sa.metadata.labels, "annotations": sa.metadata.annotations, "secrets": [s.name for s in (sa.secrets or [])]}
        elif rt == "role":
            rbac_v1 = client.RbacAuthorizationV1Api()
            r = rbac_v1.read_namespaced_role(name, ns)
            return {"name": r.metadata.name, "namespace": r.metadata.namespace, "labels": r.metadata.labels, "annotations": r.metadata.annotations, "rules": [rule.to_dict() for rule in r.rules]}
        elif rt == "rolebinding":
            rbac_v1 = client.RbacAuthorizationV1Api()
            rb = rbac_v1.read_namespaced_role_binding(name, ns)
            return {"name": rb.metadata.name, "namespace": rb.metadata.namespace, "labels": rb.metadata.labels, "annotations": rb.metadata.annotations, "role_ref": rb.role_ref.to_dict(), "subjects": [s.to_dict() for s in (rb.subjects or [])]}
        elif rt == "clusterrole":
            rbac_v1 = client.RbacAuthorizationV1Api()
            cr = rbac_v1.read_cluster_role(name)
            return {"name": cr.metadata.name, "labels": cr.metadata.labels, "annotations": cr.metadata.annotations, "rules": [rule.to_dict() for rule in cr.rules]}
        elif rt == "clusterrolebinding":
            rbac_v1 = client.RbacAuthorizationV1Api()
            crb = rbac_v1.read_cluster_role_binding(name)
            return {"name": crb.metadata.name, "labels": crb.metadata.labels, "annotations": crb.metadata.annotations, "role_ref": crb.role_ref.to_dict(), "subjects": [s.to_dict() for s in (crb.subjects or [])]}
        else:
            return {"error": f"Unsupported resource_type: {params.resource_type}"}
    except Exception as e:
        logger.error(f"Error in describe_resource: {e}")
        return {"error": str(e)}

class ResourceActionParams(BaseModel):
    action: str  # e.g., "get_logs", "exec", "events"
    resource_type: str
    name: str = None
    namespace: str = None
    container: str = None
    tail_lines: int = 100
    command: list[str] = None

@mcp.tool("resource_action")
def resource_action(params: ResourceActionParams) -> dict:
    try:
        if params.action == "get_logs" and params.resource_type == "pod":
            logs = k8s_core.read_namespaced_pod_log(
                name=params.name,
                namespace=params.namespace,
                container=params.container,
                tail_lines=params.tail_lines
            )
            return {"logs": logs}
        elif params.action == "exec" and params.resource_type == "pod":
            if not params.command:
                return {"error": "command parameter is required for exec"}
            output = stream(
                k8s_core.connect_get_namespaced_pod_exec,
                params.name,
                params.namespace,
                command=params.command,
                container=params.container,
                stderr=True,
                stdin=False,
                stdout=True,
                tty=False
            )
            return {"output": output}
        elif params.action == "events":
            if params.namespace:
                events = k8s_core.list_namespaced_event(params.namespace)
            else:
                events = k8s_core.list_event_for_all_namespaces()
            return {"events": [
                {
                    "name": e.metadata.name,
                    "namespace": e.metadata.namespace,
                    "type": e.type,
                    "reason": e.reason,
                    "message": e.message
                } for e in events.items
            ]}
        else:
            return {"error": f"Unsupported action: {params.action} for resource_type: {params.resource_type}"}
    except Exception as e:
        logger.error(f"Error in resource_action: {e}")
        return {"error": str(e)}

def main():
    mcp.run()

if __name__ == "__main__":
    main() 