#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2015, Chris Long <alcamie@gmail.com> <chlong@redhat.com>
# Copyright (c) 2017, Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
module: nmcli
author:
  - Chris Long (@alcamie101)
short_description: Manage Networking
requirements:
  - nmcli
extends_documentation_fragment:
  - community.general.attributes
description:
  - Manage the network devices. Create, modify and manage various connection and device type, for example V(ethernet), V(team),
    V(bond), V(vlan) and so on.
  - 'On CentOS 8 and Fedora >=29 like systems, the requirements can be met by installing the following packages: NetworkManager.'
  - 'On CentOS 7 and Fedora <=28 like systems, the requirements can be met by installing the following packages: NetworkManager-tui.'
  - 'On Ubuntu and Debian like systems, the requirements can be met by installing the following packages: network-manager.'
  - 'On openSUSE, the requirements can be met by installing the following packages: NetworkManager.'
attributes:
  check_mode:
    support: full
  diff_mode:
    support: full
options:
  state:
    description:
      - Whether the device should exist or not, taking action if the state is different from what is stated.
      - Using O(state=present) to create connection will automatically bring connection up.
      - Using O(state=up) and O(state=down) will not modify connection with other parameters. These states have been added
        in community.general 9.5.0.
    type: str
    required: true
    choices: [absent, present, up, down]
  autoconnect:
    description:
      - Whether the connection should start on boot.
      - Whether the connection profile can be automatically activated.
    type: bool
    default: true
  autoconnect_priority:
    description:
      - The priority of the connection profile for autoconnect. If set, connection profiles with higher priority will be preferred.
    type: int
    version_added: 11.0.0
  autoconnect_retries:
    description:
      - The number of times to retry autoconnecting.
    type: int
    version_added: 11.0.0
  conn_name:
    description:
      - The name used to call the connection. Pattern is V(<type>[-<ifname>][-<num>]).
    type: str
    required: true
  conn_reload:
    description:
      - Whether the connection should be reloaded if it was modified.
    type: bool
    required: false
    default: false
    version_added: 9.5.0
  ifname:
    description:
      - The interface to bind the connection to.
      - The connection will only be applicable to this interface name.
      - A special value of V(*) can be used for interface-independent connections.
      - The ifname argument is mandatory for all connection types except bond, team, bridge, vlan and vpn.
      - This parameter defaults to O(conn_name) when left unset for all connection types except vpn that removes it.
    type: str
  type:
    description:
      - This is the type of device or network connection that you wish to create or modify.
      - Type V(dummy) is added in community.general 3.5.0.
      - Type V(gsm) is added in community.general 3.7.0.
      - Type V(infiniband) is added in community.general 2.0.0.
      - Type V(loopback) is added in community.general 8.1.0.
      - Type V(macvlan) is added in community.general 6.6.0.
      - Type V(ovs-bridge) is added in community.general 8.6.0.
      - Type V(ovs-interface) is added in community.general 8.6.0.
      - Type V(ovs-port) is added in community.general 8.6.0.
      - Type V(wireguard) is added in community.general 4.3.0.
      - Type V(vpn) is added in community.general 5.1.0.
      - Type V(vrf) is added in community.general 10.4.0.
      - Using V(bond-slave), V(bridge-slave), or V(team-slave) implies V(ethernet) connection type with corresponding O(slave_type)
        option.
      - If you want to control non-ethernet connection attached to V(bond), V(bridge), or V(team) consider using O(slave_type)
        option.
    type: str
    choices:
      - bond
      - bond-slave
      - bridge
      - bridge-slave
      - dummy
      - ethernet
      - generic
      - gre
      - infiniband
      - ipip
      - macvlan
      - sit
      - team
      - team-slave
      - vlan
      - vxlan
      - wifi
      - gsm
      - wireguard
      - ovs-bridge
      - ovs-port
      - ovs-interface
      - vpn
      - vrf
      - loopback
  mode:
    description:
      - This is the type of device or network connection that you wish to create for a bond or bridge.
    type: str
    choices: [802.3ad, active-backup, balance-alb, balance-rr, balance-tlb, balance-xor, broadcast]
    default: balance-rr
  transport_mode:
    description:
      - This option sets the connection type of Infiniband IPoIB devices.
    type: str
    choices: [datagram, connected]
    version_added: 5.8.0
  infiniband_mac:
    description:
      - MAC address of the Infiniband IPoIB devices.
    type: str
    version_added: 10.6.0
  slave_type:
    description:
      - Type of the device of this slave's master connection (for example V(bond)).
      - Type V(ovs-port) is added in community.general 8.6.0.
    type: str
    choices: ['bond', 'bridge', 'team', 'ovs-port', 'vrf']
    version_added: 7.0.0
  master:
    description:
      - Master <master (ifname, or connection UUID or conn_name) of bridge, team, bond, ovs-port master connection profile.
      - Mandatory if O(slave_type) is defined.
    type: str
  ip4:
    description:
      - List of IPv4 addresses to this interface.
      - Use the format V(192.0.2.24/24) or V(192.0.2.24).
      - If defined and O(method4) is not specified, automatically set C(ipv4.method) to V(manual).
    type: list
    elements: str
  gw4:
    description:
      - The IPv4 gateway for this interface.
      - Use the format V(192.0.2.1).
      - This parameter is mutually_exclusive with never_default4 parameter.
    type: str
  gw4_ignore_auto:
    description:
      - Ignore automatically configured IPv4 routes.
    type: bool
    default: false
    version_added: 3.2.0
  routes4:
    description:
      - The list of IPv4 routes.
      - Use the format V(192.0.3.0/24 192.0.2.1).
      - To specify more complex routes, use the O(routes4_extended) option.
    type: list
    elements: str
    version_added: 2.0.0
  routes4_extended:
    description:
      - The list of IPv4 routes.
    type: list
    elements: dict
    suboptions:
      ip:
        description:
          - IP or prefix of route.
          - Use the format V(192.0.3.0/24).
        type: str
        required: true
      next_hop:
        description:
          - Use the format V(192.0.2.1).
        type: str
      metric:
        description:
          - Route metric.
        type: int
      table:
        description:
          - The table to add this route to.
          - The default depends on C(ipv4.route-table).
        type: int
      cwnd:
        description:
          - The clamp for congestion window.
        type: int
      mtu:
        description:
          - If non-zero, only transmit packets of the specified size or smaller.
        type: int
      onlink:
        description:
          - Pretend that the nexthop is directly attached to this link, even if it does not match any interface prefix.
        type: bool
      tos:
        description:
          - The Type Of Service.
        type: int
  route_metric4:
    description:
      - Set metric level of ipv4 routes configured on interface.
    type: int
    version_added: 2.0.0
  routing_rules4:
    description:
      - Is the same as in an C(ip rule add) command, except always requires specifying a priority.
    type: list
    elements: str
    version_added: 3.3.0
  never_default4:
    description:
      - Set as default route.
      - This parameter is mutually_exclusive with gw4 parameter.
    type: bool
    default: false
    version_added: 2.0.0
  dns4:
    description:
      - A list of up to 3 DNS servers.
      - The entries must be IPv4 addresses, for example V(192.0.2.53).
    elements: str
    type: list
  dns4_search:
    description:
      - A list of DNS search domains.
    elements: str
    type: list
  dns4_options:
    description:
      - A list of DNS options.
    elements: str
    type: list
    version_added: 7.2.0
  dns4_ignore_auto:
    description:
      - Ignore automatically configured IPv4 name servers.
    type: bool
    default: false
    version_added: 3.2.0
  method4:
    description:
      - Configuration method to be used for IPv4.
      - If O(ip4) is set, C(ipv4.method) is automatically set to V(manual) and this parameter is not needed.
    type: str
    choices: [auto, link-local, manual, shared, disabled]
    version_added: 2.2.0
  may_fail4:
    description:
      - If you need O(ip4) configured before C(network-online.target) is reached, set this option to V(false).
      - This option applies when O(method4) is not V(disabled).
    type: bool
    default: true
    version_added: 3.3.0
  ip6:
    description:
      - List of IPv6 addresses to this interface.
      - Use the format V(abbe::cafe/128) or V(abbe::cafe).
      - If defined and O(method6) is not specified, automatically set C(ipv6.method) to V(manual).
    type: list
    elements: str
  gw6:
    description:
      - The IPv6 gateway for this interface.
      - Use the format V(2001:db8::1).
    type: str
  gw6_ignore_auto:
    description:
      - Ignore automatically configured IPv6 routes.
    type: bool
    default: false
    version_added: 3.2.0
  routes6:
    description:
      - The list of IPv6 routes.
      - Use the format V(fd12:3456:789a:1::/64 2001:dead:beef::1).
      - To specify more complex routes, use the O(routes6_extended) option.
    type: list
    elements: str
    version_added: 4.4.0
  routes6_extended:
    description:
      - The list of IPv6 routes but with parameters.
    type: list
    elements: dict
    suboptions:
      ip:
        description:
          - IP or prefix of route.
          - Use the format V(fd12:3456:789a:1::/64).
        type: str
        required: true
      next_hop:
        description:
          - Use the format V(2001:dead:beef::1).
        type: str
      metric:
        description:
          - Route metric.
        type: int
      table:
        description:
          - The table to add this route to.
          - The default depends on C(ipv6.route-table).
        type: int
      cwnd:
        description:
          - The clamp for congestion window.
        type: int
      mtu:
        description:
          - If non-zero, only transmit packets of the specified size or smaller.
        type: int
      onlink:
        description:
          - Pretend that the nexthop is directly attached to this link, even if it does not match any interface prefix.
        type: bool
  route_metric6:
    description:
      - Set metric level of IPv6 routes configured on interface.
    type: int
    version_added: 4.4.0
  dns6:
    description:
      - A list of up to 3 DNS servers.
      - The entries must be IPv6 addresses, for example V(2001:4860:4860::8888).
    elements: str
    type: list
  dns6_search:
    description:
      - A list of DNS search domains.
    elements: str
    type: list
  dns6_options:
    description:
      - A list of DNS options.
    elements: str
    type: list
    version_added: 7.2.0
  dns6_ignore_auto:
    description:
      - Ignore automatically configured IPv6 name servers.
    type: bool
    default: false
    version_added: 3.2.0
  method6:
    description:
      - Configuration method to be used for IPv6.
      - If O(ip6) is set, C(ipv6.method) is automatically set to V(manual) and this parameter is not needed.
      - V(disabled) was added in community.general 3.3.0.
    type: str
    choices: [ignore, auto, dhcp, link-local, manual, shared, disabled]
    version_added: 2.2.0
  ip_privacy6:
    description:
      - If enabled, it makes the kernel generate a temporary IPv6 address in addition to the public one.
    type: str
    choices: [disabled, prefer-public-addr, prefer-temp-addr, unknown]
    version_added: 4.2.0
  addr_gen_mode6:
    description:
      - Configure method for creating the address for use with IPv6 Stateless Address Autoconfiguration.
      - V(default) and V(default-or-eui64) have been added in community.general 6.5.0.
    type: str
    choices: [default, default-or-eui64, eui64, stable-privacy]
    version_added: 4.2.0
  mtu:
    description:
      - The connection MTU, for example V(9000). This can not be applied when creating the interface and is done once the
        interface has been created.
      - Can be used when modifying Team, VLAN, Ethernet (Future plans to implement wifi, gsm, pppoe, infiniband).
      - This parameter defaults to V(1500) when unset.
    type: int
  dhcp_client_id:
    description:
      - DHCP Client Identifier sent to the DHCP server.
    type: str
  primary:
    description:
      - This is only used with bond and is the primary interface name (for "active-backup" mode), this is the usually the
        'ifname'.
    type: str
  miimon:
    description:
      - This is only used with bond - miimon.
      - This parameter defaults to V(100) when unset.
    type: int
  downdelay:
    description:
      - This is only used with bond - downdelay.
    type: int
  updelay:
    description:
      - This is only used with bond - updelay.
    type: int
  xmit_hash_policy:
    description:
      - This is only used with bond - xmit_hash_policy type.
    type: str
    version_added: 5.6.0
  fail_over_mac:
    description:
      - This is only used with bond - fail_over_mac.
    type: str
    choices: [none, active, follow]
    version_added: 10.3.0
  arp_interval:
    description:
      - This is only used with bond - ARP interval.
    type: int
  arp_ip_target:
    description:
      - This is only used with bond - ARP IP target.
    type: str
  stp:
    description:
      - This is only used with bridge and controls whether Spanning Tree Protocol (STP) is enabled for this bridge.
    type: bool
    default: true
  priority:
    description:
      - This is only used with 'bridge' - sets STP priority.
    type: int
    default: 128
  forwarddelay:
    description:
      - This is only used with bridge - [forward-delay <2-30>] STP forwarding delay, in seconds.
    type: int
    default: 15
  hellotime:
    description:
      - This is only used with bridge - [hello-time <1-10>] STP hello time, in seconds.
    type: int
    default: 2
  maxage:
    description:
      - This is only used with bridge - [max-age <6-42>] STP maximum message age, in seconds.
    type: int
    default: 20
  ageingtime:
    description:
      - This is only used with bridge - [ageing-time <0-1000000>] the Ethernet MAC address aging time, in seconds.
    type: int
    default: 300
  mac:
    description:
      - MAC address of the connection.
      - Note this requires a recent kernel feature, originally introduced in 3.15 upstream kernel.
    type: str
  slavepriority:
    description:
      - This is only used with 'bridge-slave' - [<0-63>] - STP priority of this slave.
    type: int
    default: 32
  path_cost:
    description:
      - This is only used with 'bridge-slave' - [<1-65535>] - STP port cost for destinations using this slave.
    type: int
    default: 100
  hairpin:
    description:
      - This is only used with 'bridge-slave' - 'hairpin mode' for the slave, which allows frames to be sent back out through
        the slave the frame was received on.
      - The default change to V(false) in community.general 7.0.0. It used to be V(true) before.
    type: bool
    default: false
  runner:
    description:
      - This is the type of device or network connection that you wish to create for a team.
    type: str
    choices: [broadcast, roundrobin, activebackup, loadbalance, lacp]
    default: roundrobin
    version_added: 3.4.0
  runner_hwaddr_policy:
    description:
      - This defines the policy of how hardware addresses of team device and port devices should be set during the team lifetime.
    type: str
    choices: [same_all, by_active, only_active]
    version_added: 3.4.0
  runner_fast_rate:
    description:
      - Option specifies the rate at which our link partner is asked to transmit LACPDU packets. If this is V(true) then packets
        will be sent once per second. Otherwise they will be sent every 30 seconds.
      - Only allowed for O(runner=lacp).
    type: bool
    version_added: 6.5.0
  vlanid:
    description:
      - This is only used with VLAN - VLAN ID in range <0-4095>.
    type: int
  vlandev:
    description:
      - This is only used with VLAN - parent device this VLAN is on, can use ifname.
    type: str
  flags:
    description:
      - This is only used with VLAN - flags.
    type: str
  ingress:
    description:
      - This is only used with VLAN - VLAN ingress priority mapping.
    type: str
  egress:
    description:
      - This is only used with VLAN - VLAN egress priority mapping.
    type: str
  vxlan_id:
    description:
      - This is only used with VXLAN - VXLAN ID.
    type: int
  vxlan_remote:
    description:
      - This is only used with VXLAN - VXLAN destination IP address.
    type: str
  vxlan_local:
    description:
      - This is only used with VXLAN - VXLAN local IP address.
    type: str
  ip_tunnel_dev:
    description:
      - This is used with GRE/IPIP/SIT - parent device this GRE/IPIP/SIT tunnel, can use ifname.
    type: str
  ip_tunnel_remote:
    description:
      - This is used with GRE/IPIP/SIT - GRE/IPIP/SIT destination IP address.
    type: str
  ip_tunnel_local:
    description:
      - This is used with GRE/IPIP/SIT - GRE/IPIP/SIT local IP address.
    type: str
  ip_tunnel_input_key:
    description:
      - The key used for tunnel input packets.
      - Only used when O(type=gre).
    type: str
    version_added: 3.6.0
  ip_tunnel_output_key:
    description:
      - The key used for tunnel output packets.
      - Only used when O(type=gre).
    type: str
    version_added: 3.6.0
  table:
    description:
      - This is only used with VRF - VRF table number.
    type: int
    version_added: 10.4.0
  zone:
    description:
      - The trust level of the connection.
      - When updating this property on a currently activated connection, the change takes effect immediately.
    type: str
    version_added: 2.0.0
  wifi_sec:
    description:
      - The security configuration of the WiFi connection.
      - Note the list of suboption attributes may vary depending on which version of NetworkManager/nmcli is installed on
        the host.
      - 'An up-to-date list of supported attributes can be found here: U(https://networkmanager.dev/docs/api/latest/settings-802-11-wireless-security.html).'
      - 'For instance to use common WPA-PSK auth with a password: V({key-mgmt: wpa-psk, psk: my_password}).'
    type: dict
    suboptions:
      auth-alg:
        description:
          - When WEP is used (that is, if O(wifi_sec.key-mgmt) is V(none) or V(ieee8021x)) indicate the 802.11 authentication
            algorithm required by the AP here.
          - One of V(open) for Open System, V(shared) for Shared Key, or V(leap) for Cisco LEAP.
          - When using Cisco LEAP (that is, if O(wifi_sec.key-mgmt=ieee8021x) and O(wifi_sec.auth-alg=leap)) the O(wifi_sec.leap-username)
            and O(wifi_sec.leap-password) properties must be specified.
        type: str
        choices: [open, shared, leap]
      fils:
        description:
          - Indicates whether Fast Initial Link Setup (802.11ai) must be enabled for the connection.
          - One of V(0) (use global default value), V(1) (disable FILS), V(2) (enable FILS if the supplicant and the access
            point support it) or V(3) (enable FILS and fail if not supported).
          - When set to V(0) and no global default is set, FILS will be optionally enabled.
        type: int
        choices: [0, 1, 2, 3]
        default: 0
      group:
        description:
          - A list of group/broadcast encryption algorithms which prevents connections to Wi-Fi networks that do not utilize
            one of the algorithms in the list.
          - For maximum compatibility leave this property empty.
        type: list
        elements: str
        choices: [wep40, wep104, tkip, ccmp]
      key-mgmt:
        description:
          - Key management used for the connection.
          - One of V(none) (WEP or no password protection), V(ieee8021x) (Dynamic WEP), V(owe) (Opportunistic Wireless Encryption),
            V(wpa-psk) (WPA2 + WPA3 personal), V(sae) (WPA3 personal only), V(wpa-eap) (WPA2 + WPA3 enterprise) or V(wpa-eap-suite-b-192)
            (WPA3 enterprise only).
          - This property must be set for any Wi-Fi connection that uses security.
        type: str
        choices: [none, ieee8021x, owe, wpa-psk, sae, wpa-eap, wpa-eap-suite-b-192]
      leap-password-flags:
        description: Flags indicating how to handle the O(wifi_sec.leap-password) property.
        type: list
        elements: int
      leap-password:
        description: The login password for legacy LEAP connections (that is, if O(wifi_sec.key-mgmt=ieee8021x) and O(wifi_sec.auth-alg=leap)).
        type: str
      leap-username:
        description: The login username for legacy LEAP connections (that is, if O(wifi_sec.key-mgmt=ieee8021x) and O(wifi_sec.auth-alg=leap)).
        type: str
      pairwise:
        description:
          - A list of pairwise encryption algorithms which prevents connections to Wi-Fi networks that do not utilize one
            of the algorithms in the list.
          - For maximum compatibility leave this property empty.
        type: list
        elements: str
        choices: [tkip, ccmp]
      pmf:
        description:
          - Indicates whether Protected Management Frames (802.11w) must be enabled for the connection.
          - One of V(0) (use global default value), V(1) (disable PMF), V(2) (enable PMF if the supplicant and the access
            point support it) or V(3) (enable PMF and fail if not supported).
          - When set to V(0) and no global default is set, PMF will be optionally enabled.
        type: int
        choices: [0, 1, 2, 3]
        default: 0
      proto:
        description:
          - List of strings specifying the allowed WPA protocol versions to use.
          - Each element may be V(wpa) (allow WPA) or V(rsn) (allow WPA2/RSN).
          - If not specified, both WPA and RSN connections are allowed.
        type: list
        elements: str
        choices: [wpa, rsn]
      psk-flags:
        description: Flags indicating how to handle the O(wifi_sec.psk) property.
        type: list
        elements: int
      psk:
        description:
          - Pre-Shared-Key for WPA networks.
          - For WPA-PSK, it is either an ASCII passphrase of 8 to 63 characters that is (as specified in the 802.11i standard)
            hashed to derive the actual key, or the key in form of 64 hexadecimal character.
          - The WPA3-Personal networks use a passphrase of any length for SAE authentication.
        type: str
      wep-key-flags:
        description:
          - Flags indicating how to handle the O(wifi_sec.wep-key0), O(wifi_sec.wep-key1), O(wifi_sec.wep-key2), and O(wifi_sec.wep-key3)
            properties.
        type: list
        elements: int
      wep-key-type:
        description:
          - Controls the interpretation of WEP keys.
          - Allowed values are V(1), in which case the key is either a 10- or 26-character hexadecimal string, or a 5- or
            13-character ASCII password; or V(2), in which case the passphrase is provided as a string and will be hashed
            using the de-facto MD5 method to derive the actual WEP key.
        type: int
        choices: [1, 2]
      wep-key0:
        description:
          - Index 0 WEP key. This is the WEP key used in most networks.
          - See the O(wifi_sec.wep-key-type) property for a description of how this key is interpreted.
        type: str
      wep-key1:
        description:
          - Index 1 WEP key. This WEP index is not used by most networks.
          - See the O(wifi_sec.wep-key-type) property for a description of how this key is interpreted.
        type: str
      wep-key2:
        description:
          - Index 2 WEP key. This WEP index is not used by most networks.
          - See the O(wifi_sec.wep-key-type) property for a description of how this key is interpreted.
        type: str
      wep-key3:
        description:
          - Index 3 WEP key. This WEP index is not used by most networks.
          - See the O(wifi_sec.wep-key-type) property for a description of how this key is interpreted.
        type: str
      wep-tx-keyidx:
        description:
          - When static WEP is used (that is, if O(wifi_sec.key-mgmt=none)) and a non-default WEP key index is used by the
            AP, put that WEP key index here.
          - Valid values are V(0) (default key) through V(3).
          - Note that some consumer access points (like the Linksys WRT54G) number the keys V(1) to V(4).
        type: int
        choices: [0, 1, 2, 3]
        default: 0
      wps-method:
        description:
          - Flags indicating which mode of WPS is to be used if any.
          - There is little point in changing the default setting as NetworkManager will automatically determine whether it
            is feasible to start WPS enrollment from the Access Point capabilities.
          - WPS can be disabled by setting this property to a value of V(1).
        type: int
        default: 0
    version_added: 3.0.0
  ssid:
    description:
      - Name of the Wireless router or the access point.
    type: str
    version_added: 3.0.0
  wifi:
    description:
      - The configuration of the WiFi connection.
      - Note the list of suboption attributes may vary depending on which version of NetworkManager/nmcli is installed on
        the host.
      - 'An up-to-date list of supported attributes can be found here: U(https://networkmanager.dev/docs/api/latest/settings-802-11-wireless.html).'
      - 'For instance to create a hidden AP mode WiFi connection: V({hidden: true, mode: ap}).'
    type: dict
    suboptions:
      ap-isolation:
        description:
          - Configures AP isolation, which prevents communication between wireless devices connected to this AP.
          - This property can be set to a value different from V(-1) only when the interface is configured in AP mode.
          - If set to V(1), devices are not able to communicate with each other. This increases security because it protects
            devices against attacks from other clients in the network. At the same time, it prevents devices to access resources
            on the same wireless networks as file shares, printers, and so on.
          - If set to V(0), devices can talk to each other.
          - When set to V(-1), the global default is used; in case the global default is unspecified it is assumed to be V(0).
        type: int
        choices: [-1, 0, 1]
        default: -1
      assigned-mac-address:
        description:
          - The new field for the cloned MAC address.
          - It can be either a hardware address in ASCII representation, or one of the special values V(preserve), V(permanent),
            V(random) or V(stable).
          - This field replaces the deprecated O(wifi.cloned-mac-address) on D-Bus, which can only contain explicit hardware
            addresses.
          - Note that this property only exists in D-Bus API. libnm and nmcli continue to call this property C(cloned-mac-address).
        type: str
      band:
        description:
          - 802.11 frequency band of the network.
          - One of V(a) for 5GHz 802.11a or V(bg) for 2.4GHz 802.11.
          - This will lock associations to the Wi-Fi network to the specific band, so for example, if V(a) is specified, the
            device will not associate with the same network in the 2.4GHz band even if the network's settings are compatible.
          - This setting depends on specific driver capability and may not work with all drivers.
        type: str
        choices: [a, bg]
      bssid:
        description:
          - If specified, directs the device to only associate with the given access point.
          - This capability is highly driver dependent and not supported by all devices.
          - Note this property does not control the BSSID used when creating an Ad-Hoc network and is unlikely to in the future.
        type: str
      channel:
        description:
          - Wireless channel to use for the Wi-Fi connection.
          - The device will only join (or create for Ad-Hoc networks) a Wi-Fi network on the specified channel.
          - Because channel numbers overlap between bands, this property also requires the O(wifi.band) property to be set.
        type: int
        default: 0
      cloned-mac-address:
        description:
          - This D-Bus field is deprecated in favor of O(wifi.assigned-mac-address) which is more flexible and allows specifying
            special variants like V(random).
          - For libnm and nmcli, this field is called C(cloned-mac-address).
        type: str
      generate-mac-address-mask:
        description:
          - With O(wifi.cloned-mac-address) setting V(random) or V(stable), by default all bits of the MAC address are scrambled
            and a locally-administered, unicast MAC address is created. This property allows to specify that certain bits
            are fixed.
          - Note that the least significant bit of the first MAC address will always be unset to create a unicast MAC address.
          - If the property is V(null), it is eligible to be overwritten by a default connection setting.
          - If the value is still V(null) or an empty string, the default is to create a locally-administered, unicast MAC
            address.
          - If the value contains one MAC address, this address is used as mask. The set bits of the mask are to be filled
            with the current MAC address of the device, while the unset bits are subject to randomization.
          - Setting V(FE:FF:FF:00:00:00) means to preserve the OUI of the current MAC address and only randomize the lower
            3 bytes using the V(random) or V(stable) algorithm.
          - If the value contains one additional MAC address after the mask, this address is used instead of the current MAC
            address to fill the bits that shall not be randomized.
          - For example, a value of V(FE:FF:FF:00:00:00 68:F7:28:00:00:00) will set the OUI of the MAC address to 68:F7:28,
            while the lower bits are randomized.
          - A value of V(02:00:00:00:00:00 00:00:00:00:00:00) will create a fully scrambled globally-administered, burned-in
            MAC address.
          - If the value contains more than one additional MAC addresses, one of them is chosen randomly. For example, V(02:00:00:00:00:00
            00:00:00:00:00:00 02:00:00:00:00:00) will create a fully scrambled MAC address, randomly locally or globally administered.
        type: str
      hidden:
        description:
          - If V(true), indicates that the network is a non-broadcasting network that hides its SSID. This works both in infrastructure
            and AP mode.
          - In infrastructure mode, various workarounds are used for a more reliable discovery of hidden networks, such as
            probe-scanning the SSID. However, these workarounds expose inherent insecurities with hidden SSID networks, and
            thus hidden SSID networks should be used with caution.
          - In AP mode, the created network does not broadcast its SSID.
          - Note that marking the network as hidden may be a privacy issue for you (in infrastructure mode) or client stations
            (in AP mode), as the explicit probe-scans are distinctly recognizable on the air.
        type: bool
        default: false
      mac-address-blacklist:
        description:
          - A list of permanent MAC addresses of Wi-Fi devices to which this connection should never apply.
          - Each MAC address should be given in the standard hex-digits-and-colons notation (for example, V(00:11:22:33:44:55)).
        type: list
        elements: str
      mac-address-randomization:
        description:
          - One of V(0) (never randomize unless the user has set a global default to randomize and the supplicant supports
            randomization), V(1) (never randomize the MAC address), or V(2) (always randomize the MAC address).
          - This property is deprecated for O(wifi.cloned-mac-address).
        type: int
        default: 0
        choices: [0, 1, 2]
      mac-address:
        description:
          - If specified, this connection will only apply to the Wi-Fi device whose permanent MAC address matches.
          - This property does not change the MAC address of the device (for example for MAC spoofing).
        type: str
      mode:
        description: Wi-Fi network mode. If blank, V(infrastructure) is assumed.
        type: str
        choices: [infrastructure, mesh, adhoc, ap]
        default: infrastructure
      mtu:
        description: If non-zero, only transmit packets of the specified size or smaller, breaking larger packets up into
          multiple Ethernet frames.
        type: int
        default: 0
      powersave:
        description:
          - One of V(2) (disable Wi-Fi power saving), V(3) (enable Wi-Fi power saving), V(1) (do not touch currently configure
            setting) or V(0) (use the globally configured value).
          - All other values are reserved.
        type: int
        default: 0
        choices: [0, 1, 2, 3]
      rate:
        description:
          - If non-zero, directs the device to only use the specified bitrate for communication with the access point.
          - Units are in Kb/s, so for example V(5500) = 5.5 Mbit/s.
          - This property is highly driver dependent and not all devices support setting a static bitrate.
        type: int
        default: 0
      tx-power:
        description:
          - If non-zero, directs the device to use the specified transmit power.
          - Units are dBm.
          - This property is highly driver dependent and not all devices support setting a static transmit power.
        type: int
        default: 0
      wake-on-wlan:
        description:
          - The NMSettingWirelessWakeOnWLan options to enable. Not all devices support all options.
          - May be any combination of C(NM_SETTING_WIRELESS_WAKE_ON_WLAN_ANY) (V(0x2)), C(NM_SETTING_WIRELESS_WAKE_ON_WLAN_DISCONNECT)
            (V(0x4)), C(NM_SETTING_WIRELESS_WAKE_ON_WLAN_MAGIC) (V(0x8)), C(NM_SETTING_WIRELESS_WAKE_ON_WLAN_GTK_REKEY_FAILURE)
            (V(0x10)), C(NM_SETTING_WIRELESS_WAKE_ON_WLAN_EAP_IDENTITY_REQUEST) (V(0x20)), C(NM_SETTING_WIRELESS_WAKE_ON_WLAN_4WAY_HANDSHAKE)
            (V(0x40)), C(NM_SETTING_WIRELESS_WAKE_ON_WLAN_RFKILL_RELEASE) (V(0x80)), C(NM_SETTING_WIRELESS_WAKE_ON_WLAN_TCP)
            (V(0x100)) or the special values V(0x1) (to use global settings) and V(0x8000) (to disable management of Wake-on-LAN
            in NetworkManager).
          - Note the option values' sum must be specified in order to combine multiple options.
        type: int
        default: 1
    version_added: 3.5.0
  ignore_unsupported_suboptions:
    description:
      - Ignore suboptions which are invalid or unsupported by the version of NetworkManager/nmcli installed on the host.
      - Only O(wifi) and O(wifi_sec) options are currently affected.
    type: bool
    default: false
    version_added: 3.6.0
  gsm:
    description:
      - The configuration of the GSM connection.
      - Note the list of suboption attributes may vary depending on which version of NetworkManager/nmcli is installed on
        the host.
      - 'An up-to-date list of supported attributes can be found here: U(https://networkmanager.dev/docs/api/latest/settings-gsm.html).'
      - 'For instance to use apn, pin, username and password: V({apn: provider.apn, pin: 1234, username: apn.username, password:
        apn.password}).'
    type: dict
    version_added: 3.7.0
    suboptions:
      apn:
        description:
          - The GPRS Access Point Name specifying the APN used when establishing a data session with the GSM-based network.
          - The APN often determines how the user will be billed for their network usage and whether the user has access to
            the Internet or just a provider-specific walled-garden, so it is important to use the correct APN for the user's
            mobile broadband plan.
          - The APN may only be composed of the characters a-z, 0-9, ., and - per GSM 03.60 Section 14.9.
        type: str
      auto-config:
        description: When V(true), the settings such as O(gsm.apn), O(gsm.username), or O(gsm.password) will default to values
          that match the network the modem will register to in the Mobile Broadband Provider database.
        type: bool
        default: false
      device-id:
        description:
          - The device unique identifier (as given by the V(WWAN) management service) which this connection applies to.
          - If given, the connection will only apply to the specified device.
        type: str
      home-only:
        description:
          - When V(true), only connections to the home network will be allowed.
          - Connections to roaming networks will not be made.
        type: bool
        default: false
      mtu:
        description: If non-zero, only transmit packets of the specified size or smaller, breaking larger packets up into
          multiple Ethernet frames.
        type: int
        default: 0
      network-id:
        description:
          - The Network ID (GSM LAI format, ie MCC-MNC) to force specific network registration.
          - If the Network ID is specified, NetworkManager will attempt to force the device to register only on the specified
            network.
          - This can be used to ensure that the device does not roam when direct roaming control of the device is not otherwise
            possible.
        type: str
      number:
        description: Legacy setting that used to help establishing PPP data sessions for GSM-based modems.
        type: str
      password:
        description:
          - The password used to authenticate with the network, if required.
          - Many providers do not require a password, or accept any password.
          - But if a password is required, it is specified here.
        type: str
      password-flags:
        description:
          - NMSettingSecretFlags indicating how to handle the O(gsm.password) property.
          - 'Following choices are allowed: V(0) B(NONE): The system is responsible for providing and storing this secret
            (default), V(1) B(AGENT_OWNED): A user secret agent is responsible for providing and storing this secret; when
            it is required agents will be asked to retrieve it V(2) B(NOT_SAVED): This secret should not be saved, but should
            be requested from the user each time it is needed V(4) B(NOT_REQUIRED): In situations where it cannot be automatically
            determined that the secret is required (some VPNs and PPP providers do not require all secrets) this flag indicates
            that the specific secret is not required.'
        type: int
        choices: [0, 1, 2, 4]
        default: 0
      pin:
        description:
          - If the SIM is locked with a PIN it must be unlocked before any other operations are requested.
          - Specify the PIN here to allow operation of the device.
        type: str
      pin-flags:
        description:
          - NMSettingSecretFlags indicating how to handle the O(gsm.pin) property.
          - See O(gsm.password-flags) for NMSettingSecretFlags choices.
        type: int
        choices: [0, 1, 2, 4]
        default: 0
      sim-id:
        description:
          - The SIM card unique identifier (as given by the C(WWAN) management service) which this connection applies to.
          - If given, the connection will apply to any device also allowed by O(gsm.device-id) which contains a SIM card matching
            the given identifier.
        type: str
      sim-operator-id:
        description:
          - A MCC/MNC string like V(310260) or V(21601I) identifying the specific mobile network operator which this connection
            applies to.
          - If given, the connection will apply to any device also allowed by O(gsm.device-id) and O(gsm.sim-id) which contains
            a SIM card provisioned by the given operator.
        type: str
      username:
        description:
          - The username used to authenticate with the network, if required.
          - Many providers do not require a username, or accept any username.
          - But if a username is required, it is specified here.
  macvlan:
    description:
      - The configuration of the MAC VLAN connection.
      - Note the list of suboption attributes may vary depending on which version of NetworkManager/nmcli is installed on
        the host.
      - 'An up-to-date list of supported attributes can be found here: U(https://networkmanager.dev/docs/api/latest/settings-macvlan.html).'
    type: dict
    version_added: 6.6.0
    suboptions:
      mode:
        description:
          - The macvlan mode, which specifies the communication mechanism between multiple macvlans on the same lower device.
          - 'Following choices are allowed: V(1) B(vepa), V(2) B(bridge), V(3) B(private), V(4) B(passthru) and V(5) B(source).'
        type: int
        choices: [1, 2, 3, 4, 5]
        required: true
      parent:
        description:
          - If given, specifies the parent interface name or parent connection UUID from which this MAC-VLAN interface should
            be created. If this property is not specified, the connection must contain an "802-3-ethernet" setting with a
            "mac-address" property.
        type: str
        required: true
      promiscuous:
        description:
          - Whether the interface should be put in promiscuous mode.
        type: bool
      tap:
        description:
          - Whether the interface should be a MACVTAP.
        type: bool
  wireguard:
    description:
      - The configuration of the Wireguard connection.
      - Note the list of suboption attributes may vary depending on which version of NetworkManager/nmcli is installed on
        the host.
      - 'An up-to-date list of supported attributes can be found here: U(https://networkmanager.dev/docs/api/latest/settings-wireguard.html).'
      - 'For instance to configure a listen port: V({listen-port: 12345}).'
    type: dict
    version_added: 4.3.0
    suboptions:
      fwmark:
        description:
          - The 32-bit fwmark for outgoing packets.
          - The use of fwmark is optional and is by default off. Setting it to 0 disables it.
          - Note that O(wireguard.ip4-auto-default-route) or O(wireguard.ip6-auto-default-route) enabled, implies to automatically
            choose a fwmark.
        type: int
      ip4-auto-default-route:
        description:
          - Whether to enable special handling of the IPv4 default route.
          - If enabled, the IPv4 default route from O(wireguard.peer-routes) will be placed to a dedicated routing-table and
            two policy routing rules will be added.
          - The fwmark number is also used as routing-table for the default-route, and if fwmark is zero, an unused fwmark/table
            is chosen automatically. This corresponds to what wg-quick does with Table=auto and what WireGuard calls "Improved
            Rule-based Routing".
        type: bool
      ip6-auto-default-route:
        description:
          - Like O(wireguard.ip4-auto-default-route), but for the IPv6 default route.
        type: bool
      listen-port:
        description: The WireGuard connection listen-port. If not specified, the port will be chosen randomly when the interface
          comes up.
        type: int
      mtu:
        description:
          - If non-zero, only transmit packets of the specified size or smaller, breaking larger packets up into multiple
            fragments.
          - If zero a default MTU is used. Note that contrary to wg-quick's MTU setting, this does not take into account the
            current routes at the time of activation.
        type: int
      peer-routes:
        description:
          - Whether to automatically add routes for the AllowedIPs ranges of the peers.
          - If V(true) (the default), NetworkManager will automatically add routes in the routing tables according to C(ipv4.route-table)
            and C(ipv6.route-table). Usually you want this automatism enabled.
          - If V(false), no such routes are added automatically. In this case, the user may want to configure static routes
            in C(ipv4.routes) and C(ipv6.routes), respectively.
          - Note that if the peer's AllowedIPs is V(0.0.0.0/0) or V(::/0) and the profile's C(ipv4.never-default) or C(ipv6.never-default)
            setting is enabled, the peer route for this peer will not be added automatically.
        type: bool
      private-key:
        description: The 256 bit private-key in base64 encoding.
        type: str
      private-key-flags:
        description: C(NMSettingSecretFlags) indicating how to handle the O(wireguard.private-key) property.
        type: int
        choices: [0, 1, 2]
  vpn:
    description:
      - Configuration of a VPN connection (PPTP and L2TP).
      - In order to use L2TP you need to be sure that C(network-manager-l2tp) - and C(network-manager-l2tp-gnome) if host
        has UI - are installed on the host.
    type: dict
    version_added: 5.1.0
    suboptions:
      permissions:
        description: User that will have permission to use the connection.
        type: str
        required: true
      service-type:
        description: This defines the service type of connection.
        type: str
        required: true
      gateway:
        description: The gateway to connection. It can be an IP address (for example V(192.0.2.1)) or a FQDN address (for
          example V(vpn.example.com)).
        type: str
        required: true
      password-flags:
        description:
          - NMSettingSecretFlags indicating how to handle the C(vpn.password) property.
          - 'Following choices are allowed: V(0) B(NONE): The system is responsible for providing and storing this secret
            (default); V(1) B(AGENT_OWNED): A user secret agent is responsible for providing and storing this secret; when
            it is required agents will be asked to retrieve it; V(2) B(NOT_SAVED): This secret should not be saved, but should
            be requested from the user each time it is needed; V(4) B(NOT_REQUIRED): In situations where it cannot be automatically
            determined that the secret is required (some VPNs and PPP providers do not require all secrets) this flag indicates
            that the specific secret is not required.'
        type: int
        choices: [0, 1, 2, 4]
        default: 0
      user:
        description: Username provided by VPN administrator.
        type: str
        required: true
      ipsec-enabled:
        description:
          - Enable or disable IPSec tunnel to L2TP host.
          - This option is need when O(vpn.service-type) is V(org.freedesktop.NetworkManager.l2tp).
        type: bool
      ipsec-psk:
        description:
          - The pre-shared key in base64 encoding.
          - "You can encode using this Ansible jinja2 expression: V(\"0s{{ '[YOUR PRE-SHARED KEY]' | ansible.builtin.b64encode }}\")."
          - This is only used when O(vpn.ipsec-enabled=true).
        type: str
  sriov:
    description:
      - Allow to configure SR-IOV settings.
      - 'An up-to-date list of supported attributes can be found here:
        U(https://networkmanager.pages.freedesktop.org/NetworkManager/NetworkManager/settings-sriov.html).'
    type: dict
    version_added: 10.1.0
    suboptions:
      autoprobe-drivers:
        description:
          - Whether to autoprobe virtual functions by a compatible driver.
        type: int
      eswitch-encap-mode:
        description:
          - Select the eswitch encapsulation support.
        type: int
      eswitch-inline-mode:
        description:
          - Select the eswitch inline-mode of the device.
        type: int
      eswitch-mode:
        description:
          - Select the eswitch mode of the device.
        type: int
      total-vfs:
        description: Number of virtual functions to create. Consult your NIC documentation for the maximum number of VFs supported.
        type: int
      vfs:
        description:
          - 'Virtual function descriptors in the form: V(INDEX [ATTR=VALUE[ ATTR=VALUE]...]).'
          - Multiple VFs can be specified using a comma as separator, for example V(2 mac=00:11:22:33:44:55 spoof-check=true,3
            vlans=100).
        type: str
"""

EXAMPLES = r"""
# These examples are using the following inventory:
#
# ## Directory layout:
#
# |_/inventory/cloud-hosts
# |           /group_vars/openstack-stage.yml
# |           /host_vars/controller-01.openstack.host.com
# |           /host_vars/controller-02.openstack.host.com
# |_/playbook/library/nmcli.py
# |          /playbook-add.yml
# |          /playbook-del.yml
# ```
#
# ## inventory examples
# ### groups_vars
# ```yml
# ---
# #devops_os_define_network
# storage_gw: "192.0.2.254"
# external_gw: "198.51.100.254"
# tenant_gw: "203.0.113.254"
#
# #Team vars
# nmcli_team:
#   - conn_name: tenant
#     ip4: '{{ tenant_ip }}'
#     gw4: '{{ tenant_gw }}'
#   - conn_name: external
#     ip4: '{{ external_ip }}'
#     gw4: '{{ external_gw }}'
#   - conn_name: storage
#     ip4: '{{ storage_ip }}'
#     gw4: '{{ storage_gw }}'
# nmcli_team_slave:
#   - conn_name: em1
#     ifname: em1
#     master: tenant
#   - conn_name: em2
#     ifname: em2
#     master: tenant
#   - conn_name: p2p1
#     ifname: p2p1
#     master: storage
#   - conn_name: p2p2
#     ifname: p2p2
#     master: external
#
# #bond vars
# nmcli_bond:
#   - conn_name: tenant
#     ip4: '{{ tenant_ip }}'
#     gw4: ''
#     mode: balance-rr
#   - conn_name: external
#     ip4: '{{ external_ip }}'
#     gw4: ''
#     mode: balance-rr
#   - conn_name: storage
#     ip4: '{{ storage_ip }}'
#     gw4: '{{ storage_gw }}'
#     mode: balance-rr
# nmcli_bond_slave:
#   - conn_name: em1
#     ifname: em1
#     master: tenant
#   - conn_name: em2
#     ifname: em2
#     master: tenant
#   - conn_name: p2p1
#     ifname: p2p1
#     master: storage
#   - conn_name: p2p2
#     ifname: p2p2
#     master: external
#
# #ethernet vars
# nmcli_ethernet:
#   - conn_name: em1
#     ifname: em1
#     ip4:
#       - '{{ tenant_ip }}'
#       - '{{ second_tenant_ip }}'
#     gw4: '{{ tenant_gw }}'
#   - conn_name: em2
#     ifname: em2
#     ip4: '{{ tenant_ip1 }}'
#     gw4: '{{ tenant_gw }}'
#   - conn_name: p2p1
#     ifname: p2p1
#     ip4: '{{ storage_ip }}'
#     gw4: '{{ storage_gw }}'
#   - conn_name: p2p2
#     ifname: p2p2
#     ip4: '{{ external_ip }}'
#     gw4: '{{ external_gw }}'
# ```
#
# ### host_vars
# ```yml
# ---
# storage_ip: "192.0.2.91/23"
# external_ip: "198.51.100.23/21"
# tenant_ip: "203.0.113.77/23"
# second_tenant_ip: "204.0.113.77/23"
# ```


## playbook-add.yml example

- hosts: openstack-stage
  remote_user: root
  tasks:

    - name: Install needed network manager libs
      ansible.builtin.package:
        name:
          - NetworkManager-libnm
          - nm-connection-editor
          - libsemanage-python
          - policycoreutils-python
        state: present

##### Working with all cloud nodes - Teaming
    - name: Try nmcli add team - conn_name only & ip4 gw4
      community.general.nmcli:
        type: team
        conn_name: '{{ item.conn_name }}'
        ip4: '{{ item.ip4 }}'
        gw4: '{{ item.gw4 }}'
        state: present
      with_items:
        - '{{ nmcli_team }}'

    - name: Try nmcli add teams-slave
      community.general.nmcli:
        type: team-slave
        conn_name: '{{ item.conn_name }}'
        ifname: '{{ item.ifname }}'
        master: '{{ item.master }}'
        state: present
      with_items:
        - '{{ nmcli_team_slave }}'

##### Working with all cloud nodes - Bonding
    - name: Try nmcli add bond - conn_name only & ip4 gw4 mode
      community.general.nmcli:
        type: bond
        conn_name: '{{ item.conn_name }}'
        ip4: '{{ item.ip4 }}'
        gw4: '{{ item.gw4 }}'
        mode: '{{ item.mode }}'
        state: present
      with_items:
        - '{{ nmcli_bond }}'

    - name: Try nmcli add bond-slave
      community.general.nmcli:
        type: bond-slave
        conn_name: '{{ item.conn_name }}'
        ifname: '{{ item.ifname }}'
        master: '{{ item.master }}'
        state: present
      with_items:
        - '{{ nmcli_bond_slave }}'

##### Working with all cloud nodes - Ethernet
    - name: Try nmcli add Ethernet - conn_name only & ip4 gw4
      community.general.nmcli:
        type: ethernet
        conn_name: '{{ item.conn_name }}'
        ip4: '{{ item.ip4 }}'
        gw4: '{{ item.gw4 }}'
        state: present
      with_items:
        - '{{ nmcli_ethernet }}'

## playbook-del.yml example
- hosts: openstack-stage
  remote_user: root
  tasks:

    - name: Try nmcli del team - multiple
      community.general.nmcli:
        conn_name: '{{ item.conn_name }}'
        state: absent
      with_items:
        - conn_name: em1
        - conn_name: em2
        - conn_name: p1p1
        - conn_name: p1p2
        - conn_name: p2p1
        - conn_name: p2p2
        - conn_name: tenant
        - conn_name: storage
        - conn_name: external
        - conn_name: team-em1
        - conn_name: team-em2
        - conn_name: team-p1p1
        - conn_name: team-p1p2
        - conn_name: team-p2p1
        - conn_name: team-p2p2

    - name: Add an Ethernet connection with static IP configuration
      community.general.nmcli:
        conn_name: my-eth1
        ifname: eth1
        type: ethernet
        ip4: 192.0.2.100/24
        gw4: 192.0.2.1
        state: present

    - name: Add an Team connection with static IP configuration
      community.general.nmcli:
        conn_name: my-team1
        ifname: my-team1
        type: team
        ip4: 192.0.2.100/24
        gw4: 192.0.2.1
        state: present
        autoconnect: true

    - name: Optionally, at the same time specify IPv6 addresses for the device
      community.general.nmcli:
        conn_name: my-eth1
        ifname: eth1
        type: ethernet
        ip4: 192.0.2.100/24
        gw4: 192.0.2.1
        ip6: 2001:db8::cafe
        gw6: 2001:db8::1
        state: present

    - name: Add two IPv4 DNS server addresses
      community.general.nmcli:
        conn_name: my-eth1
        type: ethernet
        dns4:
          - 192.0.2.53
          - 198.51.100.53
        state: present

    - name: Make a profile usable for all compatible Ethernet interfaces
      community.general.nmcli:
        ctype: ethernet
        name: my-eth1
        ifname: '*'
        state: present

    - name: Change the property of a setting e.g. MTU
      community.general.nmcli:
        conn_name: my-eth1
        mtu: 9000
        type: ethernet
        state: present

    - name: Change the property of a setting e.g. MTU and reload connection
      community.general.nmcli:
        conn_name: my-eth1
        mtu: 1500
        type: ethernet
        state: present
        conn_reload: true

    - name: Disable connection
      community.general.nmcli:
        conn_name: my-eth1
        state: down

    - name: Reload and enable connection
      community.general.nmcli:
        conn_name: my-eth1
        state: up
        conn_reload: true

    - name: Add second ip4 address
      community.general.nmcli:
        conn_name: my-eth1
        ifname: eth1
        type: ethernet
        ip4:
          - 192.0.2.100/24
          - 192.0.3.100/24
        state: present

    - name: Add second ip6 address
      community.general.nmcli:
        conn_name: my-eth1
        ifname: eth1
        type: ethernet
        ip6:
          - 2001:db8::cafe
          - 2002:db8::cafe
        state: present

    - name: Add VxLan
      community.general.nmcli:
        type: vxlan
        conn_name: vxlan_test1
        vxlan_id: 16
        vxlan_local: 192.168.1.2
        vxlan_remote: 192.168.1.5

    - name: Add gre
      community.general.nmcli:
        type: gre
        conn_name: gre_test1
        ip_tunnel_dev: eth0
        ip_tunnel_local: 192.168.1.2
        ip_tunnel_remote: 192.168.1.5

    - name: Add ipip
      community.general.nmcli:
        type: ipip
        conn_name: ipip_test1
        ip_tunnel_dev: eth0
        ip_tunnel_local: 192.168.1.2
        ip_tunnel_remote: 192.168.1.5

    - name: Add sit
      community.general.nmcli:
        type: sit
        conn_name: sit_test1
        ip_tunnel_dev: eth0
        ip_tunnel_local: 192.168.1.2
        ip_tunnel_remote: 192.168.1.5

    - name: Add zone
      community.general.nmcli:
        type: ethernet
        conn_name: my-eth1
        zone: external
        state: present

# nmcli exits with status 0 if it succeeds and exits with a status greater
# than zero when there is a failure. The following list of status codes may be
# returned:
#
#     - 0 Success - indicates the operation succeeded
#     - 1 Unknown or unspecified error
#     - 2 Invalid user input, wrong nmcli invocation
#     - 3 Timeout expired (see --wait option)
#     - 4 Connection activation failed
#     - 5 Connection deactivation failed
#     - 6 Disconnecting device failed
#     - 7 Connection deletion failed
#     - 8 NetworkManager is not running
#     - 9 nmcli and NetworkManager versions mismatch
#     - 10 Connection, device, or access point does not exist.

- name: Create the wifi connection
  community.general.nmcli:
    type: wifi
    conn_name: Brittany
    ifname: wlp4s0
    ssid: Brittany
    wifi_sec:
      key-mgmt: wpa-psk
      psk: my_password
    autoconnect: true
    state: present

- name: Create a hidden AP mode wifi connection
  community.general.nmcli:
    type: wifi
    conn_name: ChocoMaster
    ifname: wlo1
    ssid: ChocoMaster
    wifi:
      hidden: true
      mode: ap
    autoconnect: true
    state: present

- name: Create a gsm connection
  community.general.nmcli:
    type: gsm
    conn_name: my-gsm-provider
    ifname: cdc-wdm0
    gsm:
      apn: my.provider.apn
      username: my-provider-username
      password: my-provider-password
      pin: my-sim-pin
    autoconnect: true
    state: present

- name: Create a macvlan connection
  community.general.nmcli:
    type: macvlan
    conn_name: my-macvlan-connection
    ifname: mymacvlan0
    macvlan:
      mode: 2
      parent: eth1
    autoconnect: true
    state: present

- name: Create a wireguard connection
  community.general.nmcli:
    type: wireguard
    conn_name: my-wg-provider
    ifname: mywg0
    wireguard:
      listen-port: 51820
      private-key: my-private-key
    autoconnect: true
    state: present

- name: >-
    Create a VPN L2TP connection for ansible_user to connect on vpn.example.com
    authenticating with user 'brittany' and pre-shared key as 'Brittany123'
  community.general.nmcli:
    type: vpn
    conn_name: my-vpn-connection
    vpn:
      permissions: "{{ ansible_user }}"
      service-type: org.freedesktop.NetworkManager.l2tp
      gateway: vpn.example.com
      password-flags: 2
      user: brittany
      ipsec-enabled: true
      ipsec-psk: "0s{{ 'Brittany123' | ansible.builtin.b64encode }}"
    autoconnect: false
    state: present

## Creating bond attached to bridge example
- name: Create bond attached to bridge
  community.general.nmcli:
    type: bond
    conn_name: bond0
    slave_type: bridge
    master: br0
    state: present

- name: Create master bridge
  community.general.nmcli:
    type: bridge
    conn_name: br0
    method4: disabled
    method6: disabled
    state: present

## Creating vlan connection attached to bridge
- name: Create master bridge
  community.general.nmcli:
    type: bridge
    conn_name: br0
    state: present

- name: Create VLAN 5
  community.general.nmcli:
    type: vlan
    conn_name: eth0.5
    slave_type: bridge
    master: br0
    vlandev: eth0
    vlanid: 5
    state: present

## Creating VRF and adding VLAN interface to it
- name: Create VRF
  community.general.nmcli:
    type: vrf
    ifname: vrf10
    table: 10
    state: present
    conn_name: vrf10
    method4: disabled
    method6: disabled

- name: Create VLAN interface inside VRF
  community.general.nmcli:
    conn_name: "eth0.124"
    type: vlan
    vlanid: "124"
    vlandev: "eth0"
    master: "vrf10"
    slave_type: vrf
    state: "present"
    ip4: '192.168.124.50'
    gw4: '192.168.124.1'

## Defining ip rules while setting a static IP
## table 'production' is set with id 200 in this example.
- name: Set Static ips for interface with ip rules and routes
  community.general.nmcli:
    type: ethernet
    conn_name: 'eth0'
    ip4: '192.168.1.50'
    gw4: '192.168.1.1'
    state: present
    routes4_extended:
      - ip: "0.0.0.0/0"
        next_hop: "192.168.1.1"
        table: "production"
    routing_rules4:
      - "priority 0 from 192.168.1.50 table 200"

## Creating an OVS bridge and attaching a port
- name: Create OVS Bridge
  community.general.nmcli:
    conn_name: ovs-br-conn
    ifname: ovs-br
    type: ovs-bridge
    state: present

- name: Create OVS Port for OVS Bridge Interface
  community.general.nmcli:
    conn_name: ovs-br-interface-port-conn
    ifname: ovs-br-interface-port
    master: ovs-br
    type: ovs-port
    state: present

## Adding an ethernet interface to an OVS bridge port
- name: Add Ethernet Interface to OVS Port
  community.general.nmcli:
    conn_name: eno1
    ifname: eno1
    master: ovs-br-interface-port
    slave_type: ovs-port
    type: ethernet
    state: present
"""

RETURN = r"""#
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
import re


class NmcliModuleError(Exception):
    pass


class Nmcli(object):
    """
    This is the generic nmcli manipulation class that is subclassed based on platform.
    A subclass may wish to override the following action methods:-
            - create_connection()
            - delete_connection()
            - edit_connection()
            - modify_connection()
            - show_connection()
            - up_connection()
            - down_connection()
    All subclasses MUST define platform and distribution (which may be None).
    """

    platform = 'Generic'
    distribution = None

    SECRET_OPTIONS = (
        '802-11-wireless-security.leap-password',
        '802-11-wireless-security.psk',
        '802-11-wireless-security.wep-key0',
        '802-11-wireless-security.wep-key1',
        '802-11-wireless-security.wep-key2',
        '802-11-wireless-security.wep-key3'
    )

    def __init__(self, module):
        self.module = module
        self.state = module.params['state']
        self.ignore_unsupported_suboptions = module.params['ignore_unsupported_suboptions']
        self.autoconnect = module.params['autoconnect']
        self.autoconnect_priority = module.params['autoconnect_priority']
        self.autoconnect_retries = module.params['autoconnect_retries']
        self.conn_name = module.params['conn_name']
        self.conn_reload = module.params['conn_reload']
        self.slave_type = module.params['slave_type']
        self.master = module.params['master']
        self.ifname = module.params['ifname']
        self.type = module.params['type']
        self.ip4 = module.params['ip4']
        self.gw4 = module.params['gw4']
        self.gw4_ignore_auto = module.params['gw4_ignore_auto']
        self.routes4 = module.params['routes4']
        self.routes4_extended = module.params['routes4_extended']
        self.route_metric4 = module.params['route_metric4']
        self.routing_rules4 = module.params['routing_rules4']
        self.never_default4 = module.params['never_default4']
        self.dns4 = module.params['dns4']
        self.dns4_search = module.params['dns4_search']
        self.dns4_options = module.params['dns4_options']
        self.dns4_ignore_auto = module.params['dns4_ignore_auto']
        self.method4 = module.params['method4']
        self.may_fail4 = module.params['may_fail4']
        self.ip6 = module.params['ip6']
        self.gw6 = module.params['gw6']
        self.gw6_ignore_auto = module.params['gw6_ignore_auto']
        self.routes6 = module.params['routes6']
        self.routes6_extended = module.params['routes6_extended']
        self.route_metric6 = module.params['route_metric6']
        self.dns6 = module.params['dns6']
        self.dns6_search = module.params['dns6_search']
        self.dns6_options = module.params['dns6_options']
        self.dns6_ignore_auto = module.params['dns6_ignore_auto']
        self.method6 = module.params['method6']
        self.ip_privacy6 = module.params['ip_privacy6']
        self.addr_gen_mode6 = module.params['addr_gen_mode6']
        self.mtu = module.params['mtu']
        self.stp = module.params['stp']
        self.priority = module.params['priority']
        self.mode = module.params['mode']
        self.miimon = module.params['miimon']
        self.primary = module.params['primary']
        self.downdelay = module.params['downdelay']
        self.updelay = module.params['updelay']
        self.xmit_hash_policy = module.params['xmit_hash_policy']
        self.fail_over_mac = module.params['fail_over_mac']
        self.arp_interval = module.params['arp_interval']
        self.arp_ip_target = module.params['arp_ip_target']
        self.slavepriority = module.params['slavepriority']
        self.forwarddelay = module.params['forwarddelay']
        self.hellotime = module.params['hellotime']
        self.maxage = module.params['maxage']
        self.ageingtime = module.params['ageingtime']
        self.hairpin = module.params['hairpin']
        self.path_cost = module.params['path_cost']
        self.mac = module.params['mac']
        self.runner = module.params['runner']
        self.runner_hwaddr_policy = module.params['runner_hwaddr_policy']
        self.runner_fast_rate = module.params['runner_fast_rate']
        self.vlanid = module.params['vlanid']
        self.vlandev = module.params['vlandev']
        self.flags = module.params['flags']
        self.ingress = module.params['ingress']
        self.egress = module.params['egress']
        self.vxlan_id = module.params['vxlan_id']
        self.vxlan_local = module.params['vxlan_local']
        self.vxlan_remote = module.params['vxlan_remote']
        self.ip_tunnel_dev = module.params['ip_tunnel_dev']
        self.ip_tunnel_local = module.params['ip_tunnel_local']
        self.ip_tunnel_remote = module.params['ip_tunnel_remote']
        self.ip_tunnel_input_key = module.params['ip_tunnel_input_key']
        self.ip_tunnel_output_key = module.params['ip_tunnel_output_key']
        self.nmcli_bin = self.module.get_bin_path('nmcli', True)
        self.dhcp_client_id = module.params['dhcp_client_id']
        self.zone = module.params['zone']
        self.ssid = module.params['ssid']
        self.wifi = module.params['wifi']
        self.wifi_sec = module.params['wifi_sec']
        self.gsm = module.params['gsm']
        self.macvlan = module.params['macvlan']
        self.wireguard = module.params['wireguard']
        self.vpn = module.params['vpn']
        self.transport_mode = module.params['transport_mode']
        self.infiniband_mac = module.params['infiniband_mac']
        self.sriov = module.params['sriov']

        if self.method4:
            self.ipv4_method = self.method4
        elif self.type in ('dummy', 'macvlan', 'wireguard') and not self.ip4:
            self.ipv4_method = 'disabled'
        elif self.ip4:
            self.ipv4_method = 'manual'
        else:
            self.ipv4_method = None

        if self.method6:
            self.ipv6_method = self.method6
        elif self.type in ('dummy', 'macvlan', 'wireguard') and not self.ip6:
            self.ipv6_method = 'disabled'
        elif self.ip6:
            self.ipv6_method = 'manual'
        else:
            self.ipv6_method = None

        if self.type == "vrf":
            self.table = module.params['table']

        self.edit_commands = []

        self.extra_options_validation()

    def extra_options_validation(self):
        """ Additional validation of options set passed to module that cannot be implemented in module's argspecs. """
        if self.type not in ("bridge-slave", "team-slave", "bond-slave"):
            if self.master is None and self.slave_type is not None:
                self.module.fail_json(msg="'master' option is required when 'slave_type' is specified.")

    def execute_command(self, cmd, use_unsafe_shell=False, data=None):
        if isinstance(cmd, list):
            cmd = [to_text(item) for item in cmd]
        else:
            cmd = to_text(cmd)
        return self.module.run_command(cmd, use_unsafe_shell=use_unsafe_shell, data=data)

    def execute_edit_commands(self, commands, arguments):
        arguments = arguments or []
        cmd = [self.nmcli_bin, 'con', 'edit'] + arguments
        data = "\n".join(commands)
        return self.execute_command(cmd, data=data)

    def connection_options(self, detect_change=False):
        # Options common to multiple connection types.
        options = {
            'connection.autoconnect': self.autoconnect,
            'connection.autoconnect-priority': self.autoconnect_priority,
            'connection.autoconnect-retries': self.autoconnect_retries,
            'connection.zone': self.zone,
        }

        # IP address options.
        # The ovs-interface type can be both ip_conn_type and have a master
        # An interface that has a master but is of slave type vrf can have an IP address
        if (self.ip_conn_type and (not self.master or self.slave_type == "vrf")) or self.type == "ovs-interface":
            options.update({
                'ipv4.addresses': self.enforce_ipv4_cidr_notation(self.ip4),
                'ipv4.dhcp-client-id': self.dhcp_client_id,
                'ipv4.dns': self.dns4,
                'ipv4.dns-search': self.dns4_search,
                'ipv4.dns-options': self.dns4_options,
                'ipv4.ignore-auto-dns': self.dns4_ignore_auto,
                'ipv4.gateway': self.gw4,
                'ipv4.ignore-auto-routes': self.gw4_ignore_auto,
                'ipv4.routes': self.enforce_routes_format(self.routes4, self.routes4_extended),
                'ipv4.route-metric': self.route_metric4,
                'ipv4.routing-rules': self.routing_rules4,
                'ipv4.never-default': self.never_default4,
                'ipv4.method': self.ipv4_method,
                'ipv4.may-fail': self.may_fail4,
                'ipv6.addresses': self.enforce_ipv6_cidr_notation(self.ip6),
                'ipv6.dns': self.dns6,
                'ipv6.dns-search': self.dns6_search,
                'ipv6.dns-options': self.dns6_options,
                'ipv6.ignore-auto-dns': self.dns6_ignore_auto,
                'ipv6.gateway': self.gw6,
                'ipv6.ignore-auto-routes': self.gw6_ignore_auto,
                'ipv6.routes': self.enforce_routes_format(self.routes6, self.routes6_extended),
                'ipv6.route-metric': self.route_metric6,
                'ipv6.method': self.ipv6_method,
                'ipv6.ip6-privacy': self.ip_privacy6,
                'ipv6.addr-gen-mode': self.addr_gen_mode6
            })
            # when 'method' is disabled the 'may_fail' no make sense but accepted by nmcli with keeping 'yes'
            # force ignoring to save idempotency
            if self.ipv4_method and self.ipv4_method != 'disabled':
                options.update({'ipv4.may-fail': self.may_fail4})

        # Layer 2 options.
        if self.mac:
            options.update({self.mac_setting: self.mac})

        if self.mtu_conn_type:
            options.update({self.mtu_setting: self.mtu})

        # Connections that can have a master.
        if self.slave_conn_type:
            options.update({
                'connection.master': self.master,
                'connection.slave-type': self.slave_type,
            })

        # Options specific to a connection type.
        if self.type == 'bond':
            options.update({
                'arp-interval': self.arp_interval,
                'arp-ip-target': self.arp_ip_target,
                'downdelay': self.downdelay,
                'miimon': self.miimon,
                'mode': self.mode,
                'primary': self.primary,
                'updelay': self.updelay,
                'xmit_hash_policy': self.xmit_hash_policy,
                'fail_over_mac': self.fail_over_mac,
            })
        elif self.type == 'bond-slave':
            if self.slave_type and self.slave_type != 'bond':
                self.module.fail_json(msg="Connection type '%s' cannot be combined with '%s' slave-type. "
                                          "Allowed slave-type for '%s' is 'bond'."
                                          % (self.type, self.slave_type, self.type)
                                      )
            if not self.slave_type:
                self.module.warn("Connection 'slave-type' property automatically set to 'bond' "
                                 "because of using 'bond-slave' connection type.")
                options.update({
                    'connection.slave-type': 'bond',
                })
        elif self.type == 'bridge':
            options.update({
                'bridge.ageing-time': self.ageingtime,
                'bridge.forward-delay': self.forwarddelay,
                'bridge.hello-time': self.hellotime,
                'bridge.max-age': self.maxage,
                'bridge.priority': self.priority,
                'bridge.stp': self.stp,
            })
            # priority make sense when stp enabled, otherwise nmcli keeps bridge-priority to 32768 regrdless of input.
            # force ignoring to save idempotency
            if self.stp:
                options.update({'bridge.priority': self.priority})
        elif self.type == 'team':
            options.update({
                'team.runner': self.runner,
                'team.runner-hwaddr-policy': self.runner_hwaddr_policy,
            })
            if self.runner_fast_rate is not None:
                options.update({
                    'team.runner-fast-rate': self.runner_fast_rate,
                })
        elif self.type == 'bridge-slave':
            if self.slave_type and self.slave_type != 'bridge':
                self.module.fail_json(msg="Connection type '%s' cannot be combined with '%s' slave-type. "
                                          "Allowed slave-type for '%s' is 'bridge'."
                                          % (self.type, self.slave_type, self.type)
                                      )
            if not self.slave_type:
                self.module.warn("Connection 'slave-type' property automatically set to 'bridge' "
                                 "because of using 'bridge-slave' connection type.")
                options.update({'connection.slave-type': 'bridge'})
            self.module.warn(
                "Connection type as 'bridge-slave' implies 'ethernet' connection with 'bridge' slave-type. "
                "Consider using slave_type='bridge' with necessary type."
            )
            options.update({
                'bridge-port.path-cost': self.path_cost,
                'bridge-port.hairpin-mode': self.hairpin,
                'bridge-port.priority': self.slavepriority,
            })
        elif self.type == 'team-slave':
            if self.slave_type and self.slave_type != 'team':
                self.module.fail_json(msg="Connection type '%s' cannot be combined with '%s' slave-type. "
                                          "Allowed slave-type for '%s' is 'team'."
                                          % (self.type, self.slave_type, self.type)
                                      )
            if not self.slave_type:
                self.module.warn("Connection 'slave-type' property automatically set to 'team' "
                                 "because of using 'team-slave' connection type.")
                options.update({
                    'connection.slave-type': 'team',
                })
        elif self.tunnel_conn_type:
            options.update({
                'ip-tunnel.local': self.ip_tunnel_local,
                'ip-tunnel.mode': self.type,
                'ip-tunnel.parent': self.ip_tunnel_dev,
                'ip-tunnel.remote': self.ip_tunnel_remote,
            })
            if self.type == 'gre':
                options.update({
                    'ip-tunnel.input-key': self.ip_tunnel_input_key,
                    'ip-tunnel.output-key': self.ip_tunnel_output_key
                })
        elif self.type == 'vlan':
            options.update({
                'vlan.id': self.vlanid,
                'vlan.parent': self.vlandev,
                'vlan.flags': self.flags,
                'vlan.ingress': self.ingress,
                'vlan.egress': self.egress,
            })
        elif self.type == 'vxlan':
            options.update({
                'vxlan.id': self.vxlan_id,
                'vxlan.local': self.vxlan_local,
                'vxlan.remote': self.vxlan_remote,
            })
        elif self.type == 'wifi':
            options.update({
                '802-11-wireless.ssid': self.ssid,
                'connection.slave-type': ('bond' if self.slave_type is None else self.slave_type) if self.master else None,
            })
            if self.wifi:
                for name, value in self.wifi.items():
                    options.update({
                        '802-11-wireless.%s' % name: value
                    })
            if self.wifi_sec:
                for name, value in self.wifi_sec.items():
                    options.update({
                        '802-11-wireless-security.%s' % name: value
                    })
        elif self.type == 'gsm':
            if self.gsm:
                for name, value in self.gsm.items():
                    options.update({
                        'gsm.%s' % name: value,
                    })
        elif self.type == 'macvlan':
            if self.macvlan:
                for name, value in self.macvlan.items():
                    options.update({
                        'macvlan.%s' % name: value,
                    })
            elif self.state == 'present':
                raise NmcliModuleError('type is macvlan but all of the following are missing: macvlan')
        elif self.type == 'wireguard':
            if self.wireguard:
                for name, value in self.wireguard.items():
                    options.update({
                        'wireguard.%s' % name: value,
                    })
        elif self.type == 'vpn':
            if self.vpn:
                vpn_data_values = ''
                for name, value in self.vpn.items():
                    if name == 'service-type':
                        options.update({
                            'vpn.service-type': value,
                        })
                    elif name == 'permissions':
                        options.update({
                            'connection.permissions': value,
                        })
                    else:
                        if vpn_data_values != '':
                            vpn_data_values += ', '

                        if isinstance(value, bool):
                            value = self.bool_to_string(value)

                        vpn_data_values += '%s=%s' % (name, value)
                    options.update({
                        'vpn.data': vpn_data_values,
                    })
        elif self.type == 'infiniband':
            options.update({
                'infiniband.transport-mode': self.transport_mode,
            })
            if self.infiniband_mac:
                options['infiniband.mac-address'] = self.infiniband_mac
        elif self.type == 'vrf':
            options.update({
                'table': self.table,
            })

        if self.type == 'ethernet':
            if self.sriov:
                for name, value in self.sriov.items():
                    options.update({
                        'sriov.%s' % name: value,
                    })

        # Convert settings values based on the situation.
        for setting, value in options.items():
            setting_type = self.settings_type(setting)
            convert_func = None
            if setting_type is bool:
                # Convert all bool options to yes/no.
                convert_func = self.bool_to_string
            if detect_change:
                if setting in ('vlan.id', 'vxlan.id'):
                    # Convert VLAN/VXLAN IDs to text when detecting changes.
                    convert_func = to_text
                elif setting == self.mtu_setting:
                    # MTU is 'auto' by default when detecting changes.
                    convert_func = self.mtu_to_string
                elif setting == 'ipv6.ip6-privacy':
                    convert_func = self.ip6_privacy_to_num
            elif setting_type is list:
                # Convert lists to strings for nmcli create/modify commands.
                convert_func = self.list_to_string

            if callable(convert_func):
                options[setting] = convert_func(value)

        return options

    @property
    def ip_conn_type(self):
        return self.type in (
            'bond',
            'bridge',
            'dummy',
            'ethernet',
            '802-3-ethernet',
            'generic',
            'gre',
            'infiniband',
            'ipip',
            'sit',
            'team',
            'vlan',
            'wifi',
            '802-11-wireless',
            'gsm',
            'macvlan',
            'wireguard',
            'vpn',
            'loopback',
            'ovs-interface',
            'vrf'
        )

    @property
    def mac_setting(self):
        if self.type == 'bridge':
            return 'bridge.mac-address'
        else:
            return '802-3-ethernet.cloned-mac-address'

    @property
    def mtu_conn_type(self):
        return self.type in (
            'bond',
            'bond-slave',
            'dummy',
            'ethernet',
            'infiniband',
            'team-slave',
            'vlan',
        )

    @property
    def mtu_setting(self):
        if self.type == 'infiniband':
            return 'infiniband.mtu'
        else:
            return '802-3-ethernet.mtu'

    @staticmethod
    def mtu_to_string(mtu):
        if not mtu:
            return 'auto'
        else:
            return to_text(mtu)

    @staticmethod
    def ip6_privacy_to_num(privacy):
        ip6_privacy_values = {
            'disabled': '0',
            'prefer-public-addr': '1 (enabled, prefer public IP)',
            'prefer-temp-addr': '2 (enabled, prefer temporary IP)',
            'unknown': '-1',
        }

        if privacy is None:
            return None

        if privacy not in ip6_privacy_values:
            raise AssertionError('{privacy} is invalid ip_privacy6 option'.format(privacy=privacy))

        return ip6_privacy_values[privacy]

    @property
    def slave_conn_type(self):
        return self.type in (
            'ethernet',
            'bridge',
            'bond',
            'vlan',
            'team',
            'wifi',
            'bond-slave',
            'bridge-slave',
            'team-slave',
            'wifi',
            'infiniband',
            'ovs-port',
            'ovs-interface',
        )

    @property
    def tunnel_conn_type(self):
        return self.type in (
            'gre',
            'ipip',
            'sit',
        )

    @staticmethod
    def enforce_ipv4_cidr_notation(ip4_addresses):
        if ip4_addresses is None:
            return None
        return [address if '/' in address else address + '/32' for address in ip4_addresses]

    @staticmethod
    def enforce_ipv6_cidr_notation(ip6_addresses):
        if ip6_addresses is None:
            return None
        return [address if '/' in address else address + '/128' for address in ip6_addresses]

    def enforce_routes_format(self, routes, routes_extended):
        if routes is not None:
            return routes
        elif routes_extended is not None:
            return [self.route_to_string(route) for route in routes_extended]
        else:
            return None

    @staticmethod
    def route_to_string(route):
        result_str = ''
        result_str += route['ip']
        if route.get('next_hop') is not None:
            result_str += ' ' + route['next_hop']
        if route.get('metric') is not None:
            result_str += ' ' + str(route['metric'])

        for attribute, value in sorted(route.items()):
            if attribute not in ('ip', 'next_hop', 'metric') and value is not None:
                result_str += ' {0}={1}'.format(attribute, str(value).lower())

        return result_str

    @staticmethod
    def bool_to_string(boolean):
        if boolean:
            return "yes"
        else:
            return "no"

    @staticmethod
    def list_to_string(lst):
        if lst is None:
            return None
        else:
            return ",".join(lst)

    @staticmethod
    def settings_type(setting):
        if setting in ('bridge.stp',
                       'bridge-port.hairpin-mode',
                       'connection.autoconnect',
                       'ipv4.never-default',
                       'ipv4.ignore-auto-dns',
                       'ipv4.ignore-auto-routes',
                       'ipv4.may-fail',
                       'ipv6.ignore-auto-dns',
                       'ipv6.ignore-auto-routes',
                       '802-11-wireless.hidden',
                       'team.runner-fast-rate'):
            return bool
        elif setting in ('ipv4.addresses',
                         'ipv6.addresses',
                         'ipv4.dns',
                         'ipv4.dns-search',
                         'ipv4.dns-options',
                         'ipv4.routes',
                         'ipv4.routing-rules',
                         'ipv6.dns',
                         'ipv6.dns-search',
                         'ipv6.dns-options',
                         'ipv6.routes',
                         '802-11-wireless-security.group',
                         '802-11-wireless-security.leap-password-flags',
                         '802-11-wireless-security.pairwise',
                         '802-11-wireless-security.proto',
                         '802-11-wireless-security.psk-flags',
                         '802-11-wireless-security.wep-key-flags',
                         '802-11-wireless.mac-address-blacklist'):
            return list
        elif setting in ('connection.autoconnect-priority',
                         'connection.autoconnect-retries'):
            return int
        return str

    def get_route_params(self, raw_values):
        routes_params = []
        for raw_value in raw_values:
            route_params = {}
            for parameter, value in re.findall(r'([\w-]*)\s?=\s?([^\s,}]*)', raw_value):
                if parameter == 'nh':
                    route_params['next_hop'] = value
                elif parameter == 'mt':
                    route_params['metric'] = value
                else:
                    route_params[parameter] = value
            routes_params.append(route_params)
        return [self.route_to_string(route_params) for route_params in routes_params]

    def list_connection_info(self):
        cmd = [self.nmcli_bin, '--fields', 'name', '--terse', 'con', 'show']
        (rc, out, err) = self.execute_command(cmd)
        if rc != 0:
            raise NmcliModuleError(err)
        return out.splitlines()

    def connection_exists(self):
        return self.conn_name in self.list_connection_info()

    def down_connection(self):
        cmd = [self.nmcli_bin, 'con', 'down', self.conn_name]
        return self.execute_command(cmd)

    def up_connection(self):
        cmd = [self.nmcli_bin, 'con', 'up', self.conn_name]
        return self.execute_command(cmd)

    def reload_connection(self):
        cmd = [self.nmcli_bin, 'con', 'reload']
        return self.execute_command(cmd)

    def connection_update(self, nmcli_command):
        if nmcli_command == 'create':
            cmd = [self.nmcli_bin, 'con', 'add', 'type']
            if self.tunnel_conn_type:
                cmd.append('ip-tunnel')
            else:
                cmd.append(self.type)
            cmd.append('con-name')
        elif nmcli_command == 'modify':
            cmd = [self.nmcli_bin, 'con', 'modify']
        else:
            self.module.fail_json(msg="Invalid nmcli command.")
        cmd.append(self.conn_name)

        # Use connection name as default for interface name on creation.
        if nmcli_command == 'create' and self.ifname is None:
            ifname = self.conn_name
        else:
            ifname = self.ifname

        options = {
            'connection.interface-name': ifname,
        }

        # VPN doesn't need an interface but if sended it must be a valid interface.
        if self.type == 'vpn' and self.ifname is None:
            del options['connection.interface-name']

        options.update(self.connection_options())

        # Constructing the command.
        for key, value in options.items():
            if value is not None:
                if key in self.SECRET_OPTIONS:
                    self.edit_commands += ['set %s %s' % (key, value)]
                    continue
                if key == 'xmit_hash_policy':
                    cmd.extend(['+bond.options', 'xmit_hash_policy=%s' % value])
                    continue
                if key == 'fail_over_mac':
                    cmd.extend(['+bond.options', 'fail_over_mac=%s' % value])
                    continue
                cmd.extend([key, value])

        return self.execute_command(cmd)

    def create_connection(self):
        status = self.connection_update('create')
        if status[0] == 0 and self.edit_commands:
            status = self.edit_connection()
        if self.create_connection_up:
            status = self.up_connection()
        return status

    @property
    def create_connection_up(self):
        if self.type in ('bond', 'dummy', 'ethernet', 'infiniband', 'wifi'):
            if (self.mtu is not None) or (self.dns4 is not None) or (self.dns6 is not None):
                return True
        elif self.type == 'team':
            if (self.dns4 is not None) or (self.dns6 is not None):
                return True
        return False

    def remove_connection(self):
        # self.down_connection()
        cmd = [self.nmcli_bin, 'con', 'del', self.conn_name]
        return self.execute_command(cmd)

    def modify_connection(self):
        status = self.connection_update('modify')
        if status[0] == 0 and self.edit_commands:
            status = self.edit_connection()
        return status

    def edit_connection(self):
        commands = self.edit_commands + ['save', 'quit']
        return self.execute_edit_commands(commands, arguments=[self.conn_name])

    def show_connection(self):
        cmd = [self.nmcli_bin, '--show-secrets', 'con', 'show', self.conn_name]

        (rc, out, err) = self.execute_command(cmd)

        if rc != 0:
            raise NmcliModuleError(err)

        p_enum_value = re.compile(r'^([-]?\d+) \((\w+)\)$')

        conn_info = dict()
        for line in out.splitlines():
            pair = line.split(':', 1)
            key = pair[0].strip()
            key_type = self.settings_type(key)
            if key and len(pair) > 1:
                raw_value = pair[1].lstrip()
                if raw_value == '--':
                    if key_type == list:
                        conn_info[key] = []
                    else:
                        conn_info[key] = None
                elif key == 'bond.options':
                    # Aliases such as 'miimon', 'downdelay' are equivalent to the +bond.options 'option=value' syntax.
                    opts = raw_value.split(',')
                    for opt in opts:
                        alias_pair = opt.split('=', 1)
                        if len(alias_pair) > 1:
                            alias_key = alias_pair[0]
                            alias_value = alias_pair[1]
                            conn_info[alias_key] = alias_value
                elif key in ('ipv4.routes', 'ipv6.routes'):
                    conn_info[key] = [s.strip() for s in raw_value.split(';')]
                elif key_type == list:
                    conn_info[key] = [s.strip() for s in raw_value.split(',')]
                else:
                    m_enum = p_enum_value.match(raw_value)
                    if m_enum is not None:
                        value = m_enum.group(1)
                    else:
                        value = raw_value
                    conn_info[key] = value

        return conn_info

    def get_supported_properties(self, setting):
        properties = []

        if setting == '802-11-wireless-security':
            set_property = 'psk'
            set_value = 'FAKEVALUE'
            commands = ['set %s.%s %s' % (setting, set_property, set_value)]
        else:
            commands = []

        commands += ['print %s' % setting, 'quit', 'yes']

        (rc, out, err) = self.execute_edit_commands(commands, arguments=['type', self.type])

        if rc != 0:
            raise NmcliModuleError(err)

        for line in out.splitlines():
            prefix = '%s.' % setting
            if (line.startswith(prefix)):
                pair = line.split(':', 1)
                property = pair[0].strip().replace(prefix, '')
                properties.append(property)

        return properties

    def check_for_unsupported_properties(self, setting):
        if setting == '802-11-wireless':
            setting_key = 'wifi'
        elif setting == '802-11-wireless-security':
            setting_key = 'wifi_sec'
        else:
            setting_key = setting

        supported_properties = self.get_supported_properties(setting)
        unsupported_properties = []

        for property, value in getattr(self, setting_key).items():
            if property not in supported_properties:
                unsupported_properties.append(property)

        if unsupported_properties:
            msg_options = []
            for property in unsupported_properties:
                msg_options.append('%s.%s' % (setting_key, property))

            msg = 'Invalid or unsupported option(s): "%s"' % '", "'.join(msg_options)
            if self.ignore_unsupported_suboptions:
                self.module.warn(msg)
            else:
                self.module.fail_json(msg=msg)

        return unsupported_properties

    def _compare_conn_params(self, conn_info, options):
        changed = False
        diff_before = dict()
        diff_after = dict()

        for key, value in options.items():
            # We can't just do `if not value` because then if there's a value
            # of 0 specified as an integer it'll be interpreted as empty when
            # it actually isn't.
            if value not in (0, []) and not value:
                continue

            if key in conn_info:
                current_value = conn_info[key]
                if key == '802-11-wireless.wake-on-wlan' and current_value is not None:
                    match = re.match('0x([0-9A-Fa-f]+)', current_value)
                    if match:
                        current_value = str(int(match.group(1), 16))
                if key in ('ipv4.routes', 'ipv6.routes') and current_value is not None:
                    current_value = self.get_route_params(current_value)
                if key == self.mac_setting:
                    # MAC addresses are case insensitive, nmcli always reports them in uppercase
                    value = value.upper()
                    # ensure current_value is also converted to uppercase in case nmcli changes behaviour
                    if current_value:
                        current_value = current_value.upper()
                if key == 'gsm.apn':
                    # Depending on version nmcli adds double-qoutes to gsm.apn
                    # Need to strip them in order to compare both
                    if current_value:
                        current_value = current_value.strip('"')
                if key == self.mtu_setting and self.mtu is None:
                    self.mtu = 0
                if key == 'vpn.data':
                    if current_value:
                        current_value = sorted(re.sub(r'\s*=\s*', '=', part.strip(), count=1) for part in current_value.split(','))
                    value = sorted(part.strip() for part in value.split(','))
            else:
                # parameter does not exist
                current_value = None

            if isinstance(current_value, list) and isinstance(value, list):
                # compare values between two lists
                if key in ('ipv4.addresses', 'ipv6.addresses', 'ipv4.dns', 'ipv6.dns', 'ipv4.dns-search', 'ipv6.dns-search'):
                    # The order of IP addresses matters because the first one
                    # is the default source address for outbound connections.
                    # Similarly, the order of DNS nameservers and search
                    # suffixes is important.
                    changed |= current_value != value
                else:
                    changed |= sorted(current_value) != sorted(value)
            elif all([key == self.mtu_setting, self.type == 'dummy', current_value is None, value == 'auto', self.mtu is None]):
                value = None
            else:
                value = to_text(value)
                if current_value != value:
                    changed = True

            diff_before[key] = current_value
            diff_after[key] = value

        diff = {
            'before': diff_before,
            'after': diff_after,
        }
        return (changed, diff)

    def is_connection_changed(self):
        options = {
            'connection.interface-name': self.ifname,
        }

        # VPN doesn't need an interface but if sended it must be a valid interface.
        if self.type == 'vpn' and self.ifname is None:
            del options['connection.interface-name']

        if not self.type:
            current_con_type = self.show_connection().get('connection.type')
            if current_con_type:
                if current_con_type == '802-11-wireless':
                    current_con_type = 'wifi'
                self.type = current_con_type

        options.update(self.connection_options(detect_change=True))
        return self._compare_conn_params(self.show_connection(), options)


def main():
    # Parsing argument file
    module = AnsibleModule(
        argument_spec=dict(
            ignore_unsupported_suboptions=dict(type='bool', default=False),
            autoconnect=dict(type='bool', default=True),
            autoconnect_priority=dict(type='int'),
            autoconnect_retries=dict(type='int'),
            state=dict(type='str', required=True, choices=['absent', 'present', 'up', 'down']),
            conn_name=dict(type='str', required=True),
            conn_reload=dict(type='bool', default=False),
            master=dict(type='str'),
            slave_type=dict(type='str', choices=['bond', 'bridge', 'team', 'ovs-port', 'vrf']),
            ifname=dict(type='str'),
            type=dict(type='str',
                      choices=[
                          'bond',
                          'bond-slave',
                          'bridge',
                          'bridge-slave',
                          'dummy',
                          'ethernet',
                          'generic',
                          'gre',
                          'infiniband',
                          'ipip',
                          'sit',
                          'team',
                          'team-slave',
                          'vlan',
                          'vxlan',
                          'wifi',
                          'gsm',
                          'macvlan',
                          'wireguard',
                          'vpn',
                          'loopback',
                          'ovs-interface',
                          'ovs-bridge',
                          'ovs-port',
                          'vrf',
                      ]),
            ip4=dict(type='list', elements='str'),
            gw4=dict(type='str'),
            gw4_ignore_auto=dict(type='bool', default=False),
            routes4=dict(type='list', elements='str'),
            routes4_extended=dict(type='list',
                                  elements='dict',
                                  options=dict(
                                      ip=dict(type='str', required=True),
                                      next_hop=dict(type='str'),
                                      metric=dict(type='int'),
                                      table=dict(type='int'),
                                      tos=dict(type='int'),
                                      cwnd=dict(type='int'),
                                      mtu=dict(type='int'),
                                      onlink=dict(type='bool')
                                  )),
            route_metric4=dict(type='int'),
            routing_rules4=dict(type='list', elements='str'),
            never_default4=dict(type='bool', default=False),
            dns4=dict(type='list', elements='str'),
            dns4_search=dict(type='list', elements='str'),
            dns4_options=dict(type='list', elements='str'),
            dns4_ignore_auto=dict(type='bool', default=False),
            method4=dict(type='str', choices=['auto', 'link-local', 'manual', 'shared', 'disabled']),
            may_fail4=dict(type='bool', default=True),
            dhcp_client_id=dict(type='str'),
            ip6=dict(type='list', elements='str'),
            gw6=dict(type='str'),
            gw6_ignore_auto=dict(type='bool', default=False),
            dns6=dict(type='list', elements='str'),
            dns6_search=dict(type='list', elements='str'),
            dns6_options=dict(type='list', elements='str'),
            dns6_ignore_auto=dict(type='bool', default=False),
            routes6=dict(type='list', elements='str'),
            routes6_extended=dict(type='list',
                                  elements='dict',
                                  options=dict(
                                      ip=dict(type='str', required=True),
                                      next_hop=dict(type='str'),
                                      metric=dict(type='int'),
                                      table=dict(type='int'),
                                      cwnd=dict(type='int'),
                                      mtu=dict(type='int'),
                                      onlink=dict(type='bool')
                                  )),
            route_metric6=dict(type='int'),
            method6=dict(type='str', choices=['ignore', 'auto', 'dhcp', 'link-local', 'manual', 'shared', 'disabled']),
            ip_privacy6=dict(type='str', choices=['disabled', 'prefer-public-addr', 'prefer-temp-addr', 'unknown']),
            addr_gen_mode6=dict(type='str', choices=['default', 'default-or-eui64', 'eui64', 'stable-privacy']),
            # Bond Specific vars
            mode=dict(type='str', default='balance-rr',
                      choices=['802.3ad', 'active-backup', 'balance-alb', 'balance-rr', 'balance-tlb', 'balance-xor', 'broadcast']),
            miimon=dict(type='int'),
            downdelay=dict(type='int'),
            updelay=dict(type='int'),
            xmit_hash_policy=dict(type='str'),
            fail_over_mac=dict(type='str', choices=['none', 'active', 'follow']),
            arp_interval=dict(type='int'),
            arp_ip_target=dict(type='str'),
            primary=dict(type='str'),
            # general usage
            mtu=dict(type='int'),
            mac=dict(type='str'),
            zone=dict(type='str'),
            # bridge specific vars
            stp=dict(type='bool', default=True),
            priority=dict(type='int', default=128),
            slavepriority=dict(type='int', default=32),
            forwarddelay=dict(type='int', default=15),
            hellotime=dict(type='int', default=2),
            maxage=dict(type='int', default=20),
            ageingtime=dict(type='int', default=300),
            hairpin=dict(type='bool', default=False),
            path_cost=dict(type='int', default=100),
            # team specific vars
            runner=dict(type='str', default='roundrobin',
                             choices=['broadcast', 'roundrobin', 'activebackup', 'loadbalance', 'lacp']),
            # team active-backup runner specific options
            runner_hwaddr_policy=dict(type='str', choices=['same_all', 'by_active', 'only_active']),
            # team lacp runner specific options
            runner_fast_rate=dict(type='bool'),
            # vlan specific vars
            vlanid=dict(type='int'),
            vlandev=dict(type='str'),
            flags=dict(type='str'),
            ingress=dict(type='str'),
            egress=dict(type='str'),
            # vxlan specific vars
            vxlan_id=dict(type='int'),
            vxlan_local=dict(type='str'),
            vxlan_remote=dict(type='str'),
            # ip-tunnel specific vars
            ip_tunnel_dev=dict(type='str'),
            ip_tunnel_local=dict(type='str'),
            ip_tunnel_remote=dict(type='str'),
            # ip-tunnel type gre specific vars
            ip_tunnel_input_key=dict(type='str', no_log=True),
            ip_tunnel_output_key=dict(type='str', no_log=True),
            # 802-11-wireless* specific vars
            ssid=dict(type='str'),
            wifi=dict(type='dict'),
            wifi_sec=dict(type='dict', no_log=True),
            gsm=dict(type='dict'),
            macvlan=dict(type='dict', options=dict(
                              mode=dict(type='int', choices=[1, 2, 3, 4, 5], required=True),
                              parent=dict(type='str', required=True),
                              promiscuous=dict(type='bool'),
                              tap=dict(type='bool'))),
            wireguard=dict(type='dict'),
            vpn=dict(type='dict'),
            sriov=dict(type='dict'),
            table=dict(type='int'),
            # infiniband specific vars
            transport_mode=dict(type='str', choices=['datagram', 'connected']),
            infiniband_mac=dict(type='str'),

        ),
        mutually_exclusive=[['never_default4', 'gw4'],
                            ['routes4_extended', 'routes4'],
                            ['routes6_extended', 'routes6']],
        required_if=[("type", "wifi", [("ssid")])],
        supports_check_mode=True,
    )
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')

    nmcli = Nmcli(module)

    (rc, out, err) = (None, '', '')
    result = {'conn_name': nmcli.conn_name, 'state': nmcli.state}

    # check for issues
    if nmcli.conn_name is None:
        nmcli.module.fail_json(msg="Please specify a name for the connection")
    # team checks
    if nmcli.type == "team":
        if nmcli.runner_hwaddr_policy and not nmcli.runner == "activebackup":
            nmcli.module.fail_json(msg="Runner-hwaddr-policy is only allowed for runner activebackup")
        if nmcli.runner_fast_rate is not None and nmcli.runner != "lacp":
            nmcli.module.fail_json(msg="runner-fast-rate is only allowed for runner lacp")
    # team-slave checks
    if nmcli.type == 'team-slave' or nmcli.slave_type == 'team':
        if nmcli.master is None:
            nmcli.module.fail_json(msg="Please specify a name for the master when type is %s" % nmcli.type)
        if nmcli.ifname is None:
            nmcli.module.fail_json(msg="Please specify an interface name for the connection when type is %s" % nmcli.type)
    if nmcli.type == 'wifi':
        unsupported_properties = {}
        if nmcli.wifi:
            if 'ssid' in nmcli.wifi:
                module.warn("Ignoring option 'wifi.ssid', it must be specified with option 'ssid'")
                del nmcli.wifi['ssid']
            unsupported_properties['wifi'] = nmcli.check_for_unsupported_properties('802-11-wireless')
        if nmcli.wifi_sec:
            unsupported_properties['wifi_sec'] = nmcli.check_for_unsupported_properties('802-11-wireless-security')
        if nmcli.ignore_unsupported_suboptions and unsupported_properties:
            for setting_key, properties in unsupported_properties.items():
                for property in properties:
                    del getattr(nmcli, setting_key)[property]

    try:
        if nmcli.state == 'absent':
            if nmcli.connection_exists():
                if module.check_mode:
                    module.exit_json(changed=True)
                (rc, out, err) = nmcli.down_connection()
                (rc, out, err) = nmcli.remove_connection()
                if rc != 0:
                    module.fail_json(name=('No Connection named %s exists' % nmcli.conn_name), msg=err, rc=rc)

        elif nmcli.state == 'present':
            if nmcli.connection_exists():
                changed, diff = nmcli.is_connection_changed()
                if module._diff:
                    result['diff'] = diff

                if changed:
                    # modify connection (note: this function is check mode aware)
                    # result['Connection']=('Connection %s of Type %s is not being added' % (nmcli.conn_name, nmcli.type))
                    result['Exists'] = 'Connections do exist so we are modifying them'
                    if module.check_mode:
                        module.exit_json(changed=True, **result)
                    (rc, out, err) = nmcli.modify_connection()
                    if nmcli.conn_reload:
                        (rc, out, err) = nmcli.reload_connection()
                else:
                    result['Exists'] = 'Connections already exist and no changes made'
                    if module.check_mode:
                        module.exit_json(changed=False, **result)
            if not nmcli.connection_exists():
                result['Connection'] = ('Connection %s of Type %s is being added' % (nmcli.conn_name, nmcli.type))
                if module.check_mode:
                    module.exit_json(changed=True, **result)
                (rc, out, err) = nmcli.create_connection()
            if rc is not None and rc != 0:
                module.fail_json(name=nmcli.conn_name, msg=err, rc=rc)

        elif nmcli.state == 'up':
            if nmcli.connection_exists():
                if module.check_mode:
                    module.exit_json(changed=True)
                if nmcli.conn_reload:
                    (rc, out, err) = nmcli.reload_connection()
                (rc, out, err) = nmcli.up_connection()
                if rc != 0:
                    module.fail_json(name=('No Connection named %s exists' % nmcli.conn_name), msg=err, rc=rc)

        elif nmcli.state == 'down':
            if nmcli.connection_exists():
                if module.check_mode:
                    module.exit_json(changed=True)
                if nmcli.conn_reload:
                    (rc, out, err) = nmcli.reload_connection()
                (rc, out, err) = nmcli.down_connection()
                if rc != 0:
                    module.fail_json(name=('No Connection named %s exists' % nmcli.conn_name), msg=err, rc=rc)

    except NmcliModuleError as e:
        module.fail_json(name=nmcli.conn_name, msg=str(e))

    if rc is None:
        result['changed'] = False
    else:
        result['changed'] = True
    if out:
        result['stdout'] = out
    if err:
        result['stderr'] = err

    module.exit_json(**result)


if __name__ == '__main__':
    main()
