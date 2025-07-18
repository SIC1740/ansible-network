# -*- coding: utf-8 -*-
# Copyright 2025 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function


__metaclass__ = type

#############################################
#                WARNING                    #
#############################################
#
# This file is auto generated by the
# ansible.content_builder.
#
# Manually editing this file is not advised.
#
# To update the argspec make the desired changes
# in the documentation in the module file and re-run
# ansible.content_builder commenting out
# the path to external 'docstring' in build.yaml.
#
##############################################

"""
The arg spec for the ios_hsrp_interfaces module
"""


class Hsrp_interfacesArgs(object):  # pylint: disable=R0903
    """The arg spec for the ios_hsrp_interfaces module"""

    argument_spec = {
        "config": {
            "type": "list",
            "elements": "dict",
            "options": {
                "name": {"type": "str", "required": True},
                "bfd": {"type": "bool"},
                "delay": {
                    "type": "dict",
                    "options": {
                        "minimum": {"type": "int"},
                        "reload": {"type": "int"},
                    },
                },
                "follow": {"type": "str"},
                "redirect": {
                    "type": "dict",
                    "options": {
                        "advertisement": {
                            "type": "dict",
                            "options": {
                                "authentication": {
                                    "type": "dict",
                                    "options": {
                                        "key_chain": {
                                            "type": "str",
                                            "no_log": False,
                                        },
                                        "key_string": {"type": "bool"},
                                        "encryption": {
                                            "type": "str",
                                            "no_log": True,
                                        },
                                        "time_out": {"type": "int"},
                                        "password_text": {
                                            "type": "str",
                                            "no_log": True,
                                        },
                                    },
                                },
                            },
                        },
                        "timers": {
                            "type": "dict",
                            "options": {
                                "adv_timer": {"type": "int"},
                                "holddown_timer": {"type": "int"},
                            },
                        },
                    },
                },
                "mac_refresh": {"type": "int"},
                "use_bia": {
                    "type": "dict",
                    "options": {
                        "scope": {
                            "type": "dict",
                            "options": {"interface": {"type": "bool"}},
                        },
                    },
                },
                "version": {"type": "int"},
                "standby_groups": {
                    "type": "list",
                    "elements": "dict",
                    "options": {
                        "group_no": {"type": "int"},
                        "follow": {"type": "str"},
                        "ip": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "virtual_ip": {"type": "str"},
                                "secondary": {"type": "bool"},
                            },
                        },
                        "ipv6": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "ipv6_link": {"type": "str"},
                                "ipv6_prefix": {"type": "str"},
                                "autoconfig": {"type": "bool"},
                            },
                        },
                        "mac_address": {"type": "str"},
                        "group_name": {"type": "str"},
                        "authentication": {
                            "type": "dict",
                            "options": {
                                "advertisement": {
                                    "type": "dict",
                                    "options": {
                                        "key_chain": {
                                            "type": "str",
                                            "no_log": False,
                                        },
                                        "key_string": {"type": "bool"},
                                        "encryption": {"type": "int"},
                                        "time_out": {"type": "int"},
                                        "password_text": {
                                            "type": "str",
                                            "no_log": True,
                                        },
                                        "text": {
                                            "type": "dict",
                                            "options": {
                                                "password_text": {
                                                    "type": "str",
                                                    "no_log": True,
                                                },
                                            },
                                        },
                                    },
                                },
                            },
                        },
                        "preempt": {
                            "type": "dict",
                            "options": {
                                "enabled": {"type": "bool"},
                                "minimum": {"type": "int"},
                                "reload": {"type": "int"},
                                "sync": {"type": "int"},
                                "delay": {"type": "bool"},
                            },
                        },
                        "priority": {"type": "int"},
                        "timers": {
                            "type": "dict",
                            "options": {
                                "hello_interval": {"type": "int"},
                                "hold_time": {"type": "int"},
                                "msec": {
                                    "type": "dict",
                                    "options": {
                                        "hello_interval": {"type": "int"},
                                        "hold_time": {"type": "int"},
                                    },
                                },
                            },
                        },
                        "track": {
                            "type": "list",
                            "elements": "dict",
                            "options": {
                                "track_no": {"type": "int"},
                                "decrement": {"type": "int"},
                                "shutdown": {"type": "bool"},
                            },
                        },
                    },
                },
            },
        },
        "running_config": {"type": "str"},
        "state": {
            "choices": [
                "merged",
                "replaced",
                "overridden",
                "deleted",
                "rendered",
                "gathered",
                "parsed",
            ],
            "default": "merged",
            "type": "str",
        },
    }  # pylint: disable=C0301
