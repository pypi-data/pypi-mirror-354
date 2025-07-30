"""Provides mid level layer"""

from science_mode_4.layer import Layer
from science_mode_4.utils.logger import logger
from .mid_level_current_data import PacketMidLevelGetCurrentData, PacketMidLevelGetCurrentDataAck
from .mid_level_stop import PacketMidLevelStop, PacketMidLevelStopAck
from .mid_level_update import PacketMidLevelUpdate, PacketMidLevelUpdateAck
from .mid_level_types import MidLevelChannelConfiguration
from .mid_level_init import PacketMidLevelInit, PacketMidLevelInitAck


class LayerMidLevel(Layer):
    """Class for mid level layer"""


    async def init(self, do_stop_on_all_errors: bool):
        """Send mid level init command and waits for response"""
        p = PacketMidLevelInit()
        p.do_stop_on_all_errors = do_stop_on_all_errors
        ack: PacketMidLevelInitAck = await self.send_packet_and_wait(p)
        self._check_result_error(ack.result_error, "MidLevelInit")
        logger().info("Mid level init")


    async def stop(self):
        """Send mid level stop command and waits for response"""
        p = PacketMidLevelStop()
        ack: PacketMidLevelStopAck = await self.send_packet_and_wait(p)
        self._check_result_error(ack.result_error, "MidLevelStop")
        logger().info("Mid level stop")


    async def update(self, channel_configuration: list[MidLevelChannelConfiguration]):
        """Send mid level update command and waits for response"""
        p = PacketMidLevelUpdate()
        p.channel_configuration = channel_configuration
        ack: PacketMidLevelUpdateAck = await self.send_packet_and_wait(p)
        self._check_result_error(ack.result_error, "MidLevelUpdate")
        logger().info("Mid level update")


    async def get_current_data(self) -> list[bool]:
        """Send mid level get current data command and waits for response"""
        p = PacketMidLevelGetCurrentData()
        ack: PacketMidLevelGetCurrentDataAck = await self.send_packet_and_wait(p)
        self._check_result_error(ack.result_error, "MidLevelGetCurrentData")
        if True in ack.channel_error:
            raise ValueError(f"Error mid level get current data channel error {ack.channel_error}")
        logger().info("Mid level get current data, active channels: %s", ack.is_stimulation_active_per_channel)
        return ack.is_stimulation_active_per_channel
