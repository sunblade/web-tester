import time
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait

# === KONFIGURACJA ===
URLS = [
    "https://1.1.1.1",
    "https://www.aol.com",
    "https://www.onet.pl",
    "https://www.gazeta.pl",
    "https://www.mobile.de",
    "https://www.cisco.com",
    "https://www.allegro.pl",
    "https://www.wp.pl"
]

LOG_FILE = "log.csv"
VERBOSE_LOG_FILE = "verbose_log.txt"
debugVerbose = True

# === PRZYGOTUJ PRZEGLĄDARKĘ FIREFOX ===
def setup_browser():
    options = Options()
    options.headless = True

    # Ustaw preferencje wewnątrz Options
    options.set_preference("network.dns.disableIPv6", True)
    options.set_preference("javascript.options.asyncstack", False)

    service = Service(executable_path="/usr/local/bin/geckodriver")
    driver = webdriver.Firefox(service=service, options=options)
    return driver
# === POMIAR ŁADOWANIA STRONY ===
def measure_page_load(driver, url, debugVerbose=False):
    print(f"Rozpoczynam ładowanie: {url}")
    start_time = time.time()
    try:
        driver.set_page_load_timeout(10)
        driver.get(url)

        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print(f"document.readyState == complete dla {url}")

        verbose_output = []
        if debugVerbose:
            resources = driver.execute_script("""
                return performance.getEntriesByType("resource").map(r => ({
                    name: r.name,
                    type: r.initiatorType,
                    duration: r.duration.toFixed(2)
                }));
            """)
            print(f"Załadowane zasoby ({len(resources)}):")
            verbose_output.append(f"--- {url} ---")
            for res in resources:
                line = f"[{res['type']}] {res['name']} ({res['duration']} ms)"
                print(f" - {line}")
                verbose_output.append(line)
            verbose_output.append("")

            with open(VERBOSE_LOG_FILE, "a", encoding="utf-8") as f:
                f.write("\n".join(verbose_output) + "\n")

        time.sleep(2)
        load_time = time.time() - start_time
        print(f"{url} załadowano w {load_time:.2f} sekundy\n")
        return round(load_time, 2), None

    except Exception as e:
        print(f"Błąd ładowania {url}: {e}\n")
        return None, str(e)

# === LOG DO CSV ===
def log_to_csv(timestamp, url, load_time, error):
    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, url, load_time if load_time is not None else "", error if error else ""])

def main():
    print("Uruchamiam monitor z Firefoxem...")

    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "url", "load_time_sec", "error"])

    if debugVerbose:
        with open(VERBOSE_LOG_FILE, mode="a", encoding="utf-8") as f:
            f.write("=== Verbose zasoby stron (Firefox) ===\n\n")

    while True:
        driver = setup_browser()
        try:
            for url in URLS:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                load_time, error = measure_page_load(driver, url, debugVerbose)
                log_to_csv(timestamp, url, load_time, error)
        finally:
            driver.quit()
        time.sleep(30)

if __name__ == "__main__":
    main()s
