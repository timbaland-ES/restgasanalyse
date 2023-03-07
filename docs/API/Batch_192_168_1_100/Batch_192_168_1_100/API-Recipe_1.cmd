cmd ON
@echo off
echo PRISMA PRO Recipe 1 
echo =================== 

sleep 5
curl 192.168.1.100/mmsp/scanSetup/channel/1/channelMode/set?Sweep
curl 192.168.1.100/mmsp/scanSetup/channel/1/startMass/set?0
curl 192.168.1.100/mmsp/scanSetup/channel/1/stopMass/set?30
curl 192.168.1.100/mmsp/scanSetup/channel/1/dwell/set?32
curl 192.168.1.100/mmsp/scanSetup/channel/1/ppamu/set?4
curl 192.168.1.100/mmsp/scanSetup/channel/1/enabled/set?True
curl 192.168.1.100/mmsp/scanSetup/startChannel/set?1
curl 192.168.1.100/mmsp/scanSetup/stopChannel/set?1
curl 192.168.1.100/mmsp/scanSetup/scanCount/set?4

