import socket
import urllib.request
from datetime import datetime
import os

os.makedirs("reports", exist_ok=True)

def save_report(title, result):
    filename = datetime.now().strftime("reports/report_%Y%m%d_%H%M%S.txt")
    with open(filename, "w") as f:
        f.write(title + "\n" + result)
    print("Report saved:", filename)

def domain_lookup():
    domain = input("Enter domain: ").strip()
    try:
        ip = socket.gethostbyname(domain)
        print("IP:", ip)
        save_report("Domain Lookup: " + domain, ip)
    except Exception as e:
        print("Error:", e)

def public_ip():
    try:
        ip = urllib.request.urlopen("https://api.ipify.org", timeout=10).read().decode()
        print("Public IP:", ip)
        save_report("Public IP", ip)
    except Exception as e:
        print("Error:", e)

def dns_lookup():
    domain = input("Enter domain: ").strip()
    try:
        results = socket.getaddrinfo(domain, None)
        addresses = sorted(set(x[4][0] for x in results))
        output = "\n".join(addresses)
        print(output)
        save_report("DNS Lookup: " + domain, output)
    except Exception as e:
        print("Error:", e)

def local_scan():
    ports = [22, 80, 443, 8080, 3000, 5000]
    opened = []
    for port in ports:
        sock = socket.socket()
        sock.settimeout(0.5)
        if sock.connect_ex(("127.0.0.1", port)) == 0:
            opened.append(str(port))
            print("Port", port, "OPEN")
        sock.close()
    result = "Open ports: " + (", ".join(opened) if opened else "None")
    save_report("Local Port Scan", result)


def ip_info():
    try:
        ip = urllib.request.urlopen(
            "https://api.ipify.org", timeout=10
        ).read().decode().strip()

        import json
        url = "https://ipwho.is/" + ip
        data = json.loads(
            urllib.request.urlopen(url, timeout=10).read().decode()
        )

        if not data.get("success"):
            print("IP information unavailable")
            return

        result = (
            "IP: " + str(data.get("ip")) + "\\n"
            + "Country: " + str(data.get("country")) + "\\n"
            + "City: " + str(data.get("city")) + "\\n"
            + "Region: " + str(data.get("region")) + "\\n"
            + "ISP: " + str(data.get("connection", {}).get("isp"))
        )
        print(result)
        save_report("My Public IP Information", result)

    except Exception as e:
        print("Error:", e)

def menu():
    while True:
        print("\n=============================")
        print("      SONIC 962 CYBER")
        print("=============================")
        print("[1] Domain IP Lookup")
        print("[2] Public IP")
        print("[3] DNS Lookup")
        print("[4] Local Port Scanner")
        print("[5] Public IP Information")
        print("[6] Exit")
        print("=============================")
        choice = input("SONIC > ").strip()
        if choice == "1":
            domain_lookup()
        elif choice == "2":
            public_ip()
        elif choice == "3":
            dns_lookup()
        elif choice == "4":
            local_scan()
        elif choice == "5":
            ip_info()
        elif choice == "6":
            print("SONIC 962 CYBER CLOSED")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    menu()
