#!/bin/sh

IFS= read API_KEY < ./secrets/api-key.txt

curl -X POST -H "Authorization: Bearer $API_KEY" -H "Content-Type: application/json" -d '{"state": "on"}' https://ha.lddubeau.com:8123/api/states/binary_sensor.sensor_test_do_not_use
