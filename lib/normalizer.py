from datetime import datetime


def normalize_pitch_features(
    pitch_hand: str,
    velocity: float,
    pfx_x: float,
    pfx_z: float,
    spin_rate: int,
    game_date,
) -> dict:
    """
    Normalize pitch tracking features to a consistent reference frame.

    Returns a dict of normalized features ready for classification.
    """
    if isinstance(game_date, str):
        game_date = datetime.strptime(game_date, "%Y-%m-%d").date()

    # Normalize coordinate frame: flip pfx_x for left-handed pitchers
    if pitch_hand == "L":
        pfx_x = -pfx_x
        pfx_z = -pfx_z

    return {
        "velocity": velocity,
        "pfx_x": pfx_x,
        "pfx_z": pfx_z,
        "spin_rate": spin_rate,
        "pitch_hand": pitch_hand,
    }
