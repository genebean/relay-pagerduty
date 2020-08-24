#!/usr/bin/env python

from sys import exit
from pdpyras import EventsAPISession
from relay_sdk import Interface, Dynamic as D

relay = Interface()

token = relay.get(D.connection.accessToken)
session = EventsAPISession(token)

# All calls require type
# Trigger calls require summary/source/severity
# Trigger calls may take dedup_key
# Acknowledge and Resove calls require dedup_key, but I'm going to make it
# required on all because I can't figure out how to make it optional with the
# python SDK yet
eventType = relay.get(D.type)
dedup_key = relay.get(D.dedup_key)

if eventType is None:
    exit("A type is required for sending events, but none was set")
elif eventType == "trigger":
    summary = relay.get(D.summary)
    source = relay.get(D.source)
    severity = relay.get(D.severity)
    if summary is None:
        exit("A summary is required for event type trigger, but none was set")
    if source is None:
        exit("A source is required for event type trigger, but none was set")
    if severity is None:
        exit("A severity is required for event type trigger, but none was set")
    response = session.trigger(summary, source, dedup_key, severity)
elif eventType == "acknowledge":
    if dedup_key is None:
        exit("A dedup_key is required for event type acknowledge, but none was set")
    response = session.acknowledge(dedup_key)
elif eventType == "resolve":
    if dedup_key is None:
        exit("A dedup_key is required for event type resolve, but none was set")
    response = session.resolve(dedup_key)

relay.outputs.set("dedup_key", response)

print(response)
