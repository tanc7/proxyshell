#/usr/bin/python
#coding=utf-8
import os, sys, socket, operator, threading, subprocess
print """
Welcome to ProxyShell. Easy mode pivoting.
"""
def menuparser(options):
    options = options.splitlines()
    counter = 1
    for option in options:
        option = str(option.encode('utf-8')).strip().rstrip()
        print "\t{}. \t{}".format(str(counter),str(option))

        counter += 1
    return
def bash_cmd(cmd):
    commands = cmd.splitlines()
    for command in commands:
        command = str(command.encode('utf-8')).rstrip().strip()
        subprocess.call(command,shell=True,executable='/bin/bash')
    return

def popen_background(cmd):
    p = Popen(cmd,shell=True,executable='/bin/bash',stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    o = p.stdout.read()
    output = str(o.encode('utf-8')).strip().rstrip()
    return output

def ssh_commands():
    return

def netcat_commands():
    return

def ncat_commands():
    return

def Weavely_setup():
    return

def reverse_shells():
    return

def streisand():
    return
### Starting with this function, start splitting the app up into multiple modules because large py files are really hard to handle, especially if they use the same variables
def tsocks_proxychains():
    return


# UFW module
#ufw insert 1 allow in from 10.0.0.1 port 443 to 10.0.0.0/24 port 4444 comment 'test'

def get_allowdeny():
    options = """Allow (in and out)
    Allow (in)
    Allow (out)
    Deny (in and out)
    Deny (in)
    Deny (out)"""

    menuparser(options)

    opt_choice = int(raw_input("Enter a option (a number): "))

    if opt_choice == 1:
        allowdeny = "allow"
    elif opt_choice == 2:
        allowdeny = "allow in"
    elif opt_choice == 3:
        allowdeny = "allow out"
    elif opt_choice == 4:
        allowdeny = "deny"
    elif opt_choice == 5:
        allowdeny = "deny in"
    elif opt_choice == 6:
        allowdeny = "deny out"
    else:
        os.system('clear')
        get_allowdeny()

    print "Selected: ",allowdeny
    return allowdeny


def get_hostrange():
    hostrange = str(raw_input("Enter the IP address of a single host, OR the CIDR range of the subnet (192.168.1.0/24 for example): ")).strip().rstrip()
    print "DEBUG: ",hostrange
    return hostrange
def get_options():
    protocol = ''
    interface = ''
    protocol = str(raw_input("Enter a protocol you wish to specify to block/allow (tcp or udp) or leave EMPTY: ")).strip().rstrip()
    interface = str(raw_input("Enter a interface you wish to specify to block/allow (tcp or udp) or leave EMPTY: ")).strip().rstrip()

    # proto tcp OR proto udp
    if protocol != '' or None:
        protocol_statement = "proto {}".format(str(protocol))
    # on eth0 OR on wlan0
    if interface != '' or None:
        interface_statement = "on {}".format(str(interface))

    options = "{} {}".format(
        str(protocol_statement),
        str(interface_statement)
    )

    print "DEBUG: ",options
    return options

def get_portrange():
    portrange = str(raw_input("Enter the port(s) you wish to allow/block or LEAVE EMPTY: ")).strip().rstrip()
    if portrange != '' or None:
        portrange = "port {}".format(str(portrange))
    print "DEBUG: ",portrange
    return portrange
def get_comments():
    comments = str(raw_input("Enter any comments you would like to add or LEAVE EMPTY: ")).strip().rstrip()
    if comments != '' or None:
        comments = "'{}'".format(str(comments))
    print "DEBUG: ",comments
    return comments

def ufw_run_queued_commands(ufw_queued_commands):
    for line in ufw_queued_commands:
        cmd = str(line.encode('utf-8')).rstrip().strip()
        bash_cmd(cmd)
    return
def ufw_build_command_list(ufw_list_commands):
    ufw_queued_commands = []
    for command in ufw_list_commands:
        ufw_queued_commands.append[command]
    # resets the entire ufw table right before it runs the new commands
    return ufw_queued_commands

def ufw_add_statement():

    # We are SUPPOSED TO make it where the user CHOOSES where on the table the rule goes. Usually it's ALLOW on the top and DENY on the bottom.
    index = 1
    ufw_list_commands = []
    allowdeny = get_allowdeny()
    from_hostrange = get_hostrange()
    from_options = get_options()
    from_portrange = get_portrange()
    to_hostrange = get_hostrange()
    to_options = get_options()
    to_portrange = get_portrange()
    comments = get_comments()
    # lines = paragraph.splitlines()
#{ufw_first_statement}

# this needs to be fixed. The user is supposed to keep adding new lines until he says stop.

    # This is the SECOND function. It'll read the first list of statements and run them in order
    for line in lines:
        ufw_command_2nd_half = """{} from {} {} {} to {} {} '{}'""".format(
            str(allowdeny),
            str(from_hostrange),
            str(from_options),
            str(from_portrange),
            str(to_hostrange),
            str(to_options),
            str(to_portrange),
            str(comments)
        )
        ufw_first_statement = "ufw insert {} ".format(str(index))
        ufw_command = "{}{}".format(str(ufw_first_statement),str(ufw_command_2nd_half))
        print "DEBUG: ",ufw_command
        ufw_command = str(ufw_command.encode('utf-8')).strip().rstrip()
        ufw_list_commands.append[ufw_command]
        index += 1
        return ufw_list_commands

def ufw_iptables():
    ufw_list_commands = ufw_add_statement()
    ufw_queued_commands = ufw_build_command_list(ufw_list_commands)
    bash_cmd("ufw reset")
    ufw_run_queued_commands(ufw_queued_commands)
    return ufw_list_commands

# Routing module
def get_gw():
    gw = str(raw_input("Enter the NAT-Gateway you are trying to reach: "))
    return gw
def get_subnet():
    subnet = str(raw_input("Enter the subnet (network range) you are trying to connect to the gateway: "))
    return subnet

def get_iface():
    iface = str(raw_input("Enter the Network Interface you are linking it up with: "))
    return iface

def get_netmask():
    netmask = str(raw_input("Enter the netmask (range of adjacent addresses you are trying to restrict): "))
    return netmask

def get_host():
    host = str(raw_input("Enter the HOST (single IP address) you are adding to another network or peer: "))
    return host

def build_cmd_string(option_selected, gw, subnet, iface, netmask, host):

    add_default_gateway = "route add default gw {0} dev {1} metric 1".format(
        str(gw),
        str(iface)
    )
    add_subnet = "route add -net {0} netmask {1} gw {2} dev {3} metric 1".format(
        str(subnet),
        str(netmask),
        str(gw),
        str(iface)
    )
    add_regular_gateway = "route add gw {0} dev {1} metric 1".format(
        str(gw),
        str(iface)
    )
    add_host = "route add -host {0} gw {1} dev {2} metric 1".format(
        str(host),
        str(gw),
        str(iface)
    )
    if option_selected == 1:
        cmd_string = add_default_gateway
    elif option_selected == 2:
        cmd_string = add_regular_gateway
    elif option_selected == 3:
        cmd_string = add_subnet
    elif option_selected == 4:
        cmd_string = add_host

    print "DEBUG: ",str(cmd_string)
    return cmd_string
def routing_tables():
    gw = ""
    subnet = ""
    iface = ""
    netmask = ""
    host = ""

    options = """Add a default gateway (NAT before it reaches the internet)
    Add a regular gateway (Linking one gateway to another)
    Add a subnet (Linking 10.0.1.0/24 to 172.31.16.0/24)
    Add a single HOST (Pretty much a single IP address to another network possibly)"""
    menuparser(options)
    option_selected = int(raw_input("Enter the option: "))
    if option_selected == 1:
        gw = get_gw()
        iface = get_iface()
        route_cmd = build_cmd_string(option_selected, gw, subnet, iface, netmask, host)
        return
    elif option_selected == 2:
        gw = get_gw()
        iface = get_iface()
        route_cmd = build_cmd_string(option_selected, gw, subnet, iface, netmask, host)
        return
    elif option_selected == 3:
        gw = get_gw()
        iface = get_iface()
        netmask = get_netmask()
        subnet = get_subnet()
        route_cmd = build_cmd_string(option_selected, gw, subnet, iface, netmask, host)
        return
    elif option_selected == 4:
        host = get_host()
        gw = get_gw()
        iface = get_iface()
        route_cmd = build_cmd_string(option_selected, gw, subnet, iface, netmask, host)
        return
    else:
        os.system('clear')
        print "Please enter a option from 1 to 4"
        routing_tables()
        return

    route_cmd = str(route_cmd.encode('utf-8')).strip().rstrip()
    # commented for debugging
    bash_cmd(route_cmd)
    return

def main():
    options = """SSH commands: Dynamic SOCKS4, 4a, and 5 Proxies
    Netcat commands: Reverse shell listeners, and netcat relays (port-forwarding)
    Ncat commands: HTTP Proxies, Authenticated HTTP Proxies, HTTPS Tunneling
    Weavely setup: Easy setup of the persistent webshell that can quickly audit webserver flaws and path permissions issues
    Reverse shells: In /bin/sh, /bin/bash, awk, python, ruby, nodejs (JavaScript/JQuery), Java, php, netcat -E, netcat no -E, telnet, ssh
    Easy Peasey: Sub-project of mine, easily generates reverse shells through msfvenom with a selectable interface
    Streisand (Requires Amazon AWS or similar VPS): obfs4 + Tor, Shadowsocks, OpenVPN, Cisco Anyconnect/OpenConnect, WireGuard, SSH, OpenSSL + Stunnel, L2Psec
    tsocks + Proxychains: Transparent Proxifier + Proxychains to enable the use of non-proxy aware applications through the proxy
    UFW + IPTables: Automatically append new Uncomplicated Firewall Rules as you are using the other options (requires manual activation)
    Routing Paths Interactive: Quickly build static routes between gateways, subnets and hosts"""

    menu = menuparser(options)
    print menu

    option_selected = int(raw_input("Enter a option: "))
    if option_selected == 1:
        ssh_commands()
        return
    elif option_selected == 2:
        netcat_commands()
        return
    elif option_selected == 3:
        ncat_commands()
        return
    elif option_selected == 4:
        Weavely_setup()
        return
    elif option_selected == 5:
        reverse_shells()
        return
    elif option_selected == 6:
        # add that function here
        return
    elif option_selected == 7:
        streisand()
        return
    elif option_selected == 8:
        tsocks_proxychains()
        return
    elif option_selected == 9:
        ufw_iptables()
        return
    elif option_selected == 10:
        routing_tables()
        return
    else:
        os.system('clear')

        main()
    return
main()
