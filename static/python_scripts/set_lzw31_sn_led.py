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

def make_int_if_possible(value):
    try:
        return int(value)
    except ValueError:
        return value

# The bullshit of passing make_int_if_possible is required due to a bug in HA.
# HA uses exec(code, global, local) which causes the code to run as if it was in
# a class definition!! Barf!
#
# See https://github.com/home-assistant/home-assistant/issues/24704
#
def validate_param(data, name, min_bound, max_bound, make_int_if_possible,
                   lookup=None):
    value = data.get(name)

    if value == "":
        value = None
    else:
        value = make_int_if_possible(value)

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

if entity_id is not None and entity_id != "":
    a = validate_param(data, "color", 0, 255, make_int_if_possible,
                       color_lookup)
    b = validate_param(data, "level", 0, 10, make_int_if_possible,
                       level_lookup)
    c = validate_param(data, "duration", 0, 255, make_int_if_possible,
                       duration_lookup)
    d = validate_param(data, "effect", 1, 4, make_int_if_possible,
                       effect_lookup)

    value = a + b * 256 + c * 65536 + d * 16777216

    for entity in entity_id.split(","):
        # logger.warning("Setting LED of {}".format(entity))

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
