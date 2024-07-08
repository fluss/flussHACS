"""Support for Fluss Devices."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import FlussApiClient
from .const import DOMAIN
from .device import FlussCover

LOGGER = logging.getLogger(__package__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Fluss Devices."""

    api: FlussApiClient = hass.data[DOMAIN][entry.entry_id]
    # for device in await api.async_get_devices():
    #     LOGGER.warning("INFO %s", device)
    # # async_add_entities(FlussDevice() for device in )

    devices = await api.async_get_devices()
    LOGGER.warning("Devices %s", devices)
    if isinstance(devices, dict) and "devices" in devices:
        devices = devices["devices"]

    added_deviceIds = set()

    entities = []
    for device in devices:
        # use deviceId to avoid duplication
        entityId = f"cover.{device['deviceId']}"
        deviceId = device["deviceId"]
        if hass.states.get(entityId):
            LOGGER.warning(f"Entity {entityId} already exists, skipping creation.")  # noqa: G004
            continue
        entity = FlussCover(api, device)
        entities.append(entity)
        added_deviceIds.add(deviceId)
        LOGGER.debug(f"Adding entity: {entityId}")  # noqa: G004

    async_add_entities(entities)
