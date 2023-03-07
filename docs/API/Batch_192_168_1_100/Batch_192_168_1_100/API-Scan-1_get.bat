@echo off
echo PRISMA PRO Scan-1 get
echo ====================
timeout /t 1 >nul
curl http://192.168.1.100/mmsp/measurement/scans/-1/get > Scan-1_Get.txt


cmd /V:On

