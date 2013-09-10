#Re-import
import xml.dom.minidom as DOM
import os, sys, subprocess, glob, arcpy
import cPickle as pickle

#other important repeats
saveLoc = os.path.expanduser('~\\Documents\\GIS_Script_Data\\Service_Property_Manager')

#Error Handling
errorList = []
def addEr(msgEr):
    errorList.append(Service + ": " + msgEr)

#Load Pickled Data
pklFile = file(saveLoc+"\\pklFileDict.txt", 'r')
fieldDict = pickle.load(pklFile)

pklFile = file(saveLoc+"\\pklFileDIR.txt", 'r')
path = pickle.load(pklFile)

try:
    pklFile = file(saveLoc+"\\pklFileTAG.txt", 'r')
    pathMXD = pickle.load(pklFile)
except: print "No path to load"

pklFile = file(saveLoc+"\\pklFileTAGOptIn.txt", 'r')
tagOptIn = pickle.load(pklFile)

pklFileServ = file(saveLoc+"\\pklFileServ.txt", 'r')
Services = pickle.load(pklFileServ)

#States Dictionary

USstates = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}
#Find MXD files (function)
def getTags(path,serviceName):
    
    if path.endswith(".mxd"):
        mapList = [path]
    else:
        print "Searching for MXD files in " + str(path)
        mapaList = glob.glob(path+'\\*\\*\\'+serviceName+'.mxd')
        mapbList = glob.glob(path+'\\*\\*\\*\\'+serviceName+'.mxd')
        mapcList = glob.glob(path+'\\*\\*\\*\\*\\'+serviceName+'.mxd')
        mapdList = glob.glob(path+'\\*\\*\\*\\*\\*\\'+serviceName+'.mxd')
        mapeList = glob.glob(path+'\\*\\'+serviceName+'.mxd')
        mapfList = glob.glob(path+'\\'+serviceName+'.mxd')

        #Add the contents of each sub directory to the same list
        mapList = mapaList+mapbList+mapcList+mapdList+mapeList+mapfList

        MXD = mapList[0]

        mxd = arcpy.mapping.MapDocument(MXD)

        tags = mxd.tags

        print tags

        if len(mapList) > 1:
            addEr("More than one MXD matched this Service name.  Check keyword tags are satisfactory: " +tags)

        return tags


#Begin Editing
for Service in Services:

    cfg = path+'\\'+Service+".MapServer.cfg"

    x = 0
    
    OnlineResourceWFS = fieldDict.get('Online Resource URL')+Service+"/MapServer/WFSServer"
    OnlineResourceWMS = fieldDict.get('Online Resource URL')+Service+"/MapServer/WMSServer"
    StateAbr = Service[0:2]
    State = USstates.get(StateAbr)
    dataType = Service[2:]
    Abstract = str(dataType) +" in the state of "+ str(State)
    if tagOptIn == 'Use Tags':
        keywords = getTags(pathMXD,Service)
    else:
        keywords = "geothermal, " + str(dataType) +", "+ str(State)
    Title = str(State) +" "+ str(dataType)
    if dataType == "WellHeaders":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/wellheader/1.5"
    elif dataType == "WellLogs":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/welllog/0.8"
    elif dataType == "BoreholeLithIntervals":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/bhlithinterval/0.9"
    elif dataType == "HeatFlow1_23":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/heatflow/1.23"
    elif dataType == "ThermalConductivity":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/thermalconductivity/2.0"
    elif dataType == "BoreholeTemperatures":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/boreholetemperature/1.5"
    elif dataType == "AqueousChemistry1_10":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/aqueouschemistry/1.10"
    elif dataType == "aqWellChemistry":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/aqueouschemistry/1.9"
    elif dataType == "BedrockGeology":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/simplefeatures/" #Anomaly
    elif dataType == "HeatPumpFacilities":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/HeatPumpFacility/0.6"
    elif dataType == "DrillStemTests":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/drillstemtest/1.8"
    elif dataType == "DirectUseSites":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/directusesite/1.5"
    elif dataType == "RockChemistry":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/rockchemistry/0.4"
    elif dataType == "ThermalSprings":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/thermalspring/1.6"
    elif dataType == "ThermalSprings1_8":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/thermalspring/1.8"
    elif dataType == "SeismicHypocenters":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/hypocenter/1.7"
    elif dataType == "PhysicalSamples":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/physicalsample/0.8"
    elif dataType == "ActiveFaults":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/activefault/1.2"
    elif dataType == "BoreholeLithIntercepts":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/boreholelithintercept/1.1"
    elif dataType == "ContourLines":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/contourline/1.0"
    elif dataType == "GeothermalAreas":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/geothermalarea/0.7"
    elif dataType == "PowerPlantFacilities":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/powerplantfacility/0.2"
    elif dataType == "HydraulicProperties":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/hydraulicproperty/1.0"
    elif dataType == "PowerPlantProduction":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/plantproduction/1.0"
    elif dataType == "RadiogenicHeatProduction":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/radiogenicheatproduction/0.5"
    elif dataType == "VolcanicVents":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/volcanicvent/1.4"
    elif dataType == "WellFluidProduction":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/fluidproduction/1.1"
    elif dataType == "WellTests":
        AppSchemaURI = "http://stategeothermaldata.org/uri-gin/aasg/xmlschema/welltest/1.0"
    else:
        AppSchemaURI = "null"
        addEr("No Schema Match")
    # These are the WFS properties we will change in the cfg xml.
    keyList = ('OnlineResource','AppSchemaURI','AppSchemaPrefix','Title','Abstract','Keyword',
               'ServiceType', 'ServiceTypeVersion', 'Fees', 'IndividualName', 'PositionName',
               'ProviderName', 'ProviderSite', 'DeliveryPoint', 'City', 'AdministrativeArea',
               'PostalCode', 'Country', 'Phone', 'ElectronicMailAddress', 'HoursOfService', 'Role')
    valueList = (str(OnlineResourceWFS), str(AppSchemaURI), 'aasg', str(Service), str(Abstract), str(keywords),
                 'WFS', r'1.1.0', 'None', fieldDict.get('Name'), fieldDict.get('Position'), fieldDict.get('Organization (Provider)'),
                 fieldDict.get('Website'), fieldDict.get('Street Address'),
                 fieldDict.get('City'), fieldDict.get('State'), fieldDict.get('Postal (Zip) Code'),
                 fieldDict.get('Country'), fieldDict.get('Phone'), fieldDict.get('Email'),
                 fieldDict.get('Hours of Service'), fieldDict.get('Role'))

    # Read the cfg xml.
    try:
        doc = DOM.parse(cfg)
        print "Parsing"
    except:
        print "Parse Failed"
        addEr("Parse Failed")
    # Find desired property and change its value
    for key in keyList:
        print key
        DP = doc.getElementsByTagName("TypeName")
        for direct in DP:
            if direct.firstChild.data == "WFSServer":
                WFSServer = direct.firstChild
                Properties = WFSServer.parentNode.nextSibling.nextSibling.nextSibling.nextSibling.childNodes
                for prop in Properties:
                    if prop.localName == key:
                        if prop.hasChildNodes():
                            prop.firstChild.data = (str(valueList[0+x]))
                        else: #if no value exists for property
                            txt = doc.createTextNode(valueList[0+x])
                            prop.appendChild(txt)
                        x += 1
                        
    # These are the WMS properties we will change in the cfg xml.
    x=0
    keyList = ('Name', 'Title', 'Abstract', 'Keyword', 'OnlineResource', 'ContactPerson',
               'ContactPosition', 'ContactOrganization', 'AddressType','Address', 'City',
               'StateOrProvince', 'PostCode', 'Country', 'ContactVoiceTelephone',
               'ContactElectronicMailAddress', 'Fees','InheritLayerNames') 
    valueList = ('WMS', str(Service), str(Abstract), str(keywords), str(OnlineResourceWMS),
                 fieldDict.get('Name'), fieldDict.get('Position'), fieldDict.get('Organization (Provider)'), 'Postal',
                 fieldDict.get('Street Address'), fieldDict.get('City'), fieldDict.get('State'),
                 fieldDict.get('Postal (Zip) Code'), fieldDict.get('Country'),
                 fieldDict.get('Phone'), fieldDict.get('Email'), 'none','true')

    # Find desired property and change its value
    for key in keyList:
        print key
        DP = doc.getElementsByTagName("TypeName")
        for direct in DP:
            if direct.firstChild.data == "WMSServer":
                WFSServer = direct.firstChild
                Properties = WFSServer.parentNode.nextSibling.nextSibling.nextSibling.nextSibling.childNodes
                for prop in Properties:
                    if prop.localName == key:
                        if prop.hasChildNodes():
                            prop.firstChild.data = (str(valueList[0+x]))
                        else: #if no value exists for property
                            txt = doc.createTextNode(valueList[0+x])
                            prop.appendChild(txt)
                        x += 1
    # Output to a new sddraft.
    outXml = cfg     
    f = open(outXml, 'w')     
    doc.writexml( f )     
    f.close()

    print str(Service) + " Edit Complete"

#Restart Service to refresh
try:
    subprocess.call('net stop "ArcGIS Server Object Manager"')
    subprocess.call('net start "ArcGIS Server Object Manager"')
except:
    errorList.append("ArcGIS SOM Restart Failed")
    
#Export Errors to be read by Service Property Manager

pklFileErr = file(saveLoc+"\\pklFileErr.txt", 'w')
pickle.dump(errorList, pklFileErr)
pklFileErr.close()

print "Done"
