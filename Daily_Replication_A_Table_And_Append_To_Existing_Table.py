# ---------------------------------------------------------------------------
# Daily_Replication_A_Table_And_Append_To_Existing_Table.py
# Description: Replicate incident tabular data and append it to yesterdays data
# Key Data: FROM WHERE; Destination table is WHERE
# Modified: 
# ---------------------------------------------------------------------------
import arcpy, sys, logging, logging.handlers, os, time, string, inspect, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# NEXT THREE VARIABLES NEEDED FOR EMAIL ERROR EVENTS
MailSendTO = 'youremail@domain.com'
MailSendFROM ='githubexampleuser@domain.net'
SERVER = 'MYwebmail'  #SMTP SERVER NAME

Fullname = os.path.basename(inspect.getfile(inspect.currentframe()))
PyName = os.path.splitext(Fullname)[0]      # Name of the Py script
PyLocation = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory

#TODO:Set these variables
#********************************************************
LogName = PyName    # Name of the Log Same as PyName for individual log or name this to something else for a continual log
PyFunction = "Replicate incident tabular data exported from Spillman to NTGIS to do thematic mapping"     #IMPORTANT!!!: Purpose of the script.
ContinuousLog = False    #IMPORTANT!!!: Set to true for continual log file, False to delete existing log    
#********************************************************
# Defining Log files
errlog = "C:\\Users\\MyUserName\\ArcGis\\Python\\LogFiles\\" + PyName + "_Error.Log"
logFile = "C:\\Users\\MyUserName\\ArcGis\\Python\\LogFiles\\" + LogName + ".log"
# Removes Log File
if ContinuousLog == False:
    if os.path.exists(logFile)== True:
        os.remove(logFile)
        print ("Deleting existing log file " + logFile + "... Recreating " + logFile)
        print ("Running " + sys.argv[0])
else:
    print ("... Appending to existing log file..." + logFile )
# Set logger
x = logging.getLogger("logerror")
x.setLevel(logging.DEBUG)
# Creates Error Log
h1 = logging.FileHandler(errlog)
f = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
h1.setFormatter(f)
h1.setLevel(logging.DEBUG)
x.addHandler(h1)
logerror = logging.getLogger("logerror")
#Warning example logerror.warning(Variable + "\n REASON: Reason why it is a warning! \n")
def DeleteErrLog(): #Deletes error log if no errors are present
    closeLogger()
    if os.path.exists(errlog):
        if os.path.getsize(errlog) == 0:
            print ("No errors were found, removing" + errlog)
            os.remove(errlog)
        else:
            print ("Errors were found in the errlog. And " + errlog + "s size is "),
            print (os.path.getsize(errlog)),
            print ("bytes.")
def closeLogger():
    h1.close()
    h1.flush()
def GpMsg():
    arcpy.AddMessage("\n" + arcpy.GetMessages())
    print >> open(logFile, 'a'), "\n" + arcpy.GetMessages() + "\n"
    print "\n" + arcpy.GetMessages() + "\n"
def PyMsg(msg):
    arcpy.AddMessage("\n" + msg + " - " + str(time.ctime()))
    print >> open(logFile, 'a'), "\n" + msg + " - " + str(time.ctime())
    print "\n" + msg + " - " + str(time.ctime())
def DeleteIfExists(objectName):
    if arcpy.Exists(objectName):
        arcpy.Delete_management(objectName); GpMsg()
def py_mail(BODYMSG, SUBJECT, TO, FROM):
    TO = string.splitfields(TO, ",")
    BODY = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT ,
        "",
        BODYMSG
        ), "\r\n")
    # The actual sending of the e-mail
    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, BODY)
    server.quit()
#TODO: Add Local Variables Here
#******************************************************
ConnString = "C:\\Users\\MyUserName\\ArcGis\\ArcCatalog_Connections\\"
    DatabaseName = "WhatEverYouCallYourDatabase.sde"
DestinationWS = "C:\\Users\\MyUserName\\ArcGis\\Data\\YavapaiCountyData\\TargetFileGeodatabsaeName.gdb"
TempWS = "C:\\Users\\MyUserName\\ArcGis\\ArcGISPostProcess\\SourceFileGeodatabsaeName.gdb"
SourcePathTbl = "C:\\Users\\MyUserName\\ArcGis\\Data\\SourceFileGeodatabsaeName.gdb\\MyInciTableName_Data"
SourceWS = "C:\\Users\\MyUserName\\ArcGis\\Data\\SourceFileGeodatabsaeName.gdb"
SourceView = "TargetFileGeodatabsaeNameInciTableName_Data_View"
SourceTbl = "TargetFileGeodatabsaeNameInciTableName_Data"
AppendInput = SourceWS + "\\" + SourceTbl
DestinationTbl = "TargetFileGeodatabsaeNameInciTableNameAppend"
DestinationView = "TargetFileGeodatabsaeNameInciTableNameAppend_View"
AppendTarget = DestinationWS + "\\" + DestinationTbl
AppendSchemaType = "NO_TEST"
AppendfieldMappings = ""
#******************************************************
try:
    PyMsg("***********************************************************")
    PyMsg("*****  STARTING TO UPDATE " + PyFunction)
    PyMsg("*****  I am located at " + PyLocation)
    PyMsg("***********************************************************")
    #TODO: Add code to run here
    #******************************************************
    # Process: error checking for destination file geodatabase exists
    try:
      if arcpy.Exists(DestinationWS):
          PyMsg( "File Geodatabase found to append to source table.")
      else:
        logerror.warning(DestinationWS + "\n REASON: No File Geodatabase for appending source table. \n")
    except Exception, ex:
        PyMsg("Error while executing script  \n Please see error log. Located at " + errlog)
        logerror.exception(PyName)
    PyMsg("Make Table Views")
    # Process: Make Source Table View
    arcpy.MakeTableView_management (SourcePathTbl, SourceView, "", TempWS, ""); GpMsg()
    # Process: Make Destination Table View
    arcpy.MakeTableView_management (AppendTarget, DestinationView, "", TempWS, ""); GpMsg()
    PyMsg("Appending Table Views")
    # Process: Table to Table
    arcpy.Append_management(SourceView, DestinationView, AppendSchemaType, AppendfieldMappings, ""); GpMsg()
    
    
    #*******************************************************
    DeleteErrLog() #Deletes error log if no errors are present
    PyMsg("***********************************************************")
    PyMsg("***** COMPLETED SCRIPT " + PyFunction)
    PyMsg("***********************************************************")
except Exception, ex:
    PyMsg("Error while executing script. \n Please see error log. Located at " + errlog)
    logerror.exception(PyName)
    closeLogger()
    # TO EMAIL ERROR TO MailSendTO; YOU MUST DEFINE MailSendTO IN VARIABLES
    SUBJECT = "Error while executing script " + Fullname
    BODYMSG = "Error in " + str.upper(PyFunction) + ".  View error log at " + errlog
    py_mail(BODYMSG, SUBJECT, MailSendTO, MailSendFROM)
