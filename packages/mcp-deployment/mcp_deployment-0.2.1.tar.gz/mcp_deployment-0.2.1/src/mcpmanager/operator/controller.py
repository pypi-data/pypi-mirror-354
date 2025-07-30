"""Kubernetes controller for MCPServer resources."""

import asyncio
import logging
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from .crd import MCPServerCRD, MCPServerSpec, MCPServerStatus, MCPServerPhase
from mcpmanager.core.models import MCPServerConfig, TransportType

logger = logging.getLogger(__name__)


class MCPServerController:
    """Controller for MCPServer custom resources."""

    def __init__(self, namespace: str = "default"):
        """Initialize controller."""
        self.namespace = namespace
        self.watched_resources: Dict[str, MCPServerCRD] = {}
        self._running = False

    async def run_command(self, cmd: List[str], input_data: Optional[str] = None) -> Dict[str, Any]:
        """Run kubectl command."""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE if input_data else None,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate(
                input=input_data.encode() if input_data else None
            )
            
            return {
                "returncode": process.returncode,
                "stdout": stdout.decode("utf-8", errors="replace"),
                "stderr": stderr.decode("utf-8", errors="replace")
            }
        except Exception as e:
            logger.error(f"Command failed: {' '.join(cmd)}: {e}")
            raise

    async def start(self) -> None:
        """Start the controller."""
        self._running = True
        logger.info(f"Starting MCPServer controller for namespace: {self.namespace}")
        
        # Start watching for MCPServer resources
        await asyncio.gather(
            self._watch_mcpservers(),
            self._reconcile_loop(),
        )

    async def stop(self) -> None:
        """Stop the controller."""
        self._running = False
        logger.info("Stopping MCPServer controller")

    async def _watch_mcpservers(self) -> None:
        """Watch for MCPServer resource changes."""
        while self._running:
            try:
                # Get current MCPServer resources
                result = await self.run_command([
                    "kubectl", "get", "mcpservers",
                    "-n", self.namespace,
                    "-o", "json"
                ])
                
                if result["returncode"] == 0:
                    try:
                        data = json.loads(result["stdout"])
                        current_resources = {}
                        
                        for item in data.get("items", []):
                            mcpserver = MCPServerCRD.from_dict(item)
                            name = mcpserver.metadata.get("name")
                            if name:
                                current_resources[name] = mcpserver
                        
                        # Detect changes
                        await self._handle_resource_changes(current_resources)
                        self.watched_resources = current_resources
                        
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse MCPServer list: {e}")
                
                # Wait before next poll
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"Error watching MCPServers: {e}")
                await asyncio.sleep(10)

    async def _handle_resource_changes(self, current_resources: Dict[str, MCPServerCRD]) -> None:
        """Handle changes in MCPServer resources."""
        # Find new or updated resources
        for name, resource in current_resources.items():
            if name not in self.watched_resources:
                logger.info(f"New MCPServer detected: {name}")
                await self._handle_mcpserver_added(resource)
            else:
                # Check if spec changed
                old_resource = self.watched_resources[name]
                if self._resource_spec_changed(old_resource, resource):
                    logger.info(f"MCPServer updated: {name}")
                    await self._handle_mcpserver_updated(resource)
        
        # Find deleted resources
        for name in self.watched_resources:
            if name not in current_resources:
                logger.info(f"MCPServer deleted: {name}")
                await self._handle_mcpserver_deleted(name)

    def _resource_spec_changed(self, old: MCPServerCRD, new: MCPServerCRD) -> bool:
        """Check if resource spec changed."""
        # Simple comparison - in production would use resource version
        return json.dumps(old.spec.__dict__ if old.spec else {}, sort_keys=True) != \
               json.dumps(new.spec.__dict__ if new.spec else {}, sort_keys=True)

    async def _handle_mcpserver_added(self, resource: MCPServerCRD) -> None:
        """Handle new MCPServer resource."""
        name = resource.metadata.get("name")
        if not name or not resource.spec:
            return
        
        try:
            # Create Kubernetes resources for MCP server
            await self._create_mcpserver_resources(resource)
            
            # Update status
            await self._update_status(name, MCPServerPhase.PENDING, "Creating resources")
            
        except Exception as e:
            logger.error(f"Failed to handle new MCPServer {name}: {e}")
            await self._update_status(name, MCPServerPhase.FAILED, f"Failed to create: {e}")

    async def _handle_mcpserver_updated(self, resource: MCPServerCRD) -> None:
        """Handle updated MCPServer resource."""
        name = resource.metadata.get("name")
        if not name or not resource.spec:
            return
        
        try:
            # Update Kubernetes resources
            await self._update_mcpserver_resources(resource)
            
            # Update status
            await self._update_status(name, MCPServerPhase.PENDING, "Updating resources")
            
        except Exception as e:
            logger.error(f"Failed to handle updated MCPServer {name}: {e}")
            await self._update_status(name, MCPServerPhase.FAILED, f"Failed to update: {e}")

    async def _handle_mcpserver_deleted(self, name: str) -> None:
        """Handle deleted MCPServer resource."""
        try:
            # Clean up Kubernetes resources
            await self._delete_mcpserver_resources(name)
            
        except Exception as e:
            logger.error(f"Failed to clean up MCPServer {name}: {e}")

    async def _create_mcpserver_resources(self, resource: MCPServerCRD) -> None:
        """Create Kubernetes resources for MCPServer."""
        name = resource.metadata.get("name")
        spec = resource.spec
        
        if not name or not spec:
            return
        
        # Create Deployment
        deployment = self._create_deployment_manifest(name, spec)
        deployment_yaml = json.dumps(deployment)
        
        result = await self.run_command([
            "kubectl", "apply", "-f", "-"
        ], input_data=deployment_yaml)
        
        if result["returncode"] != 0:
            raise Exception(f"Failed to create deployment: {result['stderr']}")
        
        # Create Service if needed
        if spec.transport in ["sse", "proxy"] and spec.port:
            service = self._create_service_manifest(name, spec)
            service_yaml = json.dumps(service)
            
            result = await self.run_command([
                "kubectl", "apply", "-f", "-"
            ], input_data=service_yaml)
            
            if result["returncode"] != 0:
                logger.warning(f"Failed to create service: {result['stderr']}")

    async def _update_mcpserver_resources(self, resource: MCPServerCRD) -> None:
        """Update Kubernetes resources for MCPServer."""
        # For simplicity, recreate resources
        name = resource.metadata.get("name")
        if name:
            await self._delete_mcpserver_resources(name)
            await self._create_mcpserver_resources(resource)

    async def _delete_mcpserver_resources(self, name: str) -> None:
        """Delete Kubernetes resources for MCPServer."""
        # Delete deployment
        await self.run_command([
            "kubectl", "delete", "deployment", f"mcpserver-{name}",
            "-n", self.namespace, "--ignore-not-found"
        ])
        
        # Delete service
        await self.run_command([
            "kubectl", "delete", "service", f"mcpserver-{name}",
            "-n", self.namespace, "--ignore-not-found"
        ])

    def _create_deployment_manifest(self, name: str, spec: MCPServerSpec) -> Dict[str, Any]:
        """Create deployment manifest for MCPServer."""
        container = {
            "name": "mcpserver",
            "image": spec.image,
            "securityContext": {
                "allowPrivilegeEscalation": False,
                "runAsNonRoot": True,
                "runAsUser": 1000,
                "capabilities": {"drop": ["ALL"]},
                "readOnlyRootFilesystem": False
            }
        }
        
        if spec.command:
            container["command"] = spec.command
        
        if spec.environment:
            container["env"] = [
                {"name": key, "value": value}
                for key, value in spec.environment.items()
            ]
        
        if spec.port:
            container["ports"] = [{
                "containerPort": spec.port,
                "protocol": "TCP"
            }]
        
        if spec.resources:
            container["resources"] = spec.resources
        
        # Volume mounts for permission profile
        volume_mounts = []
        volumes = []
        
        if spec.permission_profile:
            read_paths = spec.permission_profile.get("read", [])
            write_paths = spec.permission_profile.get("write", [])
            
            for i, path in enumerate(read_paths):
                source = path.split(":")[0] if ":" in path else path
                target = path.split(":")[1] if ":" in path else path
                
                volume_name = f"read-vol-{i}"
                volumes.append({
                    "name": volume_name,
                    "hostPath": {"path": source, "type": "DirectoryOrCreate"}
                })
                volume_mounts.append({
                    "name": volume_name,
                    "mountPath": target,
                    "readOnly": True
                })
            
            for i, path in enumerate(write_paths):
                source = path.split(":")[0] if ":" in path else path
                target = path.split(":")[1] if ":" in path else path
                
                volume_name = f"write-vol-{i}"
                volumes.append({
                    "name": volume_name,
                    "hostPath": {"path": source, "type": "DirectoryOrCreate"}
                })
                volume_mounts.append({
                    "name": volume_name,
                    "mountPath": target,
                    "readOnly": False
                })
        
        if volume_mounts:
            container["volumeMounts"] = volume_mounts
        
        pod_spec = {
            "containers": [container],
            "securityContext": {
                "runAsNonRoot": True,
                "runAsUser": 1000,
                "fsGroup": 1000
            },
            "restartPolicy": "Always"
        }
        
        if volumes:
            pod_spec["volumes"] = volumes
        
        if spec.node_selector:
            pod_spec["nodeSelector"] = spec.node_selector
        
        if spec.tolerations:
            pod_spec["tolerations"] = spec.tolerations
        
        if spec.affinity:
            pod_spec["affinity"] = spec.affinity
        
        return {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": f"mcpserver-{name}",
                "namespace": self.namespace,
                "labels": {
                    "app.kubernetes.io/name": "mcpserver",
                    "app.kubernetes.io/instance": name,
                    "app.kubernetes.io/managed-by": "mcpmanager-operator"
                },
                "ownerReferences": [{
                    "apiVersion": "mcpmanager.io/v1alpha1",
                    "kind": "MCPServer",
                    "name": name,
                    "uid": "placeholder",  # Would need actual UID
                    "controller": True
                }]
            },
            "spec": {
                "replicas": spec.replicas,
                "selector": {
                    "matchLabels": {
                        "app.kubernetes.io/name": "mcpserver",
                        "app.kubernetes.io/instance": name
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app.kubernetes.io/name": "mcpserver",
                            "app.kubernetes.io/instance": name,
                            "app.kubernetes.io/managed-by": "mcpmanager-operator"
                        }
                    },
                    "spec": pod_spec
                }
            }
        }

    def _create_service_manifest(self, name: str, spec: MCPServerSpec) -> Dict[str, Any]:
        """Create service manifest for MCPServer."""
        return {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": f"mcpserver-{name}",
                "namespace": self.namespace,
                "labels": {
                    "app.kubernetes.io/name": "mcpserver",
                    "app.kubernetes.io/instance": name,
                    "app.kubernetes.io/managed-by": "mcpmanager-operator"
                }
            },
            "spec": {
                "selector": {
                    "app.kubernetes.io/name": "mcpserver",
                    "app.kubernetes.io/instance": name
                },
                "ports": [{
                    "name": "mcp",
                    "port": spec.port,
                    "targetPort": spec.target_port or spec.port,
                    "protocol": "TCP"
                }],
                "type": "ClusterIP"
            }
        }

    async def _update_status(self, name: str, phase: MCPServerPhase, message: str = None) -> None:
        """Update MCPServer status."""
        try:
            # Get current resource
            result = await self.run_command([
                "kubectl", "get", "mcpserver", name,
                "-n", self.namespace,
                "-o", "json"
            ])
            
            if result["returncode"] != 0:
                return
            
            resource_data = json.loads(result["stdout"])
            resource = MCPServerCRD.from_dict(resource_data)
            
            # Update status
            resource.status.phase = phase.value
            resource.status.message = message
            resource.status.last_updated = datetime.now(timezone.utc).isoformat()
            
            # Get deployment status for replica counts
            if phase in [MCPServerPhase.RUNNING, MCPServerPhase.PENDING]:
                deploy_result = await self.run_command([
                    "kubectl", "get", "deployment", f"mcpserver-{name}",
                    "-n", self.namespace,
                    "-o", "json"
                ])
                
                if deploy_result["returncode"] == 0:
                    deploy_data = json.loads(deploy_result["stdout"])
                    status = deploy_data.get("status", {})
                    resource.status.replicas = status.get("replicas", 0)
                    resource.status.ready_replicas = status.get("readyReplicas", 0)
            
            # Update status subresource
            status_patch = {
                "status": {
                    "phase": resource.status.phase,
                    "message": resource.status.message,
                    "ready_replicas": resource.status.ready_replicas,
                    "replicas": resource.status.replicas,
                    "last_updated": resource.status.last_updated
                }
            }
            
            patch_data = json.dumps(status_patch)
            await self.run_command([
                "kubectl", "patch", "mcpserver", name,
                "-n", self.namespace,
                "--subresource=status",
                "--type=merge",
                "-p", patch_data
            ])
            
        except Exception as e:
            logger.error(f"Failed to update status for {name}: {e}")

    async def _reconcile_loop(self) -> None:
        """Reconciliation loop to ensure desired state."""
        while self._running:
            try:
                await self._reconcile_all()
                await asyncio.sleep(30)  # Reconcile every 30 seconds
            except Exception as e:
                logger.error(f"Error in reconcile loop: {e}")
                await asyncio.sleep(60)

    async def _reconcile_all(self) -> None:
        """Reconcile all MCPServer resources."""
        for name, resource in self.watched_resources.items():
            try:
                await self._reconcile_mcpserver(name, resource)
            except Exception as e:
                logger.error(f"Failed to reconcile MCPServer {name}: {e}")

    async def _reconcile_mcpserver(self, name: str, resource: MCPServerCRD) -> None:
        """Reconcile single MCPServer resource."""
        if not resource.spec:
            return
        
        # Check deployment status
        result = await self.run_command([
            "kubectl", "get", "deployment", f"mcpserver-{name}",
            "-n", self.namespace,
            "-o", "json"
        ])
        
        if result["returncode"] != 0:
            # Deployment doesn't exist, create it
            await self._create_mcpserver_resources(resource)
            return
        
        try:
            deploy_data = json.loads(result["stdout"])
            status = deploy_data.get("status", {})
            
            ready_replicas = status.get("readyReplicas", 0)
            replicas = status.get("replicas", 0)
            
            if ready_replicas == replicas and replicas > 0:
                await self._update_status(name, MCPServerPhase.RUNNING, "All replicas ready")
            elif replicas > 0:
                await self._update_status(name, MCPServerPhase.PENDING, "Waiting for replicas")
            else:
                await self._update_status(name, MCPServerPhase.FAILED, "No replicas")
                
        except json.JSONDecodeError:
            logger.error(f"Failed to parse deployment status for {name}")