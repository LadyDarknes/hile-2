import psutil
import requests
import time
from googlesearch import search
import subprocess
import platform

def get_hwid():
    try:
        return subprocess.check_output('wmic csproduct get uuid', shell=True).decode().split('\n')[1].strip()
    except Exception:
        return "HWID alınamadı"

def get_windows_version():
    return platform.system() + " " + platform.version()

def get_cpu_info():
    try:
        return subprocess.check_output("wmic cpu get name", shell=True).decode().split('\n')[1].strip()
    except Exception:
        return "İşlemci bilgisi alınamadı"

def get_ram_info():
    return f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB RAM"

def is_defender_enabled():
    try:
        result = subprocess.check_output('powershell -Command "Get-MpComputerStatus | Select-Object -ExpandProperty AntivirusEnabled"', shell=True).decode().strip()
        return result.lower() == 'true'
    except Exception:
        return False

WEBHOOK_URL = input("Lütfen Discord Webhook URL'sini girin: ")

# Güvenlik listeleri
guvenli_kelimeler = ["safe", "trusted", "official", "microsoft service", "legit", "verified"]
tehlikeli_kelimeler = ["trojan", "malware", "backdoor", "spyware", "virus", "keylogger", "ransomware", "worm", "exploit"]
guvenilir_kaynaklar = ["microsoft.com", "windows.com", "docs.microsoft.com", "support.microsoft.com", "technopat.net"]
beyaz_liste = ["wuauserv", "bits", "EventLog", "plugplay", "CryptSvc", "Spooler", "WinDefend", "battlenet_helpersvc", ""]
kara_liste = ["irfanview", "Rundll32", "Csrss"]

def get_services():
    """Çalışan Windows servislerini alır."""
    try:
        return [
            {
                "name": s.name(), 
                "display_name": s.display_name() or "Bilinmiyor", 
                "status": s.status(),
                "start_type": s.start_type(),
                "pid": s.pid() if s.status() == "running" else "N/A",
                "uptime": time.strftime('%H:%M:%S', time.gmtime(time.time() - psutil.Process(s.pid()).create_time())) if s.status() == "running" else "N/A"
            }
            for s in psutil.win_service_iter()
        ]
    except Exception as e:
        print(f"Hizmetleri alırken hata oluştu: {e}")
        return []

def google_search(query, num_results=5):
    """Google üzerinden arama yapar."""
    try:
        return [result for result in search(query, num_results=num_results)]
    except Exception as e:
        print(f"Google arama hatası: {e}")
        return []

def calculate_threat_score(service_name, display_name):
    """Servis tehdit puanını hesaplar."""
    threat_score = 0

    if service_name.lower() in (s.lower() for s in beyaz_liste):
        return 0  # Beyaz listede, kesin güvenli

    if service_name.lower() in (s.lower() for s in kara_liste):
        return 100  # Kara listede, kesin tehlikeli

    if not display_name:
        threat_score += 30  # Açıklaması yoksa şüpheli

    try:
        search_results = google_search(f"{service_name} Windows service", 5)
        results_text = " ".join(search_results).lower()

        if any(domain in results_text for domain in guvenilir_kaynaklar):
            return 0  # Microsoft kaynaklarında geçiyorsa güvenli

        if any(word in results_text for word in tehlikeli_kelimeler):
            threat_score += 50  # Tehlikeli kelime içeriyorsa risk artar

        if any(word in results_text for word in guvenli_kelimeler):
            threat_score -= 20  # Güvenli kelime içeriyorsa risk düşer
    except Exception as e:
        print(f"Arama hatası: {e}")

    return max(0, min(100, threat_score))  # 0 ile 100 arasında sınırla

def send_to_webhook(services_chunk, first_message=False):
    """Servis bilgilerini Discord'a gönderir."""
    try:
        embeds = []
        for service in services_chunk:
            threat_score = calculate_threat_score(service["name"], service["display_name"])
            threat_status = "✅ **Güvenli**" if threat_score == 0 else ("⚠️ **Orta Risk**" if threat_score < 50 else "🚨 **Tehlikeli!**")
            color = 0x00FF00 if threat_score == 0 else (0xFFFF00 if threat_score < 50 else 0xFF0000)

            embed = {
                "title": f"🔍 Servis İncelemesi: {service['name']}",
                "description": f"**📌 Durum:** {service['status']}\n"
                               f"**📝 Açıklama:** {service['display_name']}\n"
                               f"**🚀 Başlangıç Türü:** {service['start_type']}\n"
                               f"**💻 PID:** {service['pid']}\n"
                               f"**⏳ Çalışma Süresi:** {service['uptime']}\n"
                               f"**🛡️ Tehdit Puanı:** `{threat_score}/100`\n"
                               f"**⚠️ Güvenlik Durumu:** {threat_status}",
                "color": color
            }
            embeds.append(embed)

        if first_message:
            system_info = {
                "title": "🖥️ **Sistem Bilgileri**",
                "description": f"**💻 HWID:** `{get_hwid()}`\n"
                               f"**🖥️ Windows Sürümü:** `{get_windows_version()}`\n"
                               f"**⚡ İşlemci:** `{get_cpu_info()}`\n"
                               f"**💾 RAM:** `{get_ram_info()}`\n"
                               f"**🛡️ Defender Durumu:** {'🟢 Açık' if is_defender_enabled() else '🔴 Kapalı (Açmanız Önerilir!)'}",
                "color": 0x3498DB
            }
            embeds.append(system_info)

        data = {"embeds": embeds[:10]}  # Discord 10 embed sınırı var
        response = requests.post(WEBHOOK_URL, json=data)

        if response.status_code in [200, 204]:
            print(f"{len(services_chunk)} hizmet başarıyla gönderildi.")
        else:
            print(f"Hizmetler gönderilemedi. Hata: {response.status_code}")
    except Exception as e:
        print(f"Webhook gönderim hatası: {e}")

def main():
    services = get_services()
    chunk_size = 5  # 5'erli gruplar halinde gönder
    first_message = True

    for i in range(0, len(services), chunk_size):
        send_to_webhook(services[i:i + chunk_size], first_message)
        first_message = False
        time.sleep(5)  # Spam koruması için bekleme süresi

if __name__ == "__main__":
    main()
