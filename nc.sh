snmpwalk -v 2c -c public 192.168.20.211 iso.3.6.1.2.1.2.1 | awk '{print $4}' > ex.txt
snmpwalk -v 2c -c public 192.168.20.211 iso.3.6.1.4.1.2021.4.5.0 | awk '{print $4}' >> ex.txt
snmpwalk -v 2c -c public 192.168.20.211 iso.3.6.1.4.1.2021.11.52.0 | awk '{print $4}' >> ex.txt
snmpwalk -v 2c -c public 192.168.20.211 iso.3.6.1.4.1.2021.9.1.6.1 | awk '{print $4}' >> ex.txt
snmpwalk -v 2c -c public 192.168.20.211 iso.3.6.1.2.1.1.1 | awk '{for(i=4;i<=NF;++i)printf "%s ", $i}' >> ex.txt
sort "ex.txt" | cat
rm -f ex.txt
