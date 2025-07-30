from colav_protobuf_utils import ProtoType
from colav_protobuf_utils.deserialization import deserialize_protobuf
from rclpy.node import Node
from colav_interfaces.msg import Waypoint
from hybrid_automaton_interfaces.action import HybridAutomatonExecuteMission
from std_msgs.msg import Header
from .utils import parse_vessel, parse_point, parse_waypoints, parse_stamp
from builtin_interfaces.msg import Time

def parse_mission_request(msg: bytes) -> HybridAutomatonExecuteMission.Goal:
    """Parse mission request protobuf to ros"""
    try: 
        protobuf_mission_request = deserialize_protobuf(msg, ProtoType.MISSION_REQUEST)
        return HybridAutomatonExecuteMission.Goal(
                stamp = parse_stamp(protobuf_mission_request.stamp),
                goal_waypoints = parse_waypoints((list(protobuf_mission_request.goal_waypoints))),
        )
    except Exception as e: 
        raise ValueError(f"Error parsing mission request: {e}") from e