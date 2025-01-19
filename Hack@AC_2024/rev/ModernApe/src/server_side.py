from flask import Flask, jsonify
import datetime
import hashlib
import cmath

app = Flask(__name__)

def generate_dynamic_key():
    complex_key_part = complex_key()
    vector_key_part = vector_key()
    
    key = str(complex_key_part) + vector_key_part
    return key

def complex_key():
    current_time = datetime.datetime.utcnow()
    seconds = current_time.second
    real_part = seconds * (cmath.cos(seconds) + cmath.sin(seconds))
    imaginary_part = cmath.sin(seconds) + cmath.cos(seconds)
    key = real_part + imaginary_part
    return key

def vector_key():
    current_time = datetime.datetime.utcnow()
    time_hash = hashlib.sha256(str(current_time).encode()).hexdigest()
    return time_hash

def encrypt_flag(flag, key):
    encrypted_flag = ''.join(chr(ord(f) ^ ord(k)) for f, k in zip(flag, key))
    return encrypted_flag

@app.route('/')
def welcome_page():
    current_time = datetime.datetime.utcnow()
    key = generate_dynamic_key()
    encrypted_flag = encrypt_flag("ACSI{b33p_b33p_b5n5n5!}", key)
    
    response_data = {
        'message': "Welcome to the city of ModernApe. We have gone digital. You aren't getting past this time.",
        'time_stamp': current_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
        'secret': encrypted_flag
    }

    return jsonify(response_data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8040)
