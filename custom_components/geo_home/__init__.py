"""The Geo Home integration."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .geohome import GeoHomeHub

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["sensor"]


class GeoHomeCoordinator(DataUpdateCoordinator):
    """Coordinator for Geo Home."""
    def __init__(self, hass, hub):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="geo home sensor",
            update_interval=timedelta(seconds=120),
        )
        self.hub = hub

    async def _async_update_data(self):
        async with async_timeout.timeout(30):
            res = await self.hub.get_device_data()
            if not res:
                raise UpdateFailed("Failed to fetch data from GeoHome API")
            return datetime.now()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Geo Home from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    username = entry.data.get("username")
    password = entry.data.get("password")
    system_name = entry.data.get("system_name")

    hub = GeoHomeHub(username, password, system_name, hass)
    coordinator = GeoHomeCoordinator(hass, hub)

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    entry.async_on_unload(entry.add_update_listener(update_listener))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        if DOMAIN in hass.data:
            hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
