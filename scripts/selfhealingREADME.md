## This readme is for the script selfhealing.py which is a kubernetes feature
1. This script needs to be scheduled in a cron job over a period of time.
   Script should be added in the crontab file.
2. This scripts runs in the background and checks the health of the containers.
   If the containers are stopped, it will restart the containers.
   If the containers are deleted, it will recreate the containers from the latest committed image file. 
