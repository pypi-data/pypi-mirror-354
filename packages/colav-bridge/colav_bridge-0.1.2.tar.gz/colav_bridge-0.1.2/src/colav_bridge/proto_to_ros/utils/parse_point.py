from geometry_msgs.msg import Point

def parse_point(point):
    """Parse a protobuf point to ros."""
    try: 
        return Point(
            x=point.x,
            y=point.y,
            z=point.z
        )
    except Exception as e: 
        raise ValueError("Error parsing point") from e
