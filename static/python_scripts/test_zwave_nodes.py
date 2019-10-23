# The zwave.test_node service does not allow passing multiple node ids. But we
# want a service that takes multiple node ids. This service bridges the gap, we
# can pass a single node id or multiple ones as entity_id. The list is then
# split and passed one by one to zwave.test_node.
entity_id = data.get('entity_id')
if entity_id is not None:
    for entity in entity_id.split(","):
        hass.services.call('zwave', 'test_node', {'node_id': entity}, False)
        time.sleep(1)
