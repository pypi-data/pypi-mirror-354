from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

from . import __package__ as tool_name
from . import __version__ as tool_version


@dataclass
class Property:
    name: str
    value: str

    def __json__(self) -> dict:
        return {
            "name": self.name,
            "value": self.value,
        }

    def __lt__(self, other: "Property") -> bool:
        return isinstance(other, Property) and self.name < other.name


@dataclass
class Hash:
    alg: str
    content: str

    def __json__(self) -> dict:
        return {
            "alg": self.alg,
            "content": self.content,
        }

    def __lt__(self, other: "Hash") -> bool:
        return isinstance(other, Hash) and self.alg < other.alg


@dataclass
class ExternalReference:
    type: str
    url: str
    hashes: List[Hash] = field(default_factory=list)

    def __json__(self) -> dict:
        return {
            "type": self.type,
            "url": self.url,
            **({"hashes": [h.__json__() for h in sorted(self.hashes)]} if self.hashes else {}),
        }

    def __lt__(self, other: "ExternalReference") -> bool:
        return isinstance(other, ExternalReference) and (self.type, self.url) < (other.type, other.url)


@dataclass
class License:
    name: str

    def __json__(self) -> dict:
        return {"license": {"name": self.name}}

    def __lt__(self, other: "License") -> bool:
        return isinstance(other, License) and self.name < other.name


@dataclass
class Component:
    name: str
    type: str = "library"
    bom_ref: str = field(default_factory=lambda: str(uuid4()))
    purl: Optional[str] = None
    cpe: Optional[str] = None
    version: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    licenses: List[License] = field(default_factory=list)
    external_references: List[ExternalReference] = field(default_factory=list)
    hashes: List[Hash] = field(default_factory=list)
    properties: List[Property] = field(default_factory=list)

    def __json__(self) -> Dict:
        return {
            "type": self.type,
            "bom-ref": self.bom_ref,
            "name": self.name,
            **({"purl": self.purl} if self.purl else {}),
            **({"cpe": self.cpe} if self.cpe else {}),
            **({"version": self.version} if self.version else {}),
            **({"description": self.description} if self.description else {}),
            **({"authors": [{"name": self.author}]} if self.author else {}),
            **({"hashes": [h.__json__() for h in sorted(self.hashes)]} if self.hashes else {}),
            **({"licenses": [lic.__json__() for lic in sorted(self.licenses)]} if self.licenses else {}),
            **(
                {"externalReferences": [ref.__json__() for ref in sorted(self.external_references)]}
                if self.external_references
                else {}
            ),
            **({"properties": [prop.__json__() for prop in sorted(self.properties)]} if self.properties else {}),
        }

    def __lt__(self, other: "Component") -> bool:
        return isinstance(other, Component) and self.bom_ref < other.bom_ref


@dataclass
class Dependency:
    ref: str
    depends_on: List[str] = field(default_factory=list)

    def __json__(self) -> dict:
        return {
            "ref": self.ref,
            **({"dependsOn": sorted(self.depends_on)} if self.depends_on else {}),
        }

    def __lt__(self, other: "Dependency") -> bool:
        return isinstance(other, Dependency) and self.ref < other.ref


@dataclass
class Metadata:
    component: Component = field(default_factory=lambda: Component(bom_ref="pkg:conan/unknown", name="unknown"))
    tools: List[Component] = field(
        default_factory=lambda: [
            Component(type="application", name=tool_name or "", author="Dynatrace LLC", version=tool_version)
        ]
    )
    timestamp = datetime.now(tz=timezone.utc)

    def __json__(self) -> dict:
        return {
            "component": self.component.__json__(),
            "tools": {"components": [tool.__json__() for tool in sorted(self.tools)]},
            "timestamp": str(self.timestamp),
        }


@dataclass
class CycloneDxBom:
    bom_format = "CycloneDX"
    spec_version = "1.6"
    version = 1
    serial_number: str = field(default_factory=lambda: str(uuid4()))
    metadata: Metadata = field(default_factory=Metadata)
    components: List[Component] = field(default_factory=list)
    dependencies: List[Dependency] = field(default_factory=list)

    def add_component(self, component: Component) -> None:
        self.components.append(component)

    def add_dependency(self, dependency: Dependency) -> None:
        self.dependencies.append(dependency)

    def __json__(self) -> dict:
        return {
            "bomFormat": self.bom_format,
            "specVersion": self.spec_version,
            "version": self.version,
            "serialNumber": f"urn:uuid:{self.serial_number}",
            "metadata": self.metadata.__json__(),
            "components": [component.__json__() for component in sorted(self.components)],
            "dependencies": [dep.__json__() for dep in sorted(self.dependencies)],
        }
