# Internet Monitor (Debian + Firefox + Selenium)

Skrypt monitorujący jakość łącza internetowego poprzez pomiar czasu ładowania stron WWW, z wykorzystaniem przeglądarki Firefox w trybie headless.

## ✅ Funkcje

- Ładowanie wybranych stron z pełnym pobraniem zasobów (obrazki, skrypty, banery)
- Pomiar czasu pełnego ładowania (`document.readyState == complete`)
- Szczegółowe logowanie załadowanych zasobów (jeśli `debugVerbose=True`)
- Zapis wyników do pliku `log.csv` + `verbose_log.txt`
- Działa na serwerach bez środowiska graficznego (Xvfb)

---

## 🛠️ Wymagania systemowe

- Debian 11 / 12
- Python 3 + pip
- Firefox ESR
- `xvfb` (wirtualny X-server)
- `geckodriver` (sterownik dla Selenium)

---

## 📦 Instalacja

### 1. Zainstaluj wymagane pakiety:

```bash
sudo apt update
sudo apt install -y \
    python3 python3-pip \
    firefox-esr \
    xvfb \
    wget curl \
    libgtk-3-0 libdbus-glib-1-2 libxt6
