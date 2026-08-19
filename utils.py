from config import CERT_PREFIX

def generate_cert_id(num):
    return f"TRIVARNA-2026-{str(num).zfill(4)}"