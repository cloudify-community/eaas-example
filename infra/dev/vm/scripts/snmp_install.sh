#!/bin/bash
sudo ufw disable
sudo apt-get install -y snmpd
sudo service snmpd stop
echo "syslocation Unknown
syscontact Root <root@localhost>
dontLogTCPWrappersConnects yes
view CloudifyMonitoringView included .1.3.6.1.4.1.2021
createUser ${snmp_user} SHA ${snmp_pass} AES ${snmp_pass}
rouser ${snmp_user} priv -V CloudifyMonitoringView
disk / 
proc nginx
proc systemd" | sudo tee /etc/snmp/snmpd.conf
sudo service snmpd restart
sudo systemctl enable snmpd
