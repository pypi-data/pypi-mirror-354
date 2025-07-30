"""Main operator implementation."""

import asyncio
import logging
import os
import signal
import sys
from typing import Optional

from .controller import MCPServerController
from .crd import create_crd_manifest, create_rbac_manifests, create_operator_deployment

logger = logging.getLogger(__name__)


class MCPOperator:
    """Main MCPManager Kubernetes operator."""

    def __init__(self, namespace: str = None):
        """Initialize operator."""
        self.namespace = namespace or os.getenv("WATCH_NAMESPACE", "default")
        self.controller = MCPServerController(self.namespace)
        self._running = False

    async def start(self) -> None:
        """Start the operator."""
        logger.info(f"Starting MCPManager operator in namespace: {self.namespace}")
        self._running = True
        
        # Setup signal handlers
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down...")
            asyncio.create_task(self.stop())
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        try:
            # Start controller
            await self.controller.start()
        except Exception as e:
            logger.error(f"Operator failed: {e}")
            sys.exit(1)

    async def stop(self) -> None:
        """Stop the operator."""
        if not self._running:
            return
        
        logger.info("Stopping MCPManager operator")
        self._running = False
        
        # Stop controller
        await self.controller.stop()
        
        # Exit
        sys.exit(0)

    async def install_crds(self) -> None:
        """Install Custom Resource Definitions."""
        logger.info("Installing MCPServer CRD")
        
        try:
            # Create CRD manifest
            crd_manifest = create_crd_manifest()
            
            # Apply CRD
            import json
            import subprocess
            
            crd_yaml = json.dumps(crd_manifest)
            process = await asyncio.create_subprocess_exec(
                "kubectl", "apply", "-f", "-",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate(input=crd_yaml.encode())
            
            if process.returncode != 0:
                raise Exception(f"Failed to install CRD: {stderr.decode()}")
            
            logger.info("MCPServer CRD installed successfully")
            
        except Exception as e:
            logger.error(f"Failed to install CRDs: {e}")
            raise

    async def install_rbac(self, namespace: str = "mcpmanager-system") -> None:
        """Install RBAC resources."""
        logger.info(f"Installing RBAC resources in namespace: {namespace}")
        
        try:
            # Create namespace first
            namespace_manifest = {
                "apiVersion": "v1",
                "kind": "Namespace",
                "metadata": {
                    "name": namespace,
                    "labels": {
                        "app.kubernetes.io/name": "mcpmanager",
                        "app.kubernetes.io/component": "operator"
                    }
                }
            }
            
            await self._apply_manifest(namespace_manifest)
            
            # Create RBAC manifests
            rbac_manifests = create_rbac_manifests(namespace)
            
            for manifest in rbac_manifests:
                await self._apply_manifest(manifest)
            
            logger.info("RBAC resources installed successfully")
            
        except Exception as e:
            logger.error(f"Failed to install RBAC: {e}")
            raise

    async def install_operator(
        self, 
        namespace: str = "mcpmanager-system",
        image: str = "mcpmanager/operator:latest"
    ) -> None:
        """Install operator deployment."""
        logger.info(f"Installing operator deployment in namespace: {namespace}")
        
        try:
            # Create operator deployment
            deployment_manifest = create_operator_deployment(namespace, image)
            await self._apply_manifest(deployment_manifest)
            
            logger.info("Operator deployment installed successfully")
            
        except Exception as e:
            logger.error(f"Failed to install operator: {e}")
            raise

    async def _apply_manifest(self, manifest: dict) -> None:
        """Apply a Kubernetes manifest."""
        import json
        
        manifest_yaml = json.dumps(manifest)
        process = await asyncio.create_subprocess_exec(
            "kubectl", "apply", "-f", "-",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate(input=manifest_yaml.encode())
        
        if process.returncode != 0:
            raise Exception(f"Failed to apply manifest: {stderr.decode()}")

    async def uninstall(self) -> None:
        """Uninstall operator and CRDs."""
        logger.info("Uninstalling MCPManager operator")
        
        try:
            # Delete operator deployment
            await asyncio.create_subprocess_exec(
                "kubectl", "delete", "deployment", "mcpmanager-operator",
                "-n", "mcpmanager-system", "--ignore-not-found"
            )
            
            # Delete RBAC
            await asyncio.create_subprocess_exec(
                "kubectl", "delete", "clusterrolebinding", "mcpmanager-operator",
                "--ignore-not-found"
            )
            
            await asyncio.create_subprocess_exec(
                "kubectl", "delete", "clusterrole", "mcpmanager-operator",
                "--ignore-not-found"
            )
            
            await asyncio.create_subprocess_exec(
                "kubectl", "delete", "serviceaccount", "mcpmanager-operator",
                "-n", "mcpmanager-system", "--ignore-not-found"
            )
            
            # Delete namespace
            await asyncio.create_subprocess_exec(
                "kubectl", "delete", "namespace", "mcpmanager-system",
                "--ignore-not-found"
            )
            
            # Delete CRD (this will delete all MCPServer resources!)
            await asyncio.create_subprocess_exec(
                "kubectl", "delete", "crd", "mcpservers.mcpmanager.io",
                "--ignore-not-found"
            )
            
            logger.info("Operator uninstalled successfully")
            
        except Exception as e:
            logger.error(f"Failed to uninstall operator: {e}")
            raise

    async def status(self) -> dict:
        """Get operator status."""
        status = {
            "operator": "unknown",
            "crd": "unknown",
            "rbac": "unknown",
            "mcpservers": []
        }
        
        try:
            # Check CRD
            process = await asyncio.create_subprocess_exec(
                "kubectl", "get", "crd", "mcpservers.mcpmanager.io",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            status["crd"] = "installed" if process.returncode == 0 else "missing"
            
            # Check operator deployment
            process = await asyncio.create_subprocess_exec(
                "kubectl", "get", "deployment", "mcpmanager-operator",
                "-n", "mcpmanager-system",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            status["operator"] = "running" if process.returncode == 0 else "missing"
            
            # Check RBAC
            process = await asyncio.create_subprocess_exec(
                "kubectl", "get", "clusterrole", "mcpmanager-operator",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            status["rbac"] = "installed" if process.returncode == 0 else "missing"
            
            # List MCPServers
            if status["crd"] == "installed":
                process = await asyncio.create_subprocess_exec(
                    "kubectl", "get", "mcpservers", "--all-namespaces",
                    "-o", "json",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                
                if process.returncode == 0:
                    import json
                    try:
                        data = json.loads(stdout.decode())
                        for item in data.get("items", []):
                            metadata = item.get("metadata", {})
                            spec = item.get("spec", {})
                            status_info = item.get("status", {})
                            
                            status["mcpservers"].append({
                                "name": metadata.get("name"),
                                "namespace": metadata.get("namespace"),
                                "image": spec.get("image"),
                                "phase": status_info.get("phase", "Unknown"),
                                "ready_replicas": status_info.get("ready_replicas", 0),
                                "replicas": status_info.get("replicas", 0)
                            })
                    except json.JSONDecodeError:
                        pass
        
        except Exception as e:
            logger.error(f"Failed to get operator status: {e}")
        
        return status

    async def validate_environment(self) -> bool:
        """Validate that the environment is ready for operator."""
        logger.info("Validating environment for operator")
        
        try:
            # Check kubectl availability
            process = await asyncio.create_subprocess_exec(
                "kubectl", "version", "--client",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            
            if process.returncode != 0:
                logger.error("kubectl not available")
                return False
            
            # Check cluster access
            process = await asyncio.create_subprocess_exec(
                "kubectl", "cluster-info",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            
            if process.returncode != 0:
                logger.error("Cannot access Kubernetes cluster")
                return False
            
            # Check permissions
            process = await asyncio.create_subprocess_exec(
                "kubectl", "auth", "can-i", "create", "customresourcedefinitions",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0 or "yes" not in stdout.decode().lower():
                logger.error("Insufficient permissions to install CRDs")
                return False
            
            logger.info("Environment validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Environment validation failed: {e}")
            return False