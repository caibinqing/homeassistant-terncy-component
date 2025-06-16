"""Constants for the Terncy integration."""

from homeassistant.const import MAJOR_VERSION, MINOR_VERSION

DOMAIN = "terncy"
HA_CLIENT_ID = "homeass_nbhQ43"

TERNCY_HUB_ID_PREFIX = "box-"
TERNCY_HUB_SVC_NAME = "_websocket._tcp.local."
TERNCY_MANU_NAME = "Xiaoyan Tech."

TERNCY_EVENT_SVC_ADD = "terncy_svc_add"
TERNCY_EVENT_SVC_REMOVE = "terncy_svc_remove"
TERNCY_EVENT_SVC_UPDATE = "terncy_svc_update"

PROFILE_PIR = 0
PROFILE_PLUG = 1
PROFILE_ONOFF_LIGHT = 2
PROFILE_DOOR_SENSOR = 3
PROFILE_SWITCH = 4
PROFILE_CURTAIN = 5
PROFILE_YAN_BUTTON = 6
PROFILE_SMART_DIAL = 7
PROFILE_COLOR_LIGHT = 8
# PROFILE_9 = 9  # 中央空调控制器
PROFILE_AC_UNIT_MACHINE = 10  # 中央空调分机
PROFILE_LOCK = 11  # lockState, battery
PROFILE_EXTENDED_COLOR_LIGHT = 12
PROFILE_COLOR_TEMPERATURE_LIGHT = 13

PROFILE_HA_TEMPERATURE_HUMIDITY = 15
# PROFILE_16 = 16  # todo volume, playState, mute
PROFILE_DIMMABLE_COLOR_TEMPERATURE_LIGHT = 17
PROFILE_OCCUPANCY_SENSOR = 18  # motion, [battery, motionL, motionR]
PROFILE_DIMMABLE_LIGHT = 19
PROFILE_DIMMABLE_LIGHT2 = 20
# PROFILE_21 = 21  # todo SM0202 iasZoneStatus, battery
PROFILE_RH3020 = 22  # iasZoneStatus, battery
PROFILE_GAS = 24  # iasZoneStatus
PROFILE_COLOR_DIMMABLE_LIGHT = 26
PROFILE_EXTENDED_COLOR_LIGHT2 = 27
PROFILE_HA_THERMASTAT = 34
PROFILE_XY_SINGLE_AIR_COND = 36
PROFILE_XY_FLOOR_HEATING = 37
PROFILE_XY_VENTILATION = 38
PROFILE_PRESENCE_SENSOR = 43

CONF_DEVID = "dev_id"
CONF_NAME = "dn"
CONF_IP = "ip"

CONF_EXPORT_DEVICE_GROUPS = "export_device_groups"
CONF_EXPORT_SCENES = "export_scenes"

ACTION_SINGLE_PRESS = "single_press"
ACTION_DOUBLE_PRESS = "double_press"
ACTION_TRIPLE_PRESS = "triple_press"

# 通过 hass.bus fire 的事件目前只有下面这三种 f"{DOMAIN}_{ACTION}"
ACTION_PRESSED = "pressed"
ACTION_LONG_PRESS = "long_press"
ACTION_ROTATION = "rotation"

# hass.bus fire 的事件的 data 里面的额外参数的key
EVENT_DATA_SOURCE = "source"
EVENT_DATA_CLICK_TIMES = "click_times"

# 给 device trigger 那边配置用的，是触发设备自动化的一个动作
DEVICE_TRIGGER_KEY_PRESSED_ACTIONS = [
    ACTION_SINGLE_PRESS,
    ACTION_DOUBLE_PRESS,
    ACTION_TRIPLE_PRESS,
    ACTION_LONG_PRESS,
]
DEVICE_TRIGGER_DIAL_ACTIONS = [
    *DEVICE_TRIGGER_KEY_PRESSED_ACTIONS,
    ACTION_ROTATION,
]

# 标记一下有按键的 profile
DEVICE_TRIGGER_ACTIONS_MAP = {
    PROFILE_PIR: DEVICE_TRIGGER_KEY_PRESSED_ACTIONS,
    PROFILE_ONOFF_LIGHT: DEVICE_TRIGGER_KEY_PRESSED_ACTIONS,
    PROFILE_SWITCH: DEVICE_TRIGGER_KEY_PRESSED_ACTIONS,
    PROFILE_YAN_BUTTON: DEVICE_TRIGGER_KEY_PRESSED_ACTIONS,
    PROFILE_SMART_DIAL: DEVICE_TRIGGER_DIAL_ACTIONS,
}

# 给 Event Entity 用的
_PRESS_EVENTS = [
    ACTION_SINGLE_PRESS,
    ACTION_DOUBLE_PRESS,
    ACTION_TRIPLE_PRESS,
    "quadruple_press",
    "quintuple_press",
    "sextuple_press",
    "septuple_press",
    "octuple_press",
    "nonuple_press",
]

EVENT_ENTITY_BUTTON_EVENTS = [ACTION_LONG_PRESS, *_PRESS_EVENTS]
EVENT_ENTITY_DIAL_EVENTS = [
    ACTION_LONG_PRESS,
    *_PRESS_EVENTS,
    ACTION_ROTATION,
]


HAS_EVENT_PLATFORM = (MAJOR_VERSION, MINOR_VERSION) >= (2023, 8)  # HA>=2023.8


# region Default Rooms

DEFAULT_ROOMS = {
    "zh-Hans": {
        "area-0000": "默认房间",
        "area-0001": "客厅",
        "area-0002": "主卧",
        "area-0003": "次卧",
        "area-0004": "餐厅",
        "area-0005": "厨房",
        "area-0006": "阳台",
        "area-0007": "书房",
        "area-0008": "玄关",
        "area-0009": "洗手间",
    },
    "zh-Hant": {
        "area-0000": "默認房間",
        "area-0001": "客廳",
        "area-0002": "主臥",
        "area-0003": "次臥",
        "area-0004": "餐廳",
        "area-0005": "廚房",
        "area-0006": "陽台",
        "area-0007": "書房",
        "area-0008": "玄關",
        "area-0009": "洗手間",
    },
    "en": {
        "area-0000": "Default Room",
        "area-0001": "Living Room",
        "area-0002": "Master Bedroom",
        "area-0003": "Guest Bedroom",
        "area-0004": "Dining Room",
        "area-0005": "Kitchen",
        "area-0006": "Balcony",
        "area-0007": "Study",
        "area-0008": "Entrance",
        "area-0009": "Bath Room",
    },
}

# endregion
