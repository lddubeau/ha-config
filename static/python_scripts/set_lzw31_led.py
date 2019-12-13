# The zwave.test_node service does not allow passing multiple node ids. But we
# want a service that takes multiple node ids. This service bridges the gap, we
# can pass a single node id or multiple ones as entity_id. The list is then
# split and passed one by one to zwave.test_node.
entity_id = data.get("entity_id")

color_lookup = {
    "red": 1,
    "orange": 21,
    "yellow": 42,
    "green": 85,
    "cyan": 127,
    "blue": 170,
    "pink": 234,
}

level_lookup = {
    None: 10,
    "on": 10,
    "off": 0,
}

duration_lookup = {
    None: 255,
}

effect_lookup = {
    None: 1,
    "solid": 1,
    "pulse": 2,
    "fast_blink": 3,
    "slow_blink": 4,
}

def validate_param(name, min_bound, max_bound, lookup=None):
    value = data.get(name)
    if isinstance(value, int):
        if value < min_bound or value > max_bound:
            raise Exception(f"{name} must be between {min_bound} and "
                            f"{max_bound}, inclusively")
        final = value
    else:
        if lookup is None:
            raise Exception(f"{name} must be a number")

        try:
            final = lookup[value]
        except KeyError:
            raise Exception(f"{name} must be specified" if value is None
                            else f"not a supported {name} keyword: {value}")

    return final

if entity_id is not None:
    a = validate_param("color", 0, 255, color_lookup)
    b = validate_param("level", 0, 10, level_lookup)
    c = validate_param("duration", 0, 255, duration_lookup)
    d = validate_param("effect", 1, 4, effect_lookup)

    value = a + b * 256 + c * 65536 + d * 16777216

    for entity in entity_id.split(","):
        state = hass.states.get(entity)

        if state is None:
            continue

        node_id = state.attributes["node_id"]

        hass.services.call("zwave", "set_config_parameter",
                           {
                               "node_id": node_id,
                               "parameter": 16,
                               "size": 4,
                               "value": value,
                           },
                           False)
