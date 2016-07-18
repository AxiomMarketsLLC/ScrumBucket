#ScrumBucket
##version 0.1.0

##Description
ScrumBucket is a Python 2 app for imaging our scrum board that uses Amazon S3 for storage.

##Hardware

* Raspberry Pi 2 w/ 2.8" Touchscreen
* Canon PowerShot SX510HS (w/ chdk firmware)

##Design Summary

Our Python application uses the **chdk-ptp** command line utility to control the camera over USB.  An event handler built with the **watchdog** python module watches a target directory for new image files; if one is detected, it is uploaded to a designated Amazon S3 bucket using Amazon's **boto3** module.  Our simple UI for the touchscreen is made with **Tkinter**.
 
ScrumBucket was developed during a summer internship @ [Axiom Markets, LLC](http://axiommarkets.com).

##Licensing
Available under MIT license; see LICENSE.md.

##Release Notes

*  Amazon S3 functionality requires credentials to be stored either as 1) environment variables or 2) on the filesystem, at **~/aws/credentials**.  See [this page](http://boto3.readthedocs.io/en/latest/guide/configuration.html) for details.

+ To launch on desktop startup, add a line to **/etc/xdg/lxsession/LXDE-pi/autostart** to launch the script, e.g. @lxterminal --command "/home/pi/scrum_bucket.py"
 







