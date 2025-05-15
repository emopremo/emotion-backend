from flask import Flask, request, jsonify, send_file
from datetime import datetime
import json
import os
import random
from gtts import gTTS

app = Flask(__name__)

TRIGGER_RESPONSES = {
    "happy": ["You're glowing today. Keep pushing forward.", "That smile can move mountains."],
    "sad": ["It's okay to feel this way. You're not alone.", "Lean into the feeling. It will pass."],
    "angry": ["Take a breath. You're in control.", "Channel the fire. Let it fuel your next move."],
    "surprised": ["Something unexpected? Stay curious.", "The unknown holds opportunity."],
    "fearful": ["You're safe. Fear is just a signal.", "Face it. You're stronger than you think."],
    "disgusted": ["Not everything deserves your energy.", "Let it go. It’s not worth it."]
}

PSYCHOLOGICAL_CTAS = {
    "happy": [("Get exclusive early access to our motivation kit.", "https://cash.app/$poplockitup")],
    "sad": [("Tap here to unlock our resilience journal.", "https://cash.app/$poplockitup")],
    "angry": [("Refocus your fire with this guide.", "https://cash.app/$poplockitup")],
    "fearful": [("Build courage now — start with this free tool.", "https://cash.app/$poplockitup")],
    "disgusted": [("Cleanse your space: claim our detox PDF.", "https://cash.app/$poplockitup")]
}

@app.route('/emotion', methods=['POST'])
def receive_emotion():
    data = request.json
    emotion = data.get('emotion')
    score = data.get('score')
    timestamp = datetime.utcnow().isoformat()
    print(f"[Captured] {timestamp} - {emotion} ({score:.2f})")

    log_entry = {"time": timestamp, "emotion": emotion, "score": score}
    log_path = os.path.join(os.path.dirname(__file__), "emotion_log.json")
    with open(log_path, "a") as log:
        log.write(json.dumps(log_entry) + "\n")

    response_text = random.choice(TRIGGER_RESPONSES.get(emotion, ["Emotions detected. Stay aware."]))
    cta_text, cta_link = random.choice(PSYCHOLOGICAL_CTAS.get(emotion, [("Stay grounded. More is coming.", "https://cash.app/$poplockitup")]))
    tts = gTTS(response_text)
    audio_filename = f"response_{emotion}.mp3"
    tts.save(audio_filename)

    return jsonify({
        "response": response_text,
        "response_audio_url": f"/audio/{audio_filename}",
        "psych_cta": cta_text,
        "cta_link": cta_link
    })

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_file(filename, mimetype='audio/mpeg')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
