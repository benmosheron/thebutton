echo -n "ssh ben@" > ssh-ben.sh
ping -c 1 raspberrypi.local | grep -oE "\d\d\d\.\d\d\d.\d\.\d\d\d" | tail -1 >> ssh-ben.sh
chmod u+x ssh-ben.sh
./ssh-ben.sh