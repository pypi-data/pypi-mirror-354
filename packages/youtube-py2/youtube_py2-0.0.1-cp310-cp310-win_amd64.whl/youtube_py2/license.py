import os

def require_device_cert():
    cert_path = os.environ.get("DEVICE_CERT_PATH", "device_cert.pem")
    if not os.path.exists(cert_path):
        raise Exception("端末証明書(device_cert.pem)がありません。この機能は利用できません。")
