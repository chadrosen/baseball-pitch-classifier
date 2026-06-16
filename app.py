from flask import Flask, request, jsonify, abort
from lib.classifier import classify_pitch
from lib.normalizer import normalize_pitch_features
from lib.stats import PitcherStats

app = Flask(__name__)
_stats = PitcherStats()


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


@app.route('/classify', methods=['POST'])
def classify():
    body = request.get_json(silent=True)
    if not body:
        abort(400, description='Request body must be JSON')

    required = ['pitcher_id', 'pitch_hand', 'velocity',
                'pfx_x', 'pfx_z', 'spin_rate', 'game_date']
    for field in required:
        if field not in body:
            abort(400, description=f'Missing required field: {field}')

    features = normalize_pitch_features(
        pitch_hand=body['pitch_hand'],
        velocity=float(body['velocity']),
        pfx_x=float(body['pfx_x']),
        pfx_z=float(body['pfx_z']),
        spin_rate=int(body['spin_rate']),
        game_date=body['game_date'],
    )

    pitch_type = classify_pitch(features)
    _stats.record(body['pitcher_id'], pitch_type, features['velocity'])

    # Bug 5: response key is 'type'; spec requires 'pitch_type'
    return jsonify({'type': pitch_type})


# Bug 3: route is /pitcher/<id>/stats; spec requires /stats/<pitcher_id>
@app.route('/pitcher/<pitcher_id>/stats', methods=['GET'])
def pitcher_stats(pitcher_id):
    data = _stats.get(pitcher_id)
    if data is None:
        # Bug 4: should abort(404) but returns 200 with error body
        return jsonify({'error': f'No data for pitcher {pitcher_id}'})
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
