import ftplib
import os
import sys
from lxml import etree

playoutUser = "movie"
studioUser = "movie"
playoutSANMainIP = "192.168.4.230"
playoutSANBackupIP = "192.168.4.231"
studioSANIP = "192.168.66.72"
path = "c:/gxfs"
mediaids = []
titles = []
kept = []
latestXML = None # Filename of the last modified(lastest) .xml in specified folder

# Code to import the argument containing the location of the news for this script run.
try:
    location = sys.argv[1]
except IndexError:
    print "ERROR: Too few arguments."
    print "Usage: PB_Script.py <Location>. Eg: PB_Script.py Wollongong"
    sys.exit(1)

# takes the location from the argument provided and inserts this into a full path string to use
xmlFolder = "C:\PB_Playlists\\" + location + "_News\\"

# Finds the smallest(min) time since last modified from the file list(ie: the newest file)
try:
	latestXML = max(os.listdir(xmlFolder), key=lambda f: os.path.getctime("{}/{}".format(xmlFolder, f)))
except ValueError:
	print location + "_News has no files in the xml folder. EXITING"
	raise SystemExit
except OSError:
	print location + "_News folder does not exist. EXITING"
	raise SystemExit

# Create full path to the latest xml file in the directory
fullFilePath = xmlFolder + latestXML

# parse all xml into a element tree for storage and use
doc = etree.parse(fullFilePath)

# retrieve media id's from pebble xml
for event in doc.findall(".//{http://www.pebble.tv/playlist}event"):
    titles.append(event.findtext(".//{http://www.pebble.tv/playlist}title"))
    mediaids.append(event.findtext(".//{http://www.pebble.tv/playlist}mediaid"))

studio = "STUDIO"

for i, j in enumerate(titles):
    if "STUDIO" in str(j):
        kept.append(mediaids[i])
    if "INTRO" in str(j):
        kept.append(mediaids[i])

for each in kept:
    print each



# retrieve List of media from play-out SAN
# poftp is play-out SAN FTP object
# poftpfiles is array containing play-out SAN files

poftp = ftplib.FTP(playoutSANMainIP)
poftp.login(playoutUser, "")

try:
    poftp.cwd('default')
    poftpfiles = poftp.nlst()
    poftp.quit()
except ftplib.error_perm, resp:
    if str(resp) == "550 No files found":
        print "No files in this directory"
    else:
        raise

# compare PB XML and Play-out files - find the missing items

pbmlist = set(kept) - set(poftpfiles)
for missingFilesList in pbmlist:
        print missingFilesList



# retrieve List of media from studio SAN
# sftp is Studio SAN FTP object
# sftpfiles is array containing Studio SAN files

sftp = ftplib.FTP(studioSANIP)
sftp.login(studioUser, "")

try:
    sftp.cwd('default')
    sftpfiles = sftp.nlst()
    sftp.quit()
except ftplib.error_perm, resp:
    if str(resp) == "550 No files found":
        print "No files in this directory"
    else:
        raise

# compare PBMList and Studio files - find the missing items
print ""
print "Look List Below"
print ""


looklist = set(sftpfiles) & set(pbmlist)
for word in looklist:
    print word
'''
    try:
        sftp = ftplib.FTP(studioSANIP)
        sftp.login("movie", "")
        sftp.cwd('default')
        os.chdir(path)
        sftp.retrbinary("RETR " + word ,open(word + '.gxf', 'wb').write)
        sftp.quit()
    except ftplib.error_perm, resp:
        if str(resp) == "550 No files found":
            print "No files in this directory"
'''

def ftpconnect(address, username):
    try:
        ftplib.FTP(address)
    except Exception, e:
        print str(e)

