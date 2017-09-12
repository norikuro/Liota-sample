# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------#
#  Copyright © 2015-2016 VMware, Inc. All Rights Reserved.                    #
#                                                                             #
#  Licensed under the BSD 2-Clause License (the “License”); you may not use   #
#  this file except in compliance with the License.                           #
#                                                                             #
#  The BSD 2-Clause License                                                   #
#                                                                             #
#  Redistribution and use in source and binary forms, with or without         #
#  modification, are permitted provided that the following conditions are met:#
#                                                                             #
#  - Redistributions of source code must retain the above copyright notice,   #
#      this list of conditions and the following disclaimer.                  #
#                                                                             #
#  - Redistributions in binary form must reproduce the above copyright        #
#      notice, this list of conditions and the following disclaimer in the    #
#      documentation and/or other materials provided with the distribution.   #
#                                                                             #
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"#
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE  #
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE #
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE  #
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR        #
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF       #
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS   #
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN    #
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)    #
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF     #
#  THE POSSIBILITY OF SUCH DAMAGE.                                            #
# ----------------------------------------------------------------------------#

import bme280_custom

from linux_metrics import cpu_stat
from liota.dcc_comms.socket_comms import SocketDccComms
from liota.dccs.graphite import Graphite
from liota.entities.metrics.metric import Metric
from liota.entities.edge_systems.raspberrypi_edge_system import RaspberrypiEdgeSystem
from liota.lib.utilities.utility import read_user_config

# getting values from conf file
config = read_user_config('sampleProp.conf')

def get_data():
    t = bme280_custom.get_data()
    while True:
        if t != None:
#            print(t)
            break
        else:
            t = bme280_custom.get_data()
    return t

def get_temperature():
    return get_data()[0]

def get_pressure():
    return get_data()[1]

def get_humidity():
    return get_data()[2]

# ---------------------------------------------------------------------------
# In this example, we demonstrate how a Raspberry Pi Gateway metric (e.g.,
# CPU utilization) can be directed to graphite data center component
# using Liota. The program illustrates the ease of use Liota brings
# to IoT application developers.

if __name__ == '__main__':

    edge_system = RaspberrypiEdgeSystem(config['EdgeSystemName'])
    
    # Sending data to Graphite data center component
    # Socket is the underlying transport used to connect to the Graphite
    # instance
    graphite = Graphite(SocketDccComms(ip=config['GraphiteIP'],
                               port=config['GraphitePort']))
    
    graphite_reg_edge_system = graphite.register(edge_system)
   
    metric_name_t = config['MetricName_temperature']
    temperature = Metric(
        name=metric_name_t,
        interval=3,
        sampling_function=get_temperature
    )
    reg_temperature = graphite.register(temperature)
    graphite.create_relationship(graphite_reg_edge_system, reg_temperature)
    reg_temperature.start_collecting()

    metric_name_p = config['MetricName_pressure']
    pressure = Metric(
        name=metric_name_p,
        interval=3,
        sampling_function=get_pressure
    )
    
    reg_pressure = graphite.register(pressure)
    graphite.create_relationship(graphite_reg_edge_system, reg_pressure)
    reg_pressure.start_collecting()

    metric_name_h = config['MetricName_humidity']
    humidity = Metric(
        name=metric_name_h,
        interval=3,
        sampling_function=get_humidity
    )
    
    reg_humidity = graphite.register(humidity)
    graphite.create_relationship(graphite_reg_edge_system, reg_humidity)
    reg_humidity.start_collecting()
