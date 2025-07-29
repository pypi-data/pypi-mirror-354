# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .admission_level import AdmissionLevel
from .environment_phase import EnvironmentPhase
from .environment_initializer_param import EnvironmentInitializerParam

__all__ = [
    "EnvironmentSpecParam",
    "AutomationsFile",
    "Content",
    "Devcontainer",
    "DevcontainerDotfiles",
    "Machine",
    "Port",
    "Secret",
    "SSHPublicKey",
    "Timeout",
]


class AutomationsFile(TypedDict, total=False):
    automations_file_path: Annotated[str, PropertyInfo(alias="automationsFilePath")]
    """
    automations_file_path is the path to the automations file that is applied in the
    environment, relative to the repo root. path must not be absolute (start with a
    /):

    ```
    this.matches('^$|^[^/].*')
    ```
    """

    session: str


class Content(TypedDict, total=False):
    git_email: Annotated[str, PropertyInfo(alias="gitEmail")]
    """The Git email address"""

    git_username: Annotated[str, PropertyInfo(alias="gitUsername")]
    """The Git username"""

    initializer: EnvironmentInitializerParam
    """initializer configures how the environment is to be initialized"""

    session: str


class DevcontainerDotfiles(TypedDict, total=False):
    repository: Required[str]
    """URL of a dotfiles Git repository (e.g. https://github.com/owner/repository)"""


class Devcontainer(TypedDict, total=False):
    default_devcontainer_image: Annotated[str, PropertyInfo(alias="defaultDevcontainerImage")]
    """
    default_devcontainer_image is the default image that is used to start the
    devcontainer if no devcontainer config file is found
    """

    devcontainer_file_path: Annotated[str, PropertyInfo(alias="devcontainerFilePath")]
    """
    devcontainer_file_path is the path to the devcontainer file relative to the repo
    root path must not be absolute (start with a /):

    ```
    this.matches('^$|^[^/].*')
    ```
    """

    dotfiles: DevcontainerDotfiles
    """Experimental: dotfiles is the dotfiles configuration of the devcontainer"""

    session: str


_MachineReservedKeywords = TypedDict(
    "_MachineReservedKeywords",
    {
        "class": str,
    },
    total=False,
)


class Machine(_MachineReservedKeywords, total=False):
    session: str


class Port(TypedDict, total=False):
    admission: AdmissionLevel
    """policy of this port"""

    name: str
    """name of this port"""

    port: int
    """port number"""


class Secret(TypedDict, total=False):
    id: str
    """id is the unique identifier of the secret."""

    container_registry_basic_auth_host: Annotated[str, PropertyInfo(alias="containerRegistryBasicAuthHost")]
    """
    container_registry_basic_auth_host is the hostname of the container registry
    that supports basic auth
    """

    environment_variable: Annotated[str, PropertyInfo(alias="environmentVariable")]

    file_path: Annotated[str, PropertyInfo(alias="filePath")]
    """file_path is the path inside the devcontainer where the secret is mounted"""

    git_credential_host: Annotated[str, PropertyInfo(alias="gitCredentialHost")]

    name: str
    """name is the human readable description of the secret"""

    session: str
    """
    session indicated the current session of the secret. When the session does not
    change, secrets are not reloaded in the environment.
    """

    source: str
    """source is the source of the secret, for now control-plane or runner"""

    source_ref: Annotated[str, PropertyInfo(alias="sourceRef")]
    """source_ref into the source, in case of control-plane this is uuid of the secret"""


class SSHPublicKey(TypedDict, total=False):
    id: str
    """id is the unique identifier of the public key"""

    value: str
    """value is the actual public key in the public key file format"""


class Timeout(TypedDict, total=False):
    disconnected: str
    """
    inacitivity is the maximum time of disconnection before the environment is
    stopped or paused. Minimum duration is 30 minutes. Set to 0 to disable.
    """


class EnvironmentSpecParam(TypedDict, total=False):
    admission: AdmissionLevel
    """admission controlls who can access the environment and its ports."""

    automations_file: Annotated[AutomationsFile, PropertyInfo(alias="automationsFile")]
    """automations_file is the automations file spec of the environment"""

    content: Content
    """content is the content spec of the environment"""

    desired_phase: Annotated[EnvironmentPhase, PropertyInfo(alias="desiredPhase")]
    """Phase is the desired phase of the environment"""

    devcontainer: Devcontainer
    """devcontainer is the devcontainer spec of the environment"""

    machine: Machine
    """machine is the machine spec of the environment"""

    ports: Iterable[Port]
    """ports is the set of ports which ought to be exposed to the internet"""

    secrets: Iterable[Secret]
    """secrets are confidential data that is mounted into the environment"""

    spec_version: Annotated[str, PropertyInfo(alias="specVersion")]
    """version of the spec.

    The value of this field has no semantic meaning (e.g. don't interpret it as as a
    timestamp), but it can be used to impose a partial order. If a.spec_version <
    b.spec_version then a was the spec before b.
    """

    ssh_public_keys: Annotated[Iterable[SSHPublicKey], PropertyInfo(alias="sshPublicKeys")]
    """ssh_public_keys are the public keys used to ssh into the environment"""

    timeout: Timeout
    """Timeout configures the environment timeout"""
