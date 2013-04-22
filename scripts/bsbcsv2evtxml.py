#!/usr/bin/python

#import os
#import sys
from obspy.core import UTCDateTime 

debug = True
output = ""


def _writeEvtXml():
    xmlout = "<EventParameters>"

    xmlout += "</EventParameters>"
    return xmlout
        


f = open("resources/bsb_toImport.csv")
lines = f.readlines()[1:]
for line in lines:
    bsbLine = line.split(',')
    # bsb parsing...
    evtYear = bsbLine[0]
    evtMonth = bsbLine[1]
    evtDay = bsbLine[2]
    evtHour = bsbLine[3]
    evtMin = bsbLine[4]
    evtSec = bsbLine[5]
    evtLat = bsbLine[6]
    evtLon = bsbLine[7]
    evtErr = bsbLine[8]
    evtDepth = bsbLine[10]
    evtMag = bsbLine[11]
    evtMagType = bsbLine[12]
    evtDataType = bsbLine[13]
    evtIntensity = bsbLine[14]
    evtUF = bsbLine[9]
    evtDescription = str(bsbline[15]) + str(bsbLine[16])
    evtOrigin = UTCDateTime(int(evtYear), int(evtMonth), int(evtDay), int(evtHour), int(evtMin), int(evtSec))
    if debug:
        print  evtOrigin, evtYear, evtMonth, evtDay, evtHour, evtMin, evtSec, evtLat, evtLon, evtErr, evtDepth, evtMag, evtMagType, evtDataType, evtIntensity, evtUF, evtDescription
        continue
    #    print evtOrigin.strftime("%Y%m%d%H%M%S")
    idOrigin = "Origin#" + evtOrigin.formatFissures()
    idEvent = "bsb" + str(evtOrigin.year) + str(evtOrigin.minute) + str(evtOrigin.second)
    idMag = idOrigin + "#netMag." + evtMagType
    
    output += """
        <EventParameters>
        <origin publicID='""" + idOrigin + """'>
            <time><value>""" + evtOrigin.formatIRISWebService() + """</value></time> 
            <latitude><value>""" + evtLat + """</value></latitude> 
            <longitude><value>""" + evtLon + """</value></longitude> 
            <depth><value>""" + evtDepth + """</value></depth>
            <depthType>from location</depthType>
            <methodID>LOCSAT</methodID>
            <earthModelID>iasp91</earthModelID>
            <evaluationMode>automatic</evaluationMode>
            <creationInfo>
                <agencyID>bsb</agencyID>
                <author>origin@bsb</author>
                <creationTime>""" + evtOrigin.formatIRISWebService() + """</creationTime>
            </creationInfo>"""
    
    if evtMag is not "0":
        output += """
            <magnitude publicID='""" + idMag + """'>
                <magnitude><value>""" + evtMag + """</value></magnitude>
                <type>""" + evtMagType + """</type>
                <creationInfo>
                    <agencyID>bsb</agencyID>
                    <author>mag@bsb</author>
                    <creationTime>""" + evtOrigin.formatIRISWebService() + """</creationTime>
                </creationInfo>
            </magnitude>"""
    output += """   
        </origin>
        <event publicID='"""+idEvent+"""'>
            <preferredOriginID>"""+idOrigin+"""</preferredOriginID>"""
    if evtMag is not "0":
        output += """
            <preferredMagnitudeID>"""+idMag+"</preferredMagnitudeID>"
    output += """   
            <creationInfo>
                <agencyID>bsb</agencyID>
                <author>event@bsb</author>
                <creationTime>"""+ evtOrigin.formatIRISWebService() +"""</creationTime>
                <modificationTime>"""+ evtOrigin.formatIRISWebService() + """</modificationTime>
            </creationInfo>
            <description>
                <text>"""+evtDescription+" - "+evtUF+"""</text>
                <type>region name</type>
            </description>
            <originReference>"""+idOrigin+"""</originReference>
        </event>
        </EventParameters>"""

output = """<?xml version="1.0" encoding="UTF-8"?>
<seiscomp xmlns="http://geofon.gfz-potsdam.de/ns/seiscomp3-schema/0.5" version="0.5">
""" + output + """
</seiscomp>"""
print output
