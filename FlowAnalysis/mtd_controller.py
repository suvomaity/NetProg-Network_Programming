from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ether_types, arp
import random
import threading
import time


class MTDController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MTDController, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.ip_map = {}
        self.hosts = ["10.0.0.1", "10.0.0.2"]  # Real IPs
        self.fake_ip_prefix = "172.16.1."
        threading.Thread(target=self.ip_hopping_loop, daemon=True).start()

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, CONFIG_DISPATCHER])
    def register_switch(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.logger.info(f"Switch {datapath.id} connected.")
                self.datapaths[datapath.id] = datapath

    def ip_hopping_loop(self):
        while True:
            self.generate_unique_fake_ips()
            for dp in self.datapaths.values():
                self.clear_flows(dp)
                self.install_flows(dp)
            time.sleep(10)  # Hopping interval

    def generate_unique_fake_ips(self):
        fake_octets = random.sample(range(1, 255), len(self.hosts))
        self.ip_map = {
            real: f"{self.fake_ip_prefix}{octet}"
            for real, octet in zip(self.hosts, fake_octets)
        }
        self.logger.info(f"[IP HOP] Updated mapping: {self.ip_map}")

    def clear_flows(self, datapath):
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        match = parser.OFPMatch()
        mod = parser.OFPFlowMod(
            datapath=datapath,
            command=ofproto.OFPFC_DELETE,
            out_port=ofproto.OFPP_ANY,
            out_group=ofproto.OFPG_ANY,
            match=match
        )
        datapath.send_msg(mod)
        self.logger.info(f"[CLEAR] Flows cleared for datapath {datapath.id}")

    def install_flows(self, datapath):
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        for real_ip, fake_ip in self.ip_map.items():
            # Fake → Real (for incoming packets)
            match_dst = parser.OFPMatch(eth_type=0x0800, ipv4_dst=fake_ip)
            actions_dst = [parser.OFPActionSetField(ipv4_dst=real_ip),
                           parser.OFPActionOutput(ofproto.OFPP_NORMAL)]
            inst_dst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions_dst)]
            mod_dst = parser.OFPFlowMod(datapath=datapath, priority=200,
                                        match=match_dst, instructions=inst_dst)
            datapath.send_msg(mod_dst)
            self.logger.info(f"[FLOW] dst: {fake_ip} → {real_ip}")

            # Real → Fake (for outgoing packets)
            match_src = parser.OFPMatch(eth_type=0x0800, ipv4_src=real_ip)
            actions_src = [parser.OFPActionSetField(ipv4_src=fake_ip),
                           parser.OFPActionOutput(ofproto.OFPP_NORMAL)]
            inst_src = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions_src)]
            mod_src = parser.OFPFlowMod(datapath=datapath, priority=200,
                                        match=match_src, instructions=inst_src)
            datapath.send_msg(mod_src)
            self.logger.info(f"[FLOW] src: {real_ip} → {fake_ip}")

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def handle_packet_in(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        parser = datapath.ofproto_parser
        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]

        if eth.ethertype == ether_types.ETH_TYPE_ARP:
            # Flood ARP packets to ensure MAC learning
            out = parser.OFPPacketOut(
                datapath=datapath,
                buffer_id=msg.buffer_id,
                in_port=msg.match['in_port'],
                actions=[parser.OFPActionOutput(datapath.ofproto.OFPP_FLOOD)],
                data=msg.data
            )
            datapath.send_msg(out)
