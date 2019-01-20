# --------------------------------------------------------------------------------
# Script to add fields to ArcSDE feature class.
# If directories already exist, they are not are created
# Created by: Abdul Syed
# Date of creation: 1/11/2019
# --------------------------------------------------------------------------------


import sys, string, os, datetime
import errno
import shutil

# Set the necessary product code
#import arceditor


# Import arcpy module
import arcpy

# Local variables:

#Target database info
TargerConnFile= config.TargerConnFile
TargetServer=config.TargetServer
TargetService=config.TargetService
TargetDatabase=config.TargetDatabase
TargetUser=config.TargetUser
TargetPassword=config.TargetPassword
TargetLayer=config.TargetLayer

#Input and Output location paths
ProdDir=config.ProdDir
InputLoc=ProdDir + "\\" + TargerConnFile + ".sde"
Logfile=ProdDir + "\\" + "Add_" + TargerConnFile + ".log"
# Set local variables
inFeatures = TargetLayer


#Create directories Connfiles

print "\nCreating Connection file directory %s" % ProdDir

try:
    os.makedirs(ProdDir)
    print "\nConnection file directory created"
except OSError as exception:
    if exception.errno != errno.EEXIST:
        raise
    else:
        print "\nConnfile directory %s already exists." % ProdDir

class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)

if os.path.isfile(Logfile) == True:
	os.remove(Logfile)
	f = open(Logfile, 'w')
	original = sys.stdout
	sys.stdout = Tee(sys.stdout, f)
	print "Log file created at %s" % ProdDir
else:
	f = open(Logfile, 'w')
	original = sys.stdout
	sys.stdout = Tee(sys.stdout, f)
	print "Log file created at %s" % ProdDir

now=datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")

print "Start time: "
print str(now)

print "\nCreating ArcSDE Connection File for target database"

try:
	# Process: Create ArcSDE Connection File
	if os.path.isfile(InputLoc) == False:
		arcpy.CreateArcSDEConnectionFile_management(ProdDir, TargerConnFile, TargetServer, TargetService, TargetDatabase, "DATABASE_AUTH", TargetUser, TargetPassword, "SAVE_USERNAME", "sde.DEFAULT", "DO_NOT_SAVE_VERSION")

	print "\nArcSDE Connection File created for target database"

	# Set environment settings
	arcpy.env.workspace = InputLoc

	FieldList=config.FieldList
	For Field in FieldList:

		# Execute AddField
		print "\nAdding " + Field
		arcpy.AddField_management(inFeatures,Field.Name,Field.Type,,,"",Field.Name,"NULLABLE","NON_REQUIRED")
	
		now=datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")

		print "\nFields added successfully: "
		print "\nEnd time: "
		print str(now)

except:
	print arcpy.GetMessages()

f.close()