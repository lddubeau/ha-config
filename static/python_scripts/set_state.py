entity_id = data.get("entity_id")
if entity_id is not None:
    state_obj = hass.states.get(entity_id)
    state = state_obj.state if state_obj is not None else None
    attributes = state_obj.attributes.copy() if state_obj is not None else {}
    attributes.update(data.get("attributes", {}))

    hass.states.set(entity_id, data.get("state", state), attributes)
