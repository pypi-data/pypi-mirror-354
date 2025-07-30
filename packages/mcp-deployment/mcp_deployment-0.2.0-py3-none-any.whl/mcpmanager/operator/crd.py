"""Custom Resource Definitions for MCPManager operator."""

import yaml
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

from mcpmanager.core.models import TransportType, SecretsProvider


class MCPServerPhase(str, Enum):
    """MCP Server lifecycle phases."""
    PENDING = "Pending"
    RUNNING = "Running"
    FAILED = "Failed"
    SUCCEEDED = "Succeeded"


@dataclass
class MCPServerSpec:
    """MCP Server specification."""
    image: str
    description: Optional[str] = None
    version: Optional[str] = None
    tags: List[str] = None
    transport: str = "stdio"
    port: Optional[int] = None
    target_port: Optional[int] = None
    command: List[str] = None
    environment: Dict[str, str] = None
    secrets: List[Dict[str, str]] = None
    permission_profile: Optional[Dict[str, Any]] = None
    verification: Optional[Dict[str, Any]] = None
    replicas: int = 1
    resources: Optional[Dict[str, Any]] = None
    node_selector: Optional[Dict[str, str]] = None
    tolerations: List[Dict[str, Any]] = None
    affinity: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.tags is None:
            self.tags = []
        if self.command is None:
            self.command = []
        if self.environment is None:
            self.environment = {}
        if self.secrets is None:
            self.secrets = []
        if self.tolerations is None:
            self.tolerations = []


@dataclass
class MCPServerStatus:
    """MCP Server status."""
    phase: str = MCPServerPhase.PENDING.value
    message: Optional[str] = None
    ready_replicas: int = 0
    replicas: int = 0
    conditions: List[Dict[str, Any]] = None
    last_updated: Optional[str] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.conditions is None:
            self.conditions = []


@dataclass
class MCPServerCRD:
    """MCP Server Custom Resource Definition."""
    api_version: str = "mcpmanager.io/v1alpha1"
    kind: str = "MCPServer"
    metadata: Dict[str, Any] = None
    spec: MCPServerSpec = None
    status: MCPServerStatus = None

    def __post_init__(self):
        """Initialize default values."""
        if self.metadata is None:
            self.metadata = {}
        if self.status is None:
            self.status = MCPServerStatus()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for Kubernetes."""
        result = {
            "apiVersion": self.api_version,
            "kind": self.kind,
            "metadata": self.metadata,
        }
        
        if self.spec:
            result["spec"] = asdict(self.spec)
            # Remove None values
            result["spec"] = {k: v for k, v in result["spec"].items() if v is not None}
        
        if self.status:
            result["status"] = asdict(self.status)
            # Remove None values
            result["status"] = {k: v for k, v in result["status"].items() if v is not None}
        
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPServerCRD":
        """Create from dictionary."""
        metadata = data.get("metadata", {})
        spec_data = data.get("spec", {})
        status_data = data.get("status", {})
        
        spec = MCPServerSpec(**spec_data) if spec_data else None
        status = MCPServerStatus(**status_data) if status_data else MCPServerStatus()
        
        return cls(
            api_version=data.get("apiVersion", "mcpmanager.io/v1alpha1"),
            kind=data.get("kind", "MCPServer"),
            metadata=metadata,
            spec=spec,
            status=status
        )


def create_crd_manifest() -> Dict[str, Any]:
    """Create the CRD manifest for MCPServer."""
    return {
        "apiVersion": "apiextensions.k8s.io/v1",
        "kind": "CustomResourceDefinition",
        "metadata": {
            "name": "mcpservers.mcpmanager.io",
            "labels": {
                "app.kubernetes.io/name": "mcpmanager",
                "app.kubernetes.io/component": "operator"
            }
        },
        "spec": {
            "group": "mcpmanager.io",
            "versions": [{
                "name": "v1alpha1",
                "served": True,
                "storage": True,
                "schema": {
                    "openAPIV3Schema": {
                        "type": "object",
                        "properties": {
                            "spec": {
                                "type": "object",
                                "properties": {
                                    "image": {
                                        "type": "string",
                                        "description": "Container image for the MCP server"
                                    },
                                    "description": {
                                        "type": "string",
                                        "description": "Description of the MCP server"
                                    },
                                    "version": {
                                        "type": "string",
                                        "description": "Version of the MCP server"
                                    },
                                    "tags": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Tags for categorizing the server"
                                    },
                                    "transport": {
                                        "type": "string",
                                        "enum": ["stdio", "sse", "proxy", "transparent"],
                                        "default": "stdio",
                                        "description": "Transport protocol"
                                    },
                                    "port": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 65535,
                                        "description": "Port for network transports"
                                    },
                                    "target_port": {
                                        "type": "integer",
                                        "minimum": 1,
                                        "maximum": 65535,
                                        "description": "Target port in container"
                                    },
                                    "command": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                        "description": "Command to run in container"
                                    },
                                    "environment": {
                                        "type": "object",
                                        "additionalProperties": {"type": "string"},
                                        "description": "Environment variables"
                                    },
                                    "secrets": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "name": {"type": "string"},
                                                "target": {"type": "string"}
                                            },
                                            "required": ["name", "target"]
                                        },
                                        "description": "Secret references"
                                    },
                                    "permission_profile": {
                                        "type": "object",
                                        "properties": {
                                            "read": {
                                                "type": "array",
                                                "items": {"type": "string"}
                                            },
                                            "write": {
                                                "type": "array", 
                                                "items": {"type": "string"}
                                            },
                                            "network": {
                                                "type": "object",
                                                "additionalProperties": True
                                            }
                                        },
                                        "description": "Permission profile for container"
                                    },
                                    "verification": {
                                        "type": "object",
                                        "description": "Image verification settings"
                                    },
                                    "replicas": {
                                        "type": "integer",
                                        "minimum": 0,
                                        "maximum": 100,
                                        "default": 1,
                                        "description": "Number of replicas"
                                    },
                                    "resources": {
                                        "type": "object",
                                        "properties": {
                                            "limits": {
                                                "type": "object",
                                                "additionalProperties": {"type": "string"}
                                            },
                                            "requests": {
                                                "type": "object", 
                                                "additionalProperties": {"type": "string"}
                                            }
                                        },
                                        "description": "Resource requirements"
                                    },
                                    "node_selector": {
                                        "type": "object",
                                        "additionalProperties": {"type": "string"},
                                        "description": "Node selector"
                                    },
                                    "tolerations": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "key": {"type": "string"},
                                                "operator": {"type": "string"},
                                                "value": {"type": "string"},
                                                "effect": {"type": "string"},
                                                "tolerationSeconds": {"type": "integer"}
                                            }
                                        },
                                        "description": "Tolerations"
                                    },
                                    "affinity": {
                                        "type": "object",
                                        "description": "Pod affinity rules"
                                    }
                                },
                                "required": ["image"]
                            },
                            "status": {
                                "type": "object",
                                "properties": {
                                    "phase": {
                                        "type": "string",
                                        "enum": ["Pending", "Running", "Failed", "Succeeded"],
                                        "description": "Current phase"
                                    },
                                    "message": {
                                        "type": "string",
                                        "description": "Human readable message"
                                    },
                                    "ready_replicas": {
                                        "type": "integer",
                                        "minimum": 0,
                                        "description": "Number of ready replicas"
                                    },
                                    "replicas": {
                                        "type": "integer",
                                        "minimum": 0,
                                        "description": "Total number of replicas"
                                    },
                                    "conditions": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "properties": {
                                                "type": {"type": "string"},
                                                "status": {"type": "string"},
                                                "lastTransitionTime": {"type": "string"},
                                                "reason": {"type": "string"},
                                                "message": {"type": "string"}
                                            },
                                            "required": ["type", "status"]
                                        },
                                        "description": "Conditions"
                                    },
                                    "last_updated": {
                                        "type": "string",
                                        "format": "date-time",
                                        "description": "Last update timestamp"
                                    }
                                }
                            }
                        }
                    }
                },
                "subresources": {
                    "status": {}
                },
                "additionalPrinterColumns": [
                    {
                        "name": "Phase",
                        "type": "string",
                        "description": "Current phase",
                        "jsonPath": ".status.phase"
                    },
                    {
                        "name": "Image",
                        "type": "string", 
                        "description": "Container image",
                        "jsonPath": ".spec.image"
                    },
                    {
                        "name": "Transport",
                        "type": "string",
                        "description": "Transport protocol",
                        "jsonPath": ".spec.transport"
                    },
                    {
                        "name": "Ready",
                        "type": "string",
                        "description": "Ready replicas",
                        "jsonPath": ".status.ready_replicas"
                    },
                    {
                        "name": "Age",
                        "type": "date",
                        "description": "Creation time",
                        "jsonPath": ".metadata.creationTimestamp"
                    }
                ]
            }],
            "scope": "Namespaced",
            "names": {
                "plural": "mcpservers",
                "singular": "mcpserver", 
                "kind": "MCPServer",
                "shortNames": ["mcps"]
            }
        }
    }


def create_rbac_manifests(namespace: str = "mcpmanager-system") -> List[Dict[str, Any]]:
    """Create RBAC manifests for the operator."""
    service_account = {
        "apiVersion": "v1",
        "kind": "ServiceAccount",
        "metadata": {
            "name": "mcpmanager-operator",
            "namespace": namespace
        }
    }
    
    cluster_role = {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "ClusterRole",
        "metadata": {
            "name": "mcpmanager-operator"
        },
        "rules": [
            {
                "apiGroups": ["mcpmanager.io"],
                "resources": ["mcpservers"],
                "verbs": ["get", "list", "watch", "create", "update", "patch", "delete"]
            },
            {
                "apiGroups": ["mcpmanager.io"],
                "resources": ["mcpservers/status"],
                "verbs": ["get", "update", "patch"]
            },
            {
                "apiGroups": [""],
                "resources": ["pods", "services", "configmaps", "secrets"],
                "verbs": ["get", "list", "watch", "create", "update", "patch", "delete"]
            },
            {
                "apiGroups": ["apps"],
                "resources": ["deployments", "replicasets"],
                "verbs": ["get", "list", "watch", "create", "update", "patch", "delete"]
            },
            {
                "apiGroups": [""],
                "resources": ["events"],
                "verbs": ["create", "patch"]
            }
        ]
    }
    
    cluster_role_binding = {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "ClusterRoleBinding",
        "metadata": {
            "name": "mcpmanager-operator"
        },
        "roleRef": {
            "apiGroup": "rbac.authorization.k8s.io",
            "kind": "ClusterRole",
            "name": "mcpmanager-operator"
        },
        "subjects": [
            {
                "kind": "ServiceAccount",
                "name": "mcpmanager-operator",
                "namespace": namespace
            }
        ]
    }
    
    return [service_account, cluster_role, cluster_role_binding]


def create_operator_deployment(
    namespace: str = "mcpmanager-system",
    image: str = "mcpmanager/operator:latest"
) -> Dict[str, Any]:
    """Create operator deployment manifest."""
    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {
            "name": "mcpmanager-operator",
            "namespace": namespace,
            "labels": {
                "app.kubernetes.io/name": "mcpmanager",
                "app.kubernetes.io/component": "operator"
            }
        },
        "spec": {
            "replicas": 1,
            "selector": {
                "matchLabels": {
                    "app.kubernetes.io/name": "mcpmanager",
                    "app.kubernetes.io/component": "operator"
                }
            },
            "template": {
                "metadata": {
                    "labels": {
                        "app.kubernetes.io/name": "mcpmanager",
                        "app.kubernetes.io/component": "operator"
                    }
                },
                "spec": {
                    "serviceAccountName": "mcpmanager-operator",
                    "containers": [
                        {
                            "name": "operator",
                            "image": image,
                            "command": ["mcpm", "operator", "run"],
                            "env": [
                                {
                                    "name": "WATCH_NAMESPACE",
                                    "valueFrom": {
                                        "fieldRef": {
                                            "fieldPath": "metadata.namespace"
                                        }
                                    }
                                },
                                {
                                    "name": "POD_NAME",
                                    "valueFrom": {
                                        "fieldRef": {
                                            "fieldPath": "metadata.name"
                                        }
                                    }
                                },
                                {
                                    "name": "OPERATOR_NAME",
                                    "value": "mcpmanager-operator"
                                }
                            ],
                            "resources": {
                                "limits": {
                                    "cpu": "500m",
                                    "memory": "512Mi"
                                },
                                "requests": {
                                    "cpu": "100m",
                                    "memory": "128Mi"
                                }
                            },
                            "securityContext": {
                                "allowPrivilegeEscalation": False,
                                "runAsNonRoot": True,
                                "runAsUser": 1000,
                                "capabilities": {
                                    "drop": ["ALL"]
                                }
                            }
                        }
                    ],
                    "securityContext": {
                        "runAsNonRoot": True,
                        "runAsUser": 1000,
                        "fsGroup": 1000
                    }
                }
            }
        }
    }