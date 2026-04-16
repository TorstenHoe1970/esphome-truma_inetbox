import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate
from esphome.const import (
    CONF_ID,
    CONF_NAME,
    CONF_TYPE,
)
from .. import truma_inetbox_ns, CONF_TRUMA_INETBOX_ID, TrumaINetBoxApp

DEPENDENCIES = ["truma_inetbox"]

TrumaClimate = truma_inetbox_ns.class_("TrumaClimate", climate.Climate, cg.Component)

CONF_SUPPORTED_TYPE = {
    "ROOM": truma_inetbox_ns.class_("TrumaRoomClimate", climate.Climate, cg.Component),
    "WATER": truma_inetbox_ns.class_("TrumaWaterClimate", climate.Climate, cg.Component),
}

# Hier ist die wichtige Stelle mit dem Unterstrich für 2026:
CONFIG_SCHEMA = climate._CLIMATE_SCHEMA.extend(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(TrumaClimate),
            cv.GenerateID(CONF_TRUMA_INETBOX_ID): cv.use_id(TrumaINetBoxApp),
            cv.Required(CONF_TYPE): cv.enum(CONF_SUPPORTED_TYPE, upper=True),
        }
    )
).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await climate.register_climate(var, config)
    await cg.register_parented(var, config[CONF_TRUMA_INETBOX_ID])
