"""Config flow for Geo Home integration."""
from __future__ import annotations

import logging
import time

import requests
from requests.auth import HTTPBasicAuth

from homeassistant.core import HomeAssistant
from .const import (
    BASE_URL,
    DEVICE_DETAUILS_URL,
    LOGIN_URL,
    PERIODIC_DATA_URL,
    LIVE_DATA_URL,
    DAILY_DATA_URL,
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
        self.electricityCreditRemaining = None
        self.gasCreditRemaining = None
        self.electricityEmergencyCreditBalance = None
        self.gasEmergencyCreditBalance = None
        self.electricitySupplyStatus = None
        self.gasSupplyStatus = None
        self.electricityReading = None
        self.gasReading = None
        self.gaskWhReading = None
        self.electricityReadingTime = None
        self.gasReadingTime = None
        self.deviceId = None
        self.gasPrice = None
        self.gasStandingCharge = None
        self.electricityPrice = None
        self.electricityStandingCharge = None
        self.gasPower = None
        self.electricityPower = None
        self.gasCostToday = None
        self.gasCostThisWeek = None
        self.gasCostThisMonth = None
        self.gasCostThisBill = None
        self.gasCostThisBillTimestamp=None
        self.gaskWhToday = None
        self.gaskWhThisWeek = None
        self.gaskWhThisMonth = None
        self.electricityCostToday = None
        self.electricityCostThisWeek = None
        self.electricityCostThisMonth = None
        self.electricityCostThisBill = None
        self.electricityCostThisBillTimestamp=None
        self.electricitykWhToday = None
        self.electricitykWhThisWeek = None
        self.electricitykWhThisMonth = None
        self.gasZigbeeStatus = None
        self.electricityZigbeeStatus = None
        self.hanStatus = None


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
            systemDetails = response_json.get("systemDetails")
            for system in systemDetails:
                if len(system["devices"])>0:
                    self.deviceId = system["systemId"]
                    break
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

            if powerArray is not None:

              for powerItem in powerArray:
                  if powerItem["type"] == "ELECTRICITY":
                      if powerItem["valueAvailable"]:
                          self.electricityPower = powerItem["watts"]
                  if powerItem["type"] == "GAS_ENERGY":
                      if powerItem["valueAvailable"]:
                          self.gasPower = powerItem["watts"]

            remainingArray = response_json.get("remainingCredit")

            if remainingArray is not None:

              for remainingItem in remainingArray:
                  if remainingItem["commodityType"] == "ELECTRICITY":
                      if remainingItem["valueAvailable"]:
                          self.electricityCreditRemaining = round(remainingItem["creditBalance"]/100,2)
                  if remainingItem["commodityType"] == "GAS_ENERGY":
                      if remainingItem["valueAvailable"]:
                          self.gasCreditRemaining = round(remainingItem["creditBalance"]/100,2)

            EMCArray = response_json.get("emergencyCredit")

            if EMCArray is not None:

              for EMCItem in EMCArray:
                  if EMCItem["commodityType"] == "ELECTRICITY":
                      if EMCItem["valueAvailable"]:
                          self.electricityEmergencyCreditBalance = round(EMCItem["emergencyCreditBalance"]/100,2)
                  if EMCItem["commodityType"] == "GAS_ENERGY":
                      if EMCItem["valueAvailable"]:
                          self.gasEmergencyCreditBalance = round(EMCItem["emergencyCreditBalance"]/100,2)

            zigbeeStatus = response_json.get("zigbeeStatus")

            if zigbeeStatus is not None:

              self.gasZigbeeStatus = zigbeeStatus["gasClusterStatus"]
              self.electricityZigbeeStatus = zigbeeStatus["electricityClusterStatus"]
              self.hanStatus = zigbeeStatus["hanStatus"]


            response = requests.get(
                BASE_URL + PERIODIC_DATA_URL + str(self.deviceId),
                headers={"Authorization": "Bearer " + str(self.accessToken)},
            )
            if response.status_code == 200:
                response_json = response.json()
                consumptionArray = response_json.get("totalConsumptionList")

                if consumptionArray is not None:

                  for consumptionItem in consumptionArray:
                      if consumptionItem["commodityType"] == "ELECTRICITY":
                          if consumptionItem["valueAvailable"]:
                              self.electricityReading = round(
                                  consumptionItem["totalConsumption"], 2
                              )
                              self.electricityReadingTime = consumptionItem["readingTime"]
                      if consumptionItem["commodityType"] == "GAS_ENERGY":
                          if consumptionItem["valueAvailable"]:
                              self.gasReading = consumptionItem["totalConsumption"]/1000
                              self.gaskWhReading = round(consumptionItem["totalConsumption"] * 11.3627 / 1000, 2)
                              self.gasReadingTime = consumptionItem["readingTime"]


                supplyStatusArray = response_json.get("supplyStatusList")

                if supplyStatusArray is not None:

                  for supplyStatusItem in supplyStatusArray:
                      if supplyStatusItem["commodityType"] == "ELECTRICITY":
                              self.electricitySupplyStatus =  supplyStatusItem["supplyStatus"]
                      if supplyStatusItem["commodityType"] == "GAS_ENERGY":
                              self.gasSupplyStatus=  supplyStatusItem["supplyStatus"]



                tarrifArray = response_json.get("activeTariffList")

                if tarrifArray is not None:

                  for tarrifItem in tarrifArray:
                      if tarrifItem["commodityType"] == "ELECTRICITY":
                          if tarrifItem["valueAvailable"]:
                              self.electricityPrice = tarrifItem["activeTariffPrice"] / 100
                      if tarrifItem["commodityType"] == "GAS_ENERGY":
                          if tarrifItem["valueAvailable"]:
                              self.gasPrice = tarrifItem["activeTariffPrice"] / 100

                billToDateArray = response_json.get("billToDateList")

                if billToDateArray is not None:
                  for billToDateItem in billToDateArray:
                      if billToDateItem["commodityType"] == "ELECTRICITY":
                          if billToDateItem["valueAvailable"]:
                              self.electricityCostThisBill = round(billToDateItem["billToDate"]/100,2)
                              self.electricityCostThisBillTimestamp=billToDateItem["startUTC"]
                      if billToDateItem["commodityType"] == "GAS_ENERGY":
                          if billToDateItem["valueAvailable"]:
                              self.gasCostThisBill = round(billToDateItem["billToDate"]/100,2)
                              self.gasCostThisBillTimestamp=billToDateItem["startUTC"]


                currentCostsElecArray = response_json.get("currentCostsElec")

                if currentCostsElecArray is not None:

                  for currentCostsElecItem in currentCostsElecArray:
                      if currentCostsElecItem["duration"] == "DAY":
                          self.electricitykWhToday = currentCostsElecItem["energyAmount"]
                          self.electricityCostToday = round(currentCostsElecItem["costAmount"]/100,2)
                      if currentCostsElecItem["duration"] == "WEEK":
                          self.electricitykWhThisWeek = currentCostsElecItem["energyAmount"]
                          self.electricityCostThisWeek = round(currentCostsElecItem["costAmount"]/100,2)
                      if currentCostsElecItem["duration"] == "MONTH":
                          self.electricitykWhThisMonth = currentCostsElecItem["energyAmount"]
                          self.electricityCostThisMonth = round(currentCostsElecItem["costAmount"]/100,2)

                currentCostsGasArray = response_json.get("currentCostsGas")

                if currentCostsGasArray is not None:

                  for currentCostsGasItem in currentCostsGasArray:
                      if currentCostsGasItem["duration"] == "DAY":
                          self.gaskWhToday = currentCostsGasItem["energyAmount"]
                          self.gasCostToday = round(currentCostsGasItem["costAmount"]/100,2)
                      if currentCostsGasItem["duration"] == "WEEK":
                          self.gaskWhThisWeek = currentCostsGasItem["energyAmount"]
                          self.gasCostThisWeek = round(currentCostsGasItem["costAmount"]/100,2)
                      if currentCostsGasItem["duration"] == "MONTH":
                          self.gaskWhThisMonth = currentCostsGasItem["energyAmount"]
                          self.gasCostThisMonth = round(currentCostsGasItem["costAmount"]/100,2)


                response = requests.get(
                    BASE_URL + DAILY_DATA_URL + str(self.deviceId),
                    headers={"Authorization": "Bearer " + str(self.accessToken)},
                )
                if response.status_code == 200:
                    response_json = response.json()
                    standingChargeArray = response_json.get("standingChargeList")

                    if standingChargeArray is not None:
                      for standingChargeItem in standingChargeArray:
                          if standingChargeItem["commodityType"] == "ELECTRICITY":
                              if standingChargeItem["valueAvailable"]:
                                  self.electricityStandingCharge = standingChargeItem["standingCharge"]/100
                          if standingChargeItem["commodityType"] == "GAS_ENERGY":
                              if standingChargeItem["valueAvailable"]:
                                  self.gasStandingCharge = standingChargeItem["standingCharge"]/100


                return True
            else:
                self.accessToken = None
        else:
            self.accessToken = None
        return False

    async def get_device_data(self):

        response = await self.hass.async_add_executor_job(self.async_get_device_data)
        return response
