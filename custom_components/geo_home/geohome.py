"""Config flow for Geo Home integration."""
from __future__ import annotations

import logging
import time

import requests
from requests.auth import HTTPBasicAuth

from homeassistant.components.climate.const import (
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_OFF,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
)
from homeassistant.core import HomeAssistant
from .const import (
    BASE_URL,
    DEVICE_DETAUILS_URL,
    LOGIN_URL,
    PERIODIC_DATA_URL,
    LIVE_DATA_URL,
)

_LOGGER = logging.getLogger(__name__)


class GeoHomeHub:
    """GeoHome Hub controller."""

    def __init__(self, username: str, password: str, hass: HomeAssistant) -> None:
        """Initialize the hub controller."""
        self.username = username
        self.password = password
        self.hass = hass
        self.accessToken = None
        self.electricityReading = None
        self.gasReading = None
        self.electricityReadingTime = None
        self.gasReadingTime = None
        self.deviceId = None
        self.gasPrice = None
        self.electricityPrice = None
        self.gasPower = None
        self.electricityPower = None

    def async_auth(self) -> bool:
        """Validate the username and password."""

        response = requests.post(
            BASE_URL + LOGIN_URL,
            json={"identity": self.username, "password": self.password},
        )
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get("validated"):
                self.accessToken = response_json.get("accessToken")
                return True
            else:
                return False
        else:
            _LOGGER.warning("GeoHome Auth API returned : " + str(response.status_code))
            return False

    async def authenticate(self) -> bool:
        """Validate the username, password and host asynchronously."""
        response = self.hass.async_add_executor_job(self.async_auth)

        return response

    def get_device_details(self):
        response = requests.get(
            BASE_URL + DEVICE_DETAUILS_URL,
            headers={"Authorization": "Bearer " + str(self.accessToken)},
        )
        if response.status_code == 200:
            response_json = response.json()
            system_roles = response_json.get("systemRoles")
            self.deviceId = system_roles[0]["systemId"]
        else:
            _LOGGER.warning("GeoHome Device Details API returned " + str(response.status_code))


    def async_get_device_data(self):
        if self.accessToken == None:
            self.async_auth()
        if self.deviceId == None:
            self.get_device_details()

        response = requests.get(
            BASE_URL + LIVE_DATA_URL + str(self.deviceId),
            headers={"Authorization": "Bearer " + str(self.accessToken)},
        )

        if response.status_code == 200:
            response_json = response.json()
            powerArray = response_json.get("power")

            for powerItem in powerArray:
                if powerItem["type"] == "ELECTRICITY":
                    if powerItem["valueAvailable"]:
                        self.electricityPower = powerItem["watts"]
                if powerItem["type"] == "GAS_ENERGY":
                    if powerItem["valueAvailable"]:
                        self.gasPower = powerItem["watts"]

            response = requests.get(
                BASE_URL + PERIODIC_DATA_URL + str(self.deviceId),
                headers={"Authorization": "Bearer " + str(self.accessToken)},
            )
            if response.status_code == 200:
                response_json = response.json()
                consumptionArray = response_json.get("totalConsumptionList")

                for consumptionItem in consumptionArray:
                    if consumptionItem["commodityType"] == "ELECTRICITY":
                        if consumptionItem["valueAvailable"]:
                            self.electricityReading = round(
                                consumptionItem["totalConsumption"], 2
                            )
                            self.electricityReadingTime = consumptionItem["readingTime"]
                    if consumptionItem["commodityType"] == "GAS_ENERGY":
                        if consumptionItem["valueAvailable"]:
                            self.gasReading = round(
                                consumptionItem["totalConsumption"] * 11.3627 / 1000, 2
                            )
                            self.gasReadingTime = consumptionItem["readingTime"]

                tarrifArray = response_json.get("activeTariffList")

                for tarrifItem in tarrifArray:
                    if tarrifItem["commodityType"] == "ELECTRICITY":
                        if tarrifItem["valueAvailable"]:
                            self.electricityPrice = (
                                tarrifItem["activeTariffPrice"] / 100
                            )
                    if tarrifItem["commodityType"] == "GAS_ENERGY":
                        if tarrifItem["valueAvailable"]:
                            self.gasPrice = tarrifItem["activeTariffPrice"] / 100
                return True
            else:
                self.accessToken = None
        else:
            self.accessToken = None
        return False

    async def get_device_data(self):

        response = self.hass.async_add_executor_job(self.async_get_device_data)
        return response