"""Climate platform support for Terncy."""

import logging

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    FAN_HIGH,
    FAN_LOW,
    FAN_MEDIUM,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_TEMPERATURE,
    MAJOR_VERSION,
    MINOR_VERSION,
    UnitOfTemperature,
)
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .hass.entity import TerncyEntity
from .utils import get_attr_value

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    TerncyEntity.ADD[f"{entry.entry_id}.climate"] = async_add_entities


K_AC_MODE = "acMode"  # 制冷：1，除湿：2，通风：4，制热：8
K_AC_FAN_SPEED = "acFanSpeed"  # 快速：1，中速：2，慢速：4
K_AC_CURRENT_TEMPERATURE = "acCurrentTemperature"  # 16~30
K_AC_TARGET_TEMPERATURE = "acTargetTemperature"  # 16~30
K_AC_RUNNING = "acRunning"  # 0 or 1
K_AC_TEMP_UNIT = "tempUnit"  # 温度单位为1表示精度为0.1度，否则精度为1度

_SUPPORTED_FEATURES: ClimateEntityFeature = (
    ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.FAN_MODE
)
if (MAJOR_VERSION, MINOR_VERSION) >= (2024, 2):
    _SUPPORTED_FEATURES |= ClimateEntityFeature.TURN_ON | ClimateEntityFeature.TURN_OFF


class TerncyClimate(TerncyEntity, ClimateEntity):
    _attr_fan_modes: list[str] | None = [FAN_LOW, FAN_MEDIUM, FAN_HIGH]
    _attr_hvac_mode = HVACMode.OFF
    _attr_fan_mode = FAN_LOW
    _attr_hvac_modes: list[HVACMode] = [
        HVACMode.OFF,
        HVACMode.COOL,
        HVACMode.DRY,
        HVACMode.FAN_ONLY,
        HVACMode.HEAT,
    ]
    _attr_max_temp: float = 30
    _attr_min_temp: float = 16
    _attr_precision: float = 1
    _attr_supported_features: ClimateEntityFeature = _SUPPORTED_FEATURES
    _attr_target_temperature_step: float | None = 1
    _attr_temperature_unit: str = UnitOfTemperature.CELSIUS

    _enable_turn_on_off_backwards_compatibility = False  # used in 2024.2~2024.12

    def update_state(self, attrs):
        # _LOGGER.debug("%s <= %s", self.eid, attrs)
        if (temp_unit := get_attr_value(attrs, K_AC_TEMP_UNIT)) is not None:
            if temp_unit == 1:
                self._attr_precision: float = 0.1
        if (ac_mode := get_attr_value(attrs, K_AC_MODE)) is not None:
            if ac_mode == 1:
                self._attr_hvac_mode = HVACMode.COOL
            elif ac_mode == 2:
                self._attr_hvac_mode = HVACMode.DRY
            elif ac_mode == 4:
                self._attr_hvac_mode = HVACMode.FAN_ONLY
            elif ac_mode == 8:
                self._attr_hvac_mode = HVACMode.HEAT
            else:
                self._attr_hvac_mode = None
        if (running := get_attr_value(attrs, K_AC_RUNNING)) is not None:
            if running == 0:
                self._attr_hvac_mode = HVACMode.OFF

        if (fan_speed := get_attr_value(attrs, K_AC_FAN_SPEED)) is not None:
            if fan_speed == 1:
                self._attr_fan_mode = FAN_HIGH
            elif fan_speed == 2:
                self._attr_fan_mode = FAN_MEDIUM
            elif fan_speed == 4:
                self._attr_fan_mode = FAN_LOW
            else:
                self._attr_fan_mode = None

        current_temperature = get_attr_value(attrs, K_AC_CURRENT_TEMPERATURE)
        if current_temperature is not None and current_temperature != 255:
            self._attr_current_temperature = current_temperature * self._attr_precision

        if (
            target_temperature := get_attr_value(attrs, K_AC_TARGET_TEMPERATURE)
        ) is not None:
            self._attr_target_temperature = target_temperature

        if self.hass:
            self.async_write_ha_state()

    async def async_set_temperature(self, **kwargs) -> None:
        """Set new target temperature."""
        _LOGGER.debug("%s async_set_temperature: %s", self.eid, kwargs)
        if ATTR_TEMPERATURE in kwargs:
            temperature = kwargs[ATTR_TEMPERATURE]
            self._attr_target_temperature = temperature
            await self.api.set_attribute(self.eid, K_AC_TARGET_TEMPERATURE, temperature)
            self.async_write_ha_state()

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        """Set new target fan mode."""
        if fan_mode == FAN_HIGH:
            self._attr_fan_mode = fan_mode
            await self.api.set_attribute(self.eid, K_AC_FAN_SPEED, 1)
        elif fan_mode == FAN_MEDIUM:
            self._attr_fan_mode = fan_mode
            await self.api.set_attribute(self.eid, K_AC_FAN_SPEED, 2)
        elif fan_mode == FAN_LOW:
            self._attr_fan_mode = fan_mode
            await self.api.set_attribute(self.eid, K_AC_FAN_SPEED, 4)
        else:
            _LOGGER.warning("Unsupported fan_mode: %s", fan_mode)
        self.async_write_ha_state()

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new target fan mode."""
        if hvac_mode == HVACMode.OFF:
            self._attr_hvac_mode = hvac_mode
            await self.api.set_attribute(self.eid, K_AC_RUNNING, 0)
        else:
            attrs = [{"attr": K_AC_RUNNING, "value": 1}]
            if hvac_mode == HVACMode.COOL:
                attrs.append({"attr": K_AC_MODE, "value": 1})
                self._attr_hvac_mode = hvac_mode
                await self.api.set_attributes(self.eid, attrs)
            elif hvac_mode == HVACMode.DRY:
                attrs.append({"attr": K_AC_MODE, "value": 2})
                self._attr_hvac_mode = hvac_mode
                await self.api.set_attributes(self.eid, attrs)
            elif hvac_mode == HVACMode.FAN_ONLY:
                attrs.append({"attr": K_AC_MODE, "value": 4})
                self._attr_hvac_mode = hvac_mode
                await self.api.set_attributes(self.eid, attrs)
            elif hvac_mode == HVACMode.HEAT:
                attrs.append({"attr": K_AC_MODE, "value": 8})
                self._attr_hvac_mode = hvac_mode
                await self.api.set_attributes(self.eid, attrs)
            else:
                _LOGGER.warning("Unsupported hvac_mode: %s", hvac_mode)
        self.async_write_ha_state()

    async def async_turn_on(self) -> None:
        """Turn the entity on."""
        await self.api.set_attribute(self.eid, K_AC_RUNNING, 1)


TerncyEntity.NEW["climate"] = TerncyClimate
