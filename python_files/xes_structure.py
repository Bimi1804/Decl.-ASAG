# This file defines the .xes structure for exporting an event-log

class Xes_template:
    def __init__(self):
        # header with {traces} filler
        self.xes_head = """<?xml version="1.0" encoding="UTF-8" ?>
            <log xes.version="1.0" xes.features="nested-attributes" openxes.version="1.0RC7">
                <extension name="Time" prefix="time" uri="http://www.xes-standard.org/time.xesext"/>
                <extension name="Lifecycle" prefix="lifecycle" uri="http://www.xes-standard.org/lifecycle.xesext"/>
                <extension name="Concept" prefix="concept" uri="http://www.xes-standard.org/concept.xesext"/>
                <classifier name="Event Name" keys="concept:name"/>
                <classifier name="(Event Name AND Lifecycle transition)" keys="concept:name lifecycle:transition"/>
                <string key="concept:name" value="XES Event Log"/>
                {traces}
            </log>"""
        # trace with filler for {trace_id} and {events}
        self.xes_trace = """<trace>
                        <string key="concept:name" value="{trace_id}"/>
                        {events}
                    </trace>"""
        # event with filler for {word} and {order}
        self.xes_event = """<event>
                        <string key="concept:name" value="{word}"/>
                        <string key="lifecycle:transition" value="complete"/>
                        <int key="Order" value="{order}"/>
                    </event>"""
xes_template = Xes_template() # instantiation of Xes_template
