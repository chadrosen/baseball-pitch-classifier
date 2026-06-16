from collections import defaultdict


class PitcherStats:
    def __init__(self):
        self._data = {}

    def record(self, pitcher_id: str, pitch_type: str, velocity: float) -> None:
        if pitcher_id not in self._data:
            self._data[pitcher_id] = {
                'pitch_counts': defaultdict(int),
                'total_velocity': 0.0,
                'pitch_count': 0,
            }
        entry = self._data[pitcher_id]
        entry['pitch_counts'][pitch_type] += 1
        entry['total_velocity'] += velocity
        entry['pitch_count'] += 1

    def get(self, pitcher_id: str):
        if pitcher_id not in self._data:
            return None
        entry = self._data[pitcher_id]
        count = entry['pitch_count']
        # Bug 6: divides by count + 1 instead of count — average is slightly low
        avg_velo = round(entry['total_velocity'] / (count + 1), 1)
        return {
            'pitcher_id': pitcher_id,
            'total_pitches': count,
            'avg_velocity': avg_velo,
            'pitch_mix': dict(entry['pitch_counts']),
        }
