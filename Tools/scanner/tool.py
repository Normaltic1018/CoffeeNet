import sys, os, re
from coffee_lib.interface import message
from Tools.scanner.scan_func import *
import netifaces, nmap

version = "1.0"

class Tools():
    def __init__(self, cli_option=None):
        self.tool_name = "Scanner"
        self.custom_option =""
        self.description = """
        This Tool is For use Scan Network
        You can find Alive Hosts in your network by using this tools
        And You can also see which ports are open
        This Scanner Tools works with nmap.
        If you want to use it, type \"use scanner\"
        """ 
        self.db_help_msg = """
        ** DB USAGE **
        service [IP]
        ex) service 192.168.0.1
        if you just type "service", All IP Service Information show

        host
        Just type "host", then you can see the simple host information list
        """
        self.hosts = {}
        self.menu_commands = {
                "db":"See the hosts you found",
                "scan":"Scan Network",
                "back":"Go to main CoffeeNet menu",
                "exit":"Exit CoffeeNet"}
        self.scan_commands ={
                "host" : "Scan Alive Hosts",
                "detail":"Get Detail Information",
                "custom":"Set Custom Option",
                "back" : "Go to Scanner Menu",
                "exit":"Exit CoffeeNet"}
        self.db_commands = {
                "host" : "See the hosts list you found",
                "service": "Check Open Service",
                "back" : "Go to Scanner Menu",
                "help" : "About db menu",
                "exit" : "Exit CoffeeNet"
        }
        
        return

    def main_menu(self):
        title_show = True
        menu_command = ""
        
        os.system("clear")
        self.interface = get_interface()

        self.local_ip = netifaces.ifaddresses(self.interface)[netifaces.AF_INET][0]['addr']
        self.gateway_ip = netifaces.gateways()["default"][netifaces.AF_INET][0]
        self.ip_range = get_range(self.interface, self.local_ip)
        nm = nmap.PortScanner()

        while menu_command =="":
            if title_show:
                message.tool_title(self.tool_name, version)
                print_info(self.interface, self.local_ip, self.gateway_ip, self.ip_range)

                print(util.color(" [#] Available Commands: \n"))
                for command in list(self.menu_commands.keys()):
                    print("\t"+ util.color(command)+"\t\t\t"+ self.menu_commands[command])

                print("\n")

            menu_command = input("Coffee < ").strip()

            if menu_command.startswith('back'):
                break
            elif menu_command.startswith('scan'):
                self.scan_menu(nm)
                menu_command = ""
            elif menu_command.startswith('db'):
                self.db_menu(nm)
                menu_command = ""
                title_show = False
            elif menu_command == "":
                title_show = True
            elif menu_command == "exit":
                print("\n\n" + util.color("Exit CoffeeNet... Have a Good Day!",warning=True))
                sys.exit()
            else:
                print("Coffee > " + util.color("Wrong Command!", warning=True))
                title_show = False
                menu_command = ""
            title_show = True

        return

    def scan_menu(self, nm):
        title_show = True
        scan_command = ""
        while scan_command == "":
            if title_show:
                message.tool_title(self.tool_name, version)
                print_info(self.interface, self.local_ip, self.gateway_ip, self.ip_range)
                print("Target Network\t:\t" + util.color(self.ip_range))
                print("Custom Option\t:\t" + util.color(self.custom_option) + "\n")
                print(util.color(" [#] Available Commands: \n"))
                for command in list(self.scan_commands.keys()):
                    print("\t"+ util.color(command)+"\t\t\t"+ self.scan_commands[command])

                print("\n")

            scan_command = input("Coffee < ")
            
            if scan_command.startswith('host'):
                print("Coffee > Nmap Scan Start...")
                try:
                    result = nm.scan(hosts=self.ip_range, arguments='-n -sP -PE -PA21,23,80,3389 '+self.custom_option)
                except:
                    print("Coffee > " + util.color("Error During Scan",warning=True))
                    print("Coffee > I will remove custom options")
                    self.custom_option = ""
                    scan_command = ""
                    title_show = False
                    continue

                for _, info in result['scan'].items():
                    if info['status']['state'] == 'up':
                        ip = info['addresses']['ipv4']
                        try:
                            mac = info['addresses']['mac']
                        except KeyError:
                            mac = "Unknown MAC"
                        try:
                            vendor = info['vendor'][mac.upper()]
                        except KeyError:
                            vendor = "Unknown Vendor"
                    
                        name = "Unknown"
                        os_list = []
                        open_ports = {}
                        if not ip in self.hosts:
                            self.hosts[ip] = {"mac":mac,"name": name, "vendor": vendor, "os": os_list, "open_ports": open_ports}
                print("Coffee > Here is Host Scan List, Friends\n")
                print_detailscan(self.hosts)
            
                print("Coffee > Check it?")
                input("Coffee < ")
                title_show = False

            elif scan_command.startswith("detail"):
                done = False    # to check scan complete
                if(len(scan_command.split()) == 2):
                    ip_input = scan_command.split()[1]
                    res_ip = re.findall("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", ip_input)
                    if len(res_ip) != 0:
                        try:
                            res_info = scan_single(nm, res_ip[0], self.custom_option)
                        except:
                            print("Coffee > " + util.color("Error During Scan",warning=True))
                            print("Coffee > I will remove custom options")
                            self.custom_option = ""
                            scan_command = ""
                            title_show = False
                            continue
                        
                        mac = res_info["mac"]
                        name = res_info["name"]
                        vendor = res_info["vendor"]
                        os_list = res_info["os"]
                        open_ports = res_info["open_ports"]
                        self.hosts[res_ip[0]] = {"mac":mac, "name":name, "vendor":vendor, "os":os_list, "open_ports":open_ports}
                        done = True
                    else:
                        print("Coffee > "+util.color("It is not IP format.", warning=True))

                if len(self.hosts) == 0:
                    print("Coffee > You don't have any hosts ip address")
                    print("Coffee > Enter What IP do you want to scan?")
                    print("Coffee > Do not add netmask")
                    ip_input = input("Coffee < ")
                    res_ip = re.findall("^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)", ip_input)
                    if len(res_ip) != 0:
                        try:
                            res_info = scan_single(nm, res_ip[0], self.custom_option)
                        except:
                            print("Coffee > " + util.color("Error During Scan",warning=True))
                            print("Coffee > I will remove custom options")
                            self.custom_option = ""
                            scan_command = ""
                            title_show = False
                            continue
                        mac = res_info["mac"]
                        name = res_info["name"]
                        vendor = res_info["vendor"]
                        os_list = res_info["os"]
                        open_ports = res_info["open_ports"]
                        self.hosts[res_ip[0]] = {"mac":mac, "name":name, "vendor":vendor, "os":os_list, "open_ports":open_ports}
                        done = True
                    else:
                        print("Coffee > "+util.color("It is not IP format.", warning=True))

                if(done):
                    print("Coffee > Here is Detail Scan List, Friends\n")
                    print_detailscan(self.hosts)
                    print("Coffee > Check it?")
                    input("Coffee < ")
                    title_show = False
                    continue

                total_ip = len(self.hosts)
                print("Coffee > I will scan {} IP Addresses".format(total_ip))
                count = 0
                for ip in list(self.hosts):
                    try:
                        result = nm.scan(hosts=ip, arguments='-sS -O -sV -T5 '+self.custom_option)
                    except:
                        print("Coffee > " + util.color("Error During Scan",warning=True))
                        print("Coffee > I will remove custom options")
                        self.custom_option = ""
                        scan_command = ""
                        title_show = False
                        break

                    mac = self.hosts[ip]['mac']
                    vendor = self.hosts[ip]['vendor']

                    for _, info in result['scan'].items():
                        try:
                            if mac == "Unknown MAC" and info['addresses']['mac'] != "":
                                mac = info['addresses']['mac']
                        except KeyError:
                                mac = "Unknown MAC"
                        try:
                            if vendor == "Unknown Vendor" and info["vendor"][mac.upper()] != "":
                                vendor = info["vendor"][mac.upper()]
                        except KeyError:
                            vendor = "Unknown Vendor"
                        name = info["hostnames"][0]["name"]
                        if not name:
                            name = "Unknown Name"

                        try:
                            osmatch = info["osmatch"]
                            os_list = []
                            for os in osmatch:
                                for x in os["osclass"]:
                                    try:
                                        os_list.append([x["osfamily"], x["osgen"]])
                                    except KeyError:
                                        continue
                        except KeyError:
                            os_list = None

                        try:
                            open_ports = {}
                            for port in info["tcp"]:
                                try:
                                    service = info["tcp"][port]["name"]
                                    service_version = info["tcp"][port]["product"] + " " + info["tcp"][port]["version"]
                                    if info["tcp"][port]["extrainfo"] != "":
                                        service_version += " ({})".format(info["tcp"][port]["extrainfo"])
                                    if service_version.strip() == "":
                                        service_version = "Unknown Version"
                                    open_ports[port] = {"service":service,"version":service_version}
                                except KeyError:
                                    open_ports[port] = None
                                    continue
                        except KeyError:
                            open_ports = None
                        count += 1
                        print("Coffee > {} is scan complete. Workload({}/{})".format(ip,count, total_ip))
                        self.hosts[ip] = {"mac":mac,"name": name, "vendor": vendor, "os": os_list, "open_ports": open_ports}
               
                print("Coffee > Here is Detail Scan List, Friends\n")
                print_detailscan(self.hosts)
                print("Coffee > Check it?")
                input("Coffee < ")
                title_show = False
            elif scan_command == "custom":
                print("Coffee > What you want to Set Custom Option?")
                print("Coffee > "+ util.color("If you don't know Exactly, Do not Use This Options",warning=True))
                self.custom_option = input("Coffee < ")

                print("Coffee < Complete to Set Custom Options : " + util.color(self.custom_option))
                print("Coffee > Check it?")
                input("Coffee < ")
                title_show = False
            elif scan_command == "back":
                break
            elif scan_command == "exit":
                print("\n\n" + util.color("Exit CoffeeNet... Have a Good Day!",warning=True))
                sys.exit()
            elif scan_command == "":
                title_show = True
            else:
                print("Coffee > " + util.color("Wrong Command!", warning=True))
                title_show = False
                scan_command = ""
            #title_show = True
            

    def db_menu(self, nm):
        title_show = True
        db_command = ""
        while db_command == "":
            if title_show:
                message.tool_title(self.tool_name, version)
                print_info(self.interface, self.local_ip, self.gateway_ip, self.ip_range)
                print(util.color(" DataBase of Scanner"))
                print(" List : " + util.color(str(len(self.hosts))))
                print(util.color(" [#] Available Commands: \n"))
                for command in list(self.db_commands.keys()):
                    print("\t"+ util.color(command)+"\t\t\t"+ self.db_commands[command])

                print("\n")

            db_command = input("Coffee < ")
            
            if db_command.startswith('host'):
                if len(self.hosts) == 0:
                    print("Coffee > " + util.color("Empty Data!", warning=True))
                    print("Coffee > Please Scan First")
                else:
                    print_detailscan(self.hosts)

                title_show = False
                db_command = ""
            elif db_command.startswith("service"):
                title_show = False
                if len(db_command.split()) == 1:
                    # none arguments
                    print("\nCoffee > Here is the Whole Servie List, Friends\n")
                    for ip in sorted(self.hosts):
                        print("IP : " + util.color(ip))
                        service_data = self.hosts[ip]
                        print_service(service_data)
                elif len(db_command.split()) == 2:
                    # 1 IP arguments
                    # search IP(argu) in self.hosts, self.hosts is db
                    ip_arg = db_command.split()[1]
                    if not ip_arg in self.hosts:
                        print("Coffee > " + util.color("I don't have" + str(ip_arg) + " Information", warning=True))
                    else:
                        #service print
                        print("\nCoffee > Here is the Servie List, Friends\n")
                        print("IP : " + util.color(ip_arg))
                        service_data = self.hosts[ip_arg]
                        print_service(service_data)

                db_command = ""
            elif db_command.startswith("help"):
                print(self.db_help_msg)
                db_command = ""
                title_show = False
            elif db_command.startswith("back"):
                break
            elif db_command == "exit":
                print("\n\n" + util.color("Exit CoffeeNet... Have a Good Day!",warning=True))
                sys.exit()
            else:
                title_show = True
                db_command = ""
