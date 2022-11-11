from __future__ import annotations
from .geohome import GeoHomeHub
import logging
import async_timeout

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.const import ENERGY_KILO_WATT_HOUR, POWER_WATT
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from datetime import timedelta


from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):

    username = config_entry.data.get("username")
    password = config_entry.data.get("password")
    hub = GeoHomeHub(username, password, hass)

    async def async_update_data():
        async with async_timeout.timeout(30):
            return await hub.get_device_data()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name="sensor",
        update_method=async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=timedelta(seconds=120),
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [
            GeoHomeGasSensor(coordinator, hub),
            GeoHomeElectricitySensor(coordinator, hub),
            GeoHomeGasPriceSensor(coordinator, hub),
            GeoHomeElectricityPriceSensor(coordinator, hub),
            GeoHomeGasPowerSensor(coordinator, hub),
            GeoHomeElectricityPowerSensor(coordinator, hub),
            GeoHomeGasCostPerHourSensor(coordinator, hub),
            GeoHomeElectricityCostPerHourSensor(coordinator, hub),
        ]
    )


class GeoHomeGasSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = ENERGY_KILO_WATT_HOUR
        super().__init__(coordinator)

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_total"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gasReading

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:fire"

    @property
    def last_reset(self):
        return None


class GeoHomeGasPriceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        super().__init__(coordinator)
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "£/kWh"

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas Price"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_price"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gasPrice

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"


class GeoHomeElectricitySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        super().__init__(coordinator)
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.ENERGY
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_unit_of_measurement = ENERGY_KILO_WATT_HOUR

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_total"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricityReading

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:flash"

    @property
    def last_reset(self):
        return None


class GeoHomeElectricityPriceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        super().__init__(coordinator)
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "£/kWh"

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity Price"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_price"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricityPrice

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"


class GeoHomeGasPowerSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = POWER_WATT
        super().__init__(coordinator)

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas Power"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_power"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gasPower

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:fire"

    @property
    def last_reset(self):
        return None


class GeoHomeElectricityPowerSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.POWER
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = POWER_WATT
        super().__init__(coordinator)

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity Power"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_power"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricityPower

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:flash"

    @property
    def last_reset(self):
        return None
        
class GeoHomeGasCostPerHourSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "£/hour"
        super().__init__(coordinator)

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas Cost Per Hour"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_cost_per_hour"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if(self.hub.gasPower is not None and self.hub.gasPrice is not None):
            return round(self.hub.gasPower*self.hub.gasPrice/1000,2)
        else:
            return None

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:fire"

    @property
    def last_reset(self):
        return None

class GeoHomeElectricityCostPerHourSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        self.hub = hub
        self._attr_device_class = SensorDeviceClass.MONETARY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "£/hour"
        super().__init__(coordinator)

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity Cost Per Hour"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_cost_per_hour"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if(self.hub.electricityPower is not None and self.hub.electricityPrice is not None):
            return round(self.hub.electricityPower*self.hub.electricityPrice/1000,2)
        else:
            return None

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:flash"

    @property
    def last_reset(self):
        return None
