import sys,getopt,os,string

authorize_conf_file = '/home/pi/authorize_conf'
authorizeconf = open ( authorize_conf_file, 'w')

authorized_macs_file = '/home/pi/authorized_macs'
authorizedmacs = open (authorized_macs_file,'w')

dnsfile = open('/etc/dnsmasq.d/sensimedia.dns', 'r')

for line in dnsfile:
        if (line.find('dhcp-host') > -1):
                hostline = line.split(",")[0]
                hostline = hostline.split("=")[1]
                vlanid = line.split(",")[1]
                vlanid = vlanid.split(":")[-1]
                vlanid = vlanid.replace("vlan","")
                myline = hostline.replace(":","")
                u = myline.upper()
                myline= u.lower()
                myresult= "-".join(["%s%s" % (u[i], u[i+1]) for i in range(0,12,2)])

                authorizedmacs.write (str(myresult)+'\n')
                authorizedmacs.write ('\t'+'Reply-Message = "Device with MAC Address %{Calling-Station-Id}
 authorized for network access"\n')
                authorizeconf.write (str(myline) + '\tCleartext-Password :=\t' + '\"' + str(myline) +'\"\n
')
                authorizeconf.write ('\t\t' + 'Tunnel-Type = "VLAN",\n')
                authorizeconf.write ('\t\t' + 'Tunnel-Medium-Type = "IEEE-802",\n')
                authorizeconf.write ('\t\t' + 'Tunnel-Private-Group-ID = "'+ str(vlanid) +'"\n')
                authorizeconf.write ('\t\t' + 'Auth-Type := local\n')
                authorizeconf.write ('\n')

dnsfile.close()

authorizedmacs.close()
authorizeconf.close()
