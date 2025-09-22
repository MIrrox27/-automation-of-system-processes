@echo off
color 0A

reg export HKCU\Software\Microsoft\Windows backup.reg
echo Бэкап реестра создан: backup.reg

pause(15)