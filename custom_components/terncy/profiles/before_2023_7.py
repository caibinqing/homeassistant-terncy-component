"""
这个文件的配置是给 HA 版本 <2023.7 用的
2023.7 引入了新的实体命名机制, 详见: https://developers.home-assistant.io/docs/core/entity/#entity-naming

本文件基于 profiles.py, 做以下修改以兼容旧版:
- 所有的 description 都需要指定 name。（具体字符串或者None）
- translation_key 建议删除，旧版中没有作用。

备注：
  name=None 表示这个实体是这个设备的主要功能，直接使用设备名字。
  light、cover、climate 已经在 base description 中声明过 name=None 了。
"""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.cover import CoverDeviceClass
from homeassistant.components.light import ColorMode
from homeassistant.components.switch import SwitchDeviceClass
from homeassistant.const import MAJOR_VERSION, MINOR_VERSION

if (MAJOR_VERSION, MINOR_VERSION) >= (2023, 3):
    from homeassistant.const import EntityCategory
else:
    from homeassistant.helpers.entity import EntityCategory

from ..const import (
    PROFILE_AC_UNIT_MACHINE,
    PROFILE_COLOR_DIMMABLE_LIGHT,
    PROFILE_COLOR_LIGHT,
    PROFILE_COLOR_TEMPERATURE_LIGHT,
    PROFILE_CURTAIN,
    PROFILE_DIMMABLE_COLOR_TEMPERATURE_LIGHT,
    PROFILE_DIMMABLE_LIGHT,
    PROFILE_DIMMABLE_LIGHT2,
    PROFILE_DOOR_SENSOR,
    PROFILE_EXTENDED_COLOR_LIGHT,
    PROFILE_EXTENDED_COLOR_LIGHT2,
    PROFILE_GAS,
    PROFILE_HA_TEMPERATURE_HUMIDITY,
    PROFILE_HA_THERMASTAT,
    PROFILE_LOCK,
    PROFILE_OCCUPANCY_SENSOR,
    PROFILE_ONOFF_LIGHT,
    PROFILE_PIR,
    PROFILE_PLUG,
    PROFILE_PRESENCE_SENSOR,
    PROFILE_RH3020,
    PROFILE_SMART_DIAL,
    PROFILE_SWITCH,
    PROFILE_XY_SINGLE_AIR_COND,
    PROFILE_YAN_BUTTON,
)
from ..hass.entity_descriptions import (
    BatteryDescription,
    HumidityDescription,
    IlluminanceDescription,
    TemperatureDescription,
    TerncyBinarySensorDescription,
    TerncyClimateDescription,
    TerncyCoverDescription,
    TerncyEntityDescription,
    TerncyLightDescription,
    TerncySwitchDescription,
)
from ..switch import (
    ATTR_DISABLED_RELAY_STATUS,
    ATTR_DISABLE_RELAY,
    ATTR_ON,
    ATTR_PURE_INPUT,
    KEY_DISABLED_RELAY_STATUS,
    KEY_DISABLE_RELAY,
    KEY_WALL_SWITCH,
)

PROFILES: dict[int, list[TerncyEntityDescription]] = {
    PROFILE_PIR: [
        TemperatureDescription(name="Temperature"),
        IlluminanceDescription(name="Illuminance"),
        BatteryDescription(name="Battery"),
        TerncyBinarySensorDescription(
            key="motion",
            sub_key="motionl",
            device_class=BinarySensorDeviceClass.MOTION,
            name="Motion Left",
            value_attr="motionL",
        ),
        TerncyBinarySensorDescription(
            key="motion",
            sub_key="motionr",
            device_class=BinarySensorDeviceClass.MOTION,
            name="Motion Right",
            value_attr="motionR",
        ),
        TerncyBinarySensorDescription(
            key="motion",
            sub_key="motion",
            device_class=BinarySensorDeviceClass.MOTION,
            entity_registry_enabled_default=False,
            name="Motion",
            value_attr="motion",
        ),
    ],
    PROFILE_PLUG: [
        TerncySwitchDescription(
            key="switch",
            device_class=SwitchDeviceClass.OUTLET,
            name=None,
            value_attr=ATTR_ON,
        ),
    ],
    PROFILE_ONOFF_LIGHT: [
        TerncySwitchDescription(
            key=KEY_WALL_SWITCH,
            device_class=SwitchDeviceClass.SWITCH,
            name=None,
            value_attr=ATTR_ON,
        ),
        TerncySwitchDescription(
            key="switch",
            sub_key="pure_input",
            entity_category=EntityCategory.CONFIG,
            icon="mdi:remote",
            name="Wireless Switch Enabled",
            value_attr=ATTR_PURE_INPUT,
        ),
        TerncySwitchDescription(
            key=KEY_DISABLE_RELAY,
            sub_key="disable_relay",
            entity_category=EntityCategory.CONFIG,
            name="Relay Disabled",
            value_attr=ATTR_DISABLE_RELAY,
        ),
        TerncySwitchDescription(
            key=KEY_DISABLED_RELAY_STATUS,
            sub_key="disabled_relay_status",
            entity_category=EntityCategory.CONFIG,
            name="Relay is always on",
            value_attr=ATTR_DISABLED_RELAY_STATUS,
        ),
    ],
    PROFILE_DOOR_SENSOR: [
        TerncyBinarySensorDescription(
            key="contact",
            name=None,
            value_attr="contact",
        ),
        TemperatureDescription(name="Temperature"),
        BatteryDescription(name="Battery"),
    ],
    PROFILE_SWITCH: [
        TerncySwitchDescription(
            key="switch",
            device_class=SwitchDeviceClass.SWITCH,
            name=None,
            value_attr=ATTR_ON,
        ),
    ],
    PROFILE_CURTAIN: [
        TerncyCoverDescription(
            key="cover",
            device_class=CoverDeviceClass.CURTAIN,
        ),
    ],
    PROFILE_YAN_BUTTON: [
        # no entity, but device can fire event
    ],
    PROFILE_SMART_DIAL: [
        BatteryDescription(name="Battery"),
    ],
    PROFILE_COLOR_LIGHT: [
        TerncyLightDescription(
            color_mode=ColorMode.HS,
            supported_color_modes={ColorMode.HS},
        ),
    ],
    PROFILE_AC_UNIT_MACHINE: [
        TerncyClimateDescription(
            key="climate",
        ),
    ],
    PROFILE_HA_THERMASTAT: [
        TerncyClimateDescription(
            key="climate",
        ),
    ],
    PROFILE_XY_SINGLE_AIR_COND: [
        TerncyClimateDescription(
            key="climate",
        ),
    ],
    PROFILE_LOCK: [
        TerncyBinarySensorDescription(
            key="lock",
            device_class=BinarySensorDeviceClass.LOCK,
            name=None,
            value_attr="lockState",
            value_map={1: False, 2: True},
        ),
        BatteryDescription(name="Battery"),
    ],
    PROFILE_EXTENDED_COLOR_LIGHT: [
        TerncyLightDescription(
            color_mode=ColorMode.HS,
            supported_color_modes={ColorMode.COLOR_TEMP, ColorMode.HS},
        ),
    ],
    PROFILE_COLOR_TEMPERATURE_LIGHT: [
        TerncyLightDescription(
            color_mode=ColorMode.COLOR_TEMP,
            supported_color_modes={ColorMode.COLOR_TEMP},
        ),
    ],
    PROFILE_HA_TEMPERATURE_HUMIDITY: [
        TemperatureDescription(name="Temperature"),
        HumidityDescription(name="Humidity"),
        BatteryDescription(name="Battery"),
    ],
    PROFILE_DIMMABLE_COLOR_TEMPERATURE_LIGHT: [
        TerncyLightDescription(
            color_mode=ColorMode.COLOR_TEMP,
            supported_color_modes={ColorMode.COLOR_TEMP},
        ),
    ],
    PROFILE_OCCUPANCY_SENSOR: [
        TerncyBinarySensorDescription(
            key="motion",
            sub_key="motion",
            device_class=BinarySensorDeviceClass.MOTION,
            name="Motion",
            value_attr="motion",
        ),
        BatteryDescription(
            name="Battery",
            required_attrs=["battery"],
        ),
        TerncyBinarySensorDescription(
            key="motion",
            sub_key="motionl",
            device_class=BinarySensorDeviceClass.MOTION,
            name="Motion Left",
            value_attr="motionL",
            required_attrs=["motionL"],
        ),
        TerncyBinarySensorDescription(
            key="motion",
            sub_key="motionr",
            device_class=BinarySensorDeviceClass.MOTION,
            name="Motion Right",
            value_attr="motionR",
            required_attrs=["motionR"],
        ),
    ],
    PROFILE_DIMMABLE_LIGHT: [
        TerncyLightDescription(
            color_mode=ColorMode.BRIGHTNESS,
            supported_color_modes={ColorMode.BRIGHTNESS},
        ),
    ],
    PROFILE_DIMMABLE_LIGHT2: [
        TerncyLightDescription(
            color_mode=ColorMode.BRIGHTNESS,
            supported_color_modes={ColorMode.BRIGHTNESS},
        ),
    ],
    PROFILE_RH3020: [
        TerncyBinarySensorDescription(
            key="moisture",
            sub_key="moisture",
            device_class=BinarySensorDeviceClass.MOISTURE,
            name=None,
            value_attr="iasZoneStatus",
            value_map={32: False, 33: True},
        ),
        BatteryDescription(
            name="Battery",
            value_fn=lambda x: min(x, 100),
        ),
    ],
    PROFILE_GAS: [
        TerncyBinarySensorDescription(
            key="gas",
            sub_key="gas",
            device_class=BinarySensorDeviceClass.GAS,
            name=None,
            value_attr="iasZoneStatus",
            value_map={32: False, 33: True},
        ),
    ],
    PROFILE_COLOR_DIMMABLE_LIGHT: [
        TerncyLightDescription(
            color_mode=ColorMode.HS,
            supported_color_modes={ColorMode.COLOR_TEMP, ColorMode.HS},
        ),
    ],
    PROFILE_EXTENDED_COLOR_LIGHT2: [
        TerncyLightDescription(
            color_mode=ColorMode.HS,
            supported_color_modes={ColorMode.COLOR_TEMP, ColorMode.HS},
        ),
    ],
    PROFILE_PRESENCE_SENSOR: [
        TerncyBinarySensorDescription(
            key="presenceStatus",
            device_class=BinarySensorDeviceClass.PRESENCE,
            value_attr="presenceStatus",
        ),
    ],
}
