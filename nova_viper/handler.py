# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Viper request handler."""

import webob.dec
import webob.exc
from webob import Response
import json
import posixpath

from nova.api.validator import validate_ipv4
from nova import exception
from nova.openstack.common import cfg
from nova.openstack.common import log as logging
from nova import wsgi
from nova import utils

CONF = cfg.CONF
service_opts = [
    cfg.IntOpt('viper_listen_port',
               default=7000,
               help='port for viper api to listen'),
     ]


CONF.register_opts(service_opts)


LOG = logging.getLogger(__name__)


class ViperRequestHandler(wsgi.Application):
    """VIPer"""

    def __init__(self):
        pass

    def get_ipv4_addresses(self):

        out, err = utils.execute('ip', 'addr' , 'show')
        ips = []
        for line in out.split('\n'):
            fields = line.split()
            if fields and fields[0] == 'inet':
                ip = fields[1:-1][0].split('/')[0]
                ips.append(ip)
        return  ips

    def check_ipv4(self, ipv4):
        if validate_ipv4(ipv4):
             if ipv4 in self.get_ipv4_addresses():
                 return 0
        return 1


    @webob.dec.wsgify(RequestClass=wsgi.Request)
    def __call__(self, req):
        #if os.path.normpath("/" + req.path_info) == "/":
        #    return(base.ec2_md_print(base.VERSIONS + ["latest"]))

        path = req.path_info
        if path == "" or path[0] != "/":
            path = posixpath.normpath("/" + path)
        else:
            path = posixpath.normpath(path)

        path_tokens = path.split('/')[1:]

        if path_tokens[0] not in ("ip", "help"):
            if path_tokens[0] == "":
                # request for /
                #path_tokens = ["ip"]
                #TODO
                raise webob.exc.HTTPNotFound()
        elif path_tokens[0] == u'ip' and path_tokens[1]:
            data = self.check_ipv4(path_tokens[1])
        else:
            #TODO
            raise webob.exc.HTTPNotFound()

        return Response(json.dumps(data), content_type='application/json')

