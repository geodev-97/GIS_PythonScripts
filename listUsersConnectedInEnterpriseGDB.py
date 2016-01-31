# THIS IS A PYTHON SCRIPT EXAMPLE TO LIST ALL THE USERS CONNECTED TO AN ENTERPRISE GEODATABASE
import arcpy, os, csv, logging, logging.handlers, time, string, sys, inspect, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# NEXT THREE VARIABLES NEEDED FOR EMAIL ERROR EVENTS
MailSendTO = 'youremail@domain.com'
MailSendFROM ='githubexampleuser@domain.net'
SERVER = 'MYwebmail'  #SMTP SERVER NAME

Fullname = os.path.basename(inspect.getfile(inspect.currentframe()))
PyName = os.path.splitext(Fullname)[0]      # Name of the Py script
PyLocation = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
#********************************************************
LogName = PyName #IMPORTANT!!!: Same log name for all basemap scripts
PyFunction = "LIST CURRENT CONNECTED USER TO ENTERPRISE GEODATABASE"
ContinuousLog = True #Set to true for continual log file
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
#Warning example logerror.warning(Varible + "\n REASON: Reason why it is a warning! \n")
def DeleteErrLog(): #Deletes error log if no errors are present
    closeLogger()
    if os.path.exists(errlog):
        if os.path.getsize(errlog) <= 1:
            print ("\nNo errors were found, removing" + errlog)
            os.remove(errlog)
            # TO EMAIL SUCCESSFULL TO MailSendTO; YOU MUST DEFINE MailSendTO IN VARIABLES
            SUBJECT = "Completed List Users In Database script " + Fullname
            BODYMSG = "Successfully Ran " + str.upper(PyFunction) + ".  View completed log at " + logFile
            py_mail(BODYMSG, SUBJECT, MailSendTO, MailSendFROM)
        else:
            print ("\nErrors were found in the errlog. And " + errlog + "s size is "),
            print (os.path.getsize(errlog)),
            print ("bytes.")
def closeLogger():
    h1.close()
    h1.flush()
def GpMsg():
    print "\n" + arcpy.GetMessages() + "\n"
    arcpy.AddMessage("\n" + arcpy.GetMessages())
    print >> open(logFile, 'a'), "\n" + arcpy.GetMessages() + "\n"
def PyMsg(msg):
    print "\n" + msg + " - " + str(time.ctime())
    arcpy.AddMessage("\n" + msg + " - " + str(time.ctime()))
    print >> open(logFile, 'a'), "\n" + msg + " - " + str(time.ctime())
def make_table_and_count(table,searchstring):
    arcpy.MakeTableView_management(table,"TableViewCount",searchstring)
    x = int(str(arcpy.GetCount_management("TableViewCount")))
    return x
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
try:
    PyMsg("***********************************************************")
    PyMsg("*********Starting program**************")
    PyMsg("***********************************************************")
    ConnString = "C:\\Users\\MyUserName\\ArcGis\\\\ArcCatalog_Connections\\"
    DatabaseName = "WhatEverYouCallYourDatabase.sde"
    Database = ConnString + DatabaseName
    try:
        users = arcpy.ListUsers(Database)

        cfilename = DatabaseName + "_Connections.csv"
        file = "C:\\Users\\MyUserName\\ArcGis\\logFiles\\" + cfilename #defualts to the log file location on ntgisd, change this to any other folder location for the logs
        ofile = open(file,'a')
        cfile = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        cfile.writerow([str(time.ctime()),"UserName","Session ID","Direct Connection","Client Machine","DateTime"])
        if users.count <> 0:
            for user in users:
                PyMsg("Reviewing...\n    " +"Username: {0}, Session Id: {1}, Connection Type: {2}, Client Name: {3}, Connected at: {4}".format(user.Name, user.ID, user.IsDirectConnection, user.ClientName, user.ConnectionTime))
                row =[]
                row.extend(["",user.Name, user.ID, user.IsDirectConnection, user.ClientName, user.ConnectionTime])
                cfile.writerow(row)
        ofile.close()
    except Exception, ex:
        ofile.close()
        PyMsg("Error while executing script. " + str(cfilename) + " \n Please see error log. Located at " + errlog)
        logerror.exception(PyName)
    DeleteErrLog() #Deletes error log if no errors are present
    PyMsg("***********************************************************")
    PyMsg("#### SCRIPT COMPLETED" )
    PyMsg("***********************************************************")
except Exception, ex:
    PyMsg("Error while executing script. Third Section \n Please see error log. Located at " + errlog)
    logerror.exception(PyName)
    closeLogger()
    # TO EMAIL ERROR TO MailSendTO; YOU MUST DEFINE MailSendTO IN VARIABLES
    SUBJECT = "Error while executing script " + Fullname
    BODYMSG = "Error in " + str.upper(PyFunction) + ".  View error log at " + errlog
    py_mail(BODYMSG, SUBJECT, MailSendTO, MailSendFROM)
