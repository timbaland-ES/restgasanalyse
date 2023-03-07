@echo off
echo PRISMA PRO Login get
echo ====================
timeout /t 1 >nul
curl 192.168.1.100/mmsp/communication/login/get > login_Get.txt


cmd /V:On

