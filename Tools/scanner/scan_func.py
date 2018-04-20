import netifaces
from coffee_lib.interface import coffee_util as util

def get_interface():
    print("Select the interface you want to use\n")

    interface_list = netifaces.interfaces()

    for x in range(len(interface_list)):
        print("\t" + str(x+1) +")\t" + str(interface_list[x]))

    print("\n\n")
    
    while True:
        select = ""
        select = input("Coffee < ")

        if len(select.split()) == 2:
            if(select.split()[0] == "use" and select.split()[1].isdigit()):
                select = int(select.split()[1])
            else:
                print(util.color("It is not Available command", warning=True))
                continue
        elif select.isdigit():
            select = int(select)
        else:
            if select.startswith("help"):
                print("Coffee > You need to type number")
                continue
            else:
                print(util.color("It is not Available command", warning=True))
                continue

        if 0 < select <= len(interface_list):
            return interface_list[select-1]
        else:
            print("Coffee > " + util.color("It is not Availabe!!!",warning=True)+"\n")
            print("Coffee > Select Again")
            print("Coffee > If you need Help, Type help")
    
def get_range(interface, ip):
    netmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]["netmask"]
    cidr = sum((bin(int(x)).count("1")) for x in str(netmask).split("."))
    ip = ".".join(ip.split(".")[:-1]) + ".0"
    return "{}/{}".format(ip, cidr)

def scan_single(nm, target_ip, custom_option):
    res_scan = {}
    result = nm.scan(hosts=target_ip, arguments='-sS -O -sV '+custom_option)

    info = result['scan'][target_ip]
    try:
        mac = info['addresses']['mac']
    except KeyError:
        mac = "Unknown MAC"
    try:
        vendor = info['vendor'][mac.upper()]
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
                    service_version = "Unkwnon Version"
                open_ports[port] = {"service":service, "version":service_version}
            except KeyError:
                open_ports[port] = None
                continue
    except KeyError:
        open_ports = None

    res_scan = {"mac":mac, "name":name, "vendor":vendor,"os":os_list, "open_ports":open_ports}
    return res_scan


def print_info(interface, ip, gateway_ip, ip_range):
    cidr = ip_range.split("/")[1]
    print("Selected Interface\t:\t" + util.color(interface))
    print("Local IP Address\t:\t" + util.color(ip))
    print("Gateway IP Address\t:\t" + util.color(gateway_ip))
    print("\n")

def print_hostscan(hosts):
    print("Coffee > Here is Host Scan List, Friends\n")

    print("="*80)
    print("{:^15}{:^35}{:^35}".format('ip', 'mac', 'vendor'))
    for host in sorted(hosts.keys()):
        print("{:^15}{:^35}{:^35}".format(host, hosts[host]['mac'], hosts[host]['vendor']))
    print("="*80)
    print()

def print_detailscan(hosts):
    print("="*80)
    print("{:^15}{:^20}{:^20}{:^20}".format('ip', 'mac', 'vendor','os'))
    for host in sorted(hosts.keys()):
        os_info = []
        try:
            for os_name in hosts[host]['os']:
                if os_name[0] not in os_info:
                    os_info.append(os_name[0])
            os_info = ",".join(os_info)
        except KeyError:
            os_info = ""

        print("{:^15}{:^20}{:^20}{:^20}".format(host, hosts[host]['mac'], hosts[host]['vendor'],os_info)) 
    print("="*80)

def print_service(service_data):
    open_port = service_data["open_ports"]
    if open_port == None:
        print("Coffee > " + util.color("It has no open ports"))
        return

    print("="*80)
    print("{:^10}{:^20}{:^30}".format('port', 'service', 'version'))
    print()
    for port_num in open_port:
        print("{:^10}{:^20}{:^35}".format(str(port_num), open_port[port_num]['service'], open_port[port_num]['version']))
    print("="*80)
    print()

