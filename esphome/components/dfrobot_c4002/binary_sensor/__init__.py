import esphome.codegen as cg
from esphome.components import binary_sensor
import esphome.config_validation as cv
from esphome.const import CONF_ID, DEVICE_CLASS_OCCUPANCY

from .. import CONF_C4002_ID, C4002Component, dfrobot_c4002_ns

C4002BinarySensor = dfrobot_c4002_ns.class_("C4002BinarySensor", cg.Component)

CONF_PRESENCE = "presence"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(C4002BinarySensor),
        cv.Required(CONF_C4002_ID): cv.use_id(C4002Component),
        cv.Optional(CONF_PRESENCE): binary_sensor.binary_sensor_schema(
            device_class=DEVICE_CLASS_OCCUPANCY,
        ),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    c4002_binary_sensor = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(c4002_binary_sensor, config)

    if CONF_PRESENCE in config:
        bs = await binary_sensor.new_binary_sensor(config[CONF_PRESENCE])
        cg.add(c4002_binary_sensor.set_presence_binary_sensor(bs))

    c4002_component = await cg.get_variable(config[CONF_C4002_ID])
    cg.add(c4002_component.register_listener(c4002_binary_sensor))