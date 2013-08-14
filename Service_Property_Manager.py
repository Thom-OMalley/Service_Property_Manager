#Import GUI essential modules
import easygui as eg
setupOptIn = eg.buttonbox("Welcome to the CFG Editor \n Created by Thomas O'Malley \n GIS Data Processor at the Illinois State Geological Survey \n \n Click Okay to Get Started", title="CFG Editor",image="ISGSLOGO.gif", choices=["Setup","Run"])

import os, sys
import cPickle as pickle

#Create save folder for pickled files
saveLoc = os.path.expanduser('~\\Documents\\CFG_Editor')

if not os.path.exists(saveLoc):
            os.makedirs(saveLoc)
            
###-GRAPHIC USER INTERFACE-###
msg         = "Enter your personal and survey information. For Online Resource URL, the service name and everything after will be generated.  Example entry: http://geothermal.isgs.illinois.edu/arcgis/services/aasggeothermal/"
title       = "WMS/WFS Properties"
fieldNames  = ('Name',
          'Position',
          'Organization (Provider)',
          'Website',
          'Street Address',
          'City',
          'State',
          'Postal (Zip) Code',
          'Country',
          'Phone',
          'Email',
          'Hours of Service',
          'Role',
          'Online Resource URL')
            
fieldValues = ()

try:
    pklFile = file(saveLoc+"\\ContactInfo.txt", 'r')
    restoreVal = pickle.load(pklFile)
    if setupOptIn == 'Setup':
        fieldValues = eg.multenterbox(msg,title, fieldNames, restoreVal)
    else: fieldValues = restoreVal
    pklFile.close()
except:
    print "No Values to Load"
    fieldValues = eg.multenterbox(msg + ".  No Values to Load" ,title, fieldNames)

# make sure that none of the fields were left blank
while 1:  # do forever, until we find acceptable values and break out
    if fieldValues == None: 
        break
    errmsg = ""
    
    # look for errors in the returned values
    for i in range(len(fieldNames)):
        if fieldValues[i].strip() == "":
            errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        
    if errmsg == "": 
        break # no problems found
    else:
        # show the box again, with the errmsg as the message    
        fieldValues = eg.multenterbox(errmsg, title, fieldNames, fieldValues)
    
#Save entries
pklFile = file(saveLoc+"\\ContactInfo.txt", 'w')
pickle.dump(fieldValues, pklFile)
pklFile.close()

#Makes lists into dictionary

fieldDict = dict(zip(fieldNames,fieldValues))
#Save Dict
pklFileDict = file(saveLoc+"\\pklFileDict.txt", 'w')
pickle.dump(fieldDict, pklFileDict)
pklFileDict.close()

#Determine master directory
try:
    pklFile = file(saveLoc+"\\pklFileDIR.txt", 'r')
    restoreValDIR = pickle.load(pklFile)
    if setupOptIn == 'Setup':
        path = eg.diropenbox("Path to folder containing CFG files.  ie.C:/Program Files (x86)/ArcGIS/Server10.0/server/user/cfg/aasggeothermal", default= restoreValDIR)
    else: path = restoreValDIR
except:
    path = eg.diropenbox("Path to folder containing CFG files.  ie.C:/Program Files (x86)/ArcGIS/Server10.0/server/user/cfg/aasggeothermal")

pklFile.close()
pklFile = file(saveLoc+"\\pklFileDIR.txt", 'w')
pickle.dump(path, pklFile)
pklFile.close()

#Use MXD Tags as Keywords?
try:
    pklFile = file(saveLoc+"\\pklFileTAGOptIn.txt", 'r')
    tagOptIn = pickle.load(pklFile)
except: tagOptIn = 'Use Tags'
try:
    pklFile = file(saveLoc+"\\pklFileTAG.txt", 'r')
    restoreValTags = pickle.load(pklFile)
    pklFile.close()
except: restoreValTags = ''
try:
    if setupOptIn == 'Setup':
        tagOptIn = eg.buttonbox("Do you wish to use MXD Tags as Service Keywords, or Generate Keywords using file name structure? Using MXD Tags is recommended.", title="CFG Editor",image="ISGSLOGO.gif", choices=["Use Tags","Generate"])
        pklFile = file(saveLoc+"\\pklFileTAGOptIn.txt", 'w')
        pickle.dump(tagOptIn, pklFile)
        pklFile.close()
        if tagOptIn == 'Use Tags':
            pathMXD = eg.diropenbox("Path to MXD master directory.  Program will search subfolders for MXD files.", default=restoreValTags)
            pklFile = file(saveLoc+"\\pklFileTAG.txt", 'w')
            pickle.dump(pathMXD, pklFile)
            pklFile.close()
        else: pass
    else: pathMXD = restoreValTags
except:
    tagOptIn = 'Use Tags'
    print "Use Tags directory lookup failed, defaulting to Generate"

#Ready to run script?
if setupOptIn == 'Setup':
    msg = "Thank you.  CFG Editor is now ready to run"
    title = "Ready to Begin"
    if eg.ccbox(msg, title):     # show a Continue/Cancel dialog
        pass  # user chose Continue
    else:  # user chose Cancel
        sys.exit(0)
else: pass

#Choose services to run script on
servFields = ['1','2','3','4','5','6','7','8','9','10']
Services = eg.multenterbox("Enter Service names. Exclude mxd. ie. 'ILWellLogs' without quotes", "Services", servFields)
Services = filter(None, Services)
pklFileServ = file(saveLoc+"\\pklFileServ.txt", 'w')
pickle.dump(Services, pklFileServ)
pklFileServ.close()

###-END GUI-###

#Part Two are you ready?  Do you wanna hear it?
os.system('CFG_Editor.py')

#Load errors from CFG_Editor

pklFileErr = file (saveLoc+"\\pklFileErr.txt", 'r')
errorList = pickle.load(pklFileErr)
pklFileErr.close()

#Display errors in GUI
eg.textbox(msg= "The following services produced errors: ", title= 'ERRORS', text='\n'.join(errorList))
