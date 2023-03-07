@echo off
echo PRISMA PRO Recipe MID Chn 1 + 2 on 192.168.1.100
echo ================================================
timeout /t 1 >nul
curl 192.168.1.100/mmsp/scanSetup/channel/1/channelMode/set?Single
curl 192.168.1.100/mmsp/scanSetup/channel/1/startMass/set?14
curl 192.168.1.100/mmsp/scanSetup/channel/1/dwell/set?32
curl 192.168.1.100/mmsp/scanSetup/channel/1/ppamu/set?4
curl 192.168.1.100/mmsp/scanSetup/channel/1/enabled/set?True
curl 192.168.1.100/mmsp/scanSetup/channel/2/channelMode/set?Single
curl 192.168.1.100/mmsp/scanSetup/channel/2/startMass/set?28
curl 192.168.1.100/mmsp/scanSetup/channel/2/dwell/set?32
curl 192.168.1.100/mmsp/scanSetup/channel/2/ppamu/set?4
curl 192.168.1.100/mmsp/scanSetup/channel/2/enabled/set?True
curl 192.168.1.100/mmsp/scanSetup/startChannel/set?1
curl 192.168.1.100/mmsp/scanSetup/stopChannel/set?2
curl 192.168.1.100/mmsp/scanSetup/scanCount/set?4

cmd /V:On