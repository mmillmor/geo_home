# Geo Home

Integrate with Geo Home smart meters in Home Assistant

## Instructions

To collect Geo Home smart meter data, you must have a WiFi connected
smart meter from Geo Together. If you have a smart meter that is not
WiFi connected by default, you can buy a WiFi module from 
Geo Together at https://geotogether.com/product-category/accessories/, and then e-mail customerservices@geotogether.com to ask
them to enable your meter.

Once you have a WiFi connected smart meter, create an account on the Geo Home app. The username and password for this account are used to
connect the Geo Home integration.

After downloading the Geo Home integration into HACS, remember to install it by navigating to Settings -> Devices & services -> Add integration, then
select "Geo Home". You will be prompted for
a username and password. Enter the ones you created from the app. This will create Gas and Electricity sensors, tracking the lifetime
energy usage of your meters.


## Upgrading

If you are upgrading from version 1.2, the units of your cost sensors will have been £/kWh instead of GBP/kWh. You can go to https://my.home-assistant.io/redirect/developer_statistics to correct that
