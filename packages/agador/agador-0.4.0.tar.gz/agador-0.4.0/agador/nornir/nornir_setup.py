from typing import Optional

from nornir import InitNornir
from nornir.core import Nornir

from .logging import configure_nornir_logging
from .connection_options import configure_connection_options
from .device_credentials import update_nornir_credentials

from ..utils import agador_cfg


def nornir_setup(
    log_level: str = "DEBUG",
    log_globally: Optional[bool] = False,
    log_to_console: Optional[bool] = False,
    device_filter: Optional[str] = None,
    role_filter: Optional[str] = None,
) -> Nornir:
    """
    Initializes Nornir to point at netbox, and to only care about active
    devices tied to a specific subset of device roles.
    Sets up logging. Populates default and custom passwords from cyberark. Returns
    customized Nornir instance
    """

    logfile = agador_cfg("LOG_DIR") + "/agador.log"
    configure_nornir_logging(log_level, log_globally, logfile, log_to_console)

    filter_params = {"status": "active", "has_primary_ip": "True"}

    # Restrict what the netbox inventory plugin pulls if it was indicated
    # on the CLI
    if device_filter:
        filter_params["name"] = device_filter
    elif role_filter:
        filter_params["role"] = [role_filter]

    # Nornir initialization
    nr = InitNornir(
        runner={
            "plugin": "multiprocess",
            "options": {
                "num_workers": int(agador_cfg("NUM_WORKERS")),
            },
        },
        inventory={
            "plugin": "NetBoxInventory2",
            "options": {
                "nb_url": agador_cfg("NB_URL"),
                "nb_token": agador_cfg("NB_TOKEN"),
                "filter_parameters": filter_params,
                "ssl_verify": False,
            },
        },
        logging={
            "enabled": False,
        },
    )

    update_nornir_credentials(nr)
    configure_connection_options(nr)

    return nr
