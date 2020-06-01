#!/bin/sh

PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo $PROJECT_ROOT

#install prereqs
pip3 install zeroconf

sudo rm /etc/systemd/system/bonjour_service.service

#add create script service
sudo echo "[Unit]"                                      >> /etc/systemd/system/bonjour_service.service
sudo echo "Description=Broadcasts this devices IP address, hostname, and hardware type as a mDNS device."
                                                        >> /etc/systemd/system/bonjour_service.service
sudo echo "After=network.target"                        >> /etc/systemd/system/bonjour_service.service

sudo echo "[Service]"                                   >> /etc/systemd/system/bonjour_service.service
sudo echo "ExecStart=/usr/bin/python3 -u bonjour_service.py"  >> /etc/systemd/system/bonjour_service.service
sudo echo "ExecStop=/bin/systemctl kill bonjour_service"      >> /etc/systemd/system/bonjour_service.service
sudo echo "WorkingDirectory=$PROJECT_ROOT"    >> /etc/systemd/system/bonjour_service.service
sudo echo "StandardOutput=inherit"                      >> /etc/systemd/system/bonjour_service.service
sudo echo "StandardError=inherit"                       >> /etc/systemd/system/bonjour_service.service
sudo echo "Restart=always"                              >> /etc/systemd/system/bonjour_service.service
sudo echo "User=root"                                   >> /etc/systemd/system/bonjour_service.service

sudo echo "[Install]"                                   >> /etc/systemd/system/bonjour_service.service
sudo echo "WantedBy=multi-user.target"                  >> /etc/systemd/system/bonjour_service.service

sudo systemctl daemon-reload
sudo systemctl start bonjour_service.service
sudo systemctl enable bonjour_service.service

#print instruction messages
echo ""
echo "To change the device identifiers edit lines 12 and 13 in bonjour_service.py"
echo "Plese reboot for changes to take effect."
