
import socket
import urllib.request
import json
import os
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

os.makedirs("reports", exist_ok=True)

def save_report(title, result):
    filename = datetime.now().strftime(
        "reports/report_%Y%m%d_%H%M%S.txt"
    )
    with open(filename, "w") as f:
        f.write(title + "\n" + result)

class SonicApp(App):
    def build(self):
        self.title = "SONIC 962 CYBER"

        layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        title = Label(
            text="[b]SONIC 962 CYBER[/b]",
            markup=True,
            font_size=25,
            size_hint_y=None,
            height=60
        )
        layout.add_widget(title)

        self.domain = TextInput(
            hint_text="Enter domain (example.com)",
            size_hint_y=None,
            height=50,
            multiline=False
        )
        layout.add_widget(self.domain)

        self.output = TextInput(
            text="Welcome to SONIC 962 CYBER",
            readonly=True
        )
        layout.add_widget(self.output)

        buttons = [
            ("Domain IP Lookup", self.domain_lookup),
            ("Public IP", self.public_ip),
            ("DNS Lookup", self.dns_lookup),
            ("Local Port Scanner", self.local_scan),
            ("Public IP Information", self.ip_info),
        ]

        for name, action in buttons:
            btn = Button(text=name, size_hint_y=None, height=50)
            btn.bind(on_press=action)
            layout.add_widget(btn)

        return layout

    def show_result(self, title, result):
        self.output.text = title + "\n\n" + result
        save_report(title, result)

    def domain_lookup(self, instance):
        domain = self.domain.text.strip()
        try:
            ip = socket.gethostbyname(domain)
            self.show_result("Domain IP Lookup", ip)
        except Exception as e:
            self.output.text = "Error: " + str(e)

    def public_ip(self, instance):
        try:
            ip = urllib.request.urlopen(
                "https://api.ipify.org", timeout=10
            ).read().decode()
            self.show_result("Public IP", ip)
        except Exception as e:
            self.output.text = "Error: " + str(e)

    def dns_lookup(self, instance):
        domain = self.domain.text.strip()
        try:
            results = socket.getaddrinfo(domain, None)
            addresses = sorted(set(x[4][0] for x in results))
            self.show_result("DNS Lookup", "\n".join(addresses))
        except Exception as e:
            self.output.text = "Error: " + str(e)

    def local_scan(self, instance):
        ports = [22, 80, 443, 8080, 3000, 5000]
        opened = []

        for port in ports:
            sock = socket.socket()
            sock.settimeout(0.5)
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                opened.append(str(port))
            sock.close()

        result = "Open ports: " + (
            ", ".join(opened) if opened else "None"
        )
        self.show_result("Local Port Scan", result)

    def ip_info(self, instance):
        try:
            ip = urllib.request.urlopen(
                "https://api.ipify.org", timeout=10
            ).read().decode().strip()

            url = "https://ipwho.is/" + ip
            data = json.loads(
                urllib.request.urlopen(url, timeout=10).read().decode()
            )

            if not data.get("success"):
                self.output.text = "IP information unavailable"
                return

            result = (
                "IP: " + str(data.get("ip")) + "\n"
                + "Country: " + str(data.get("country")) + "\n"
                + "City: " + str(data.get("city")) + "\n"
                + "Region: " + str(data.get("region")) + "\n"
                + "ISP: " + str(data.get("connection", {}).get("isp"))
            )
            self.show_result("Public IP Information", result)

        except Exception as e:
            self.output.text = "Error: " + str(e)

SonicApp().run()
