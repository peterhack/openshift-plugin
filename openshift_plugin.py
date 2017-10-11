import requests
import json
import logging
from ruxit.api.base_plugin import BasePlugin
from ruxit.api.snapshot import pgi_name

class DemoPlugin(BasePlugin):
    def initialize(self, **kwargs):
        self.json_config = kwargs["json_config"]
        self.metrics = kwargs["json_config"]["metrics"]

    def query(self, **kwargs):
        config = kwargs["config"]
        user = config["user"]
        password = config["password"]
        domain = config["domain"]
        port = config["port"]
        uri = config["uri"]
        
        pgi = self.find_single_process_group(pgi_name('openshift'))
        pgi_id = pgi.group_instance_id
        stats_url = ("http://"+domain+":"+port+uri)
        #stats_url = ("http://64.15.185.89:9000/metrics/snapshot")
        stats = json.loads(requests.get(stats_url, auth=(user, password)).content.decode())

        for metric in self.metrics:
            stat_key = metric["source"]["stat"]
            print(stat_key)
            stat_value = stats[stat_key]
            metric_key = metric["timeseries"]["key"]

            self.results_builder.absolute(
                key = metric_key,
                value = stat_value,
                entity_id = pgi_id
            )
