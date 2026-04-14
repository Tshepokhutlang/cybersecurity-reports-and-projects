# ==============================================
# SIMPLE SIEM-STYLE SYSTEM (Educational / Defensive)
# ==============================================
# This is a modular Security Information and Event Management (SIEM)
# system skeleton suitable for cybersecurity labs, monitoring, and
# small business security services.
#
# Features:
# - Log Collection
# - Event Parsing
# - Correlation Engine (threat detection)
# - Alert Manager
# - Report Generation
# - Continuous Monitoring Loop
#
# Safe for defensive cybersecurity, SOC labs, and IT security services.
# ==============================================

import time
import re
import json
from datetime import datetime
from collections import defaultdict


# ==============================================
# CONFIGURATION
# ==============================================

CONFIG = {
    "log_file": "logs/security.log",
    "alert_threshold": 5,
    "monitor_interval": 5,
    "report_file": "reports/siem_report.json"
}


# ==============================================
# LOG COLLECTOR
# ==============================================

class LogCollector:

    def __init__(self, log_file):
        self.log_file = log_file
        self.last_position = 0

    def collect_new_logs(self):

        logs = []

        try:
            with open(self.log_file, "r") as file:

                file.seek(self.last_position)

                new_lines = file.readlines()

                self.last_position = file.tell()

                logs.extend(new_lines)

        except FileNotFoundError:
            print("Log file not found.")

        return logs


# ==============================================
# EVENT PARSER
# ==============================================

class EventParser:

    def parse(self, log_line):

        event = {
            "timestamp": None,
            "status": None,
            "user": None,
            "ip": None
        }

        try:
            parts = log_line.strip().split()

            event["timestamp"] = parts[0] + " " + parts[1]

            if "FAILED" in log_line:
                event["status"] = "FAILED"

            if "SUCCESS" in log_line:
                event["status"] = "SUCCESS"

            user_match = re.search(r'user=(\\w+)', log_line)
            ip_match = re.search(r'ip=(\\d+\\.\\d+\\.\\d+\\.\\d+)', log_line)

            if user_match:
                event["user"] = user_match.group(1)

            if ip_match:
                event["ip"] = ip_match.group(1)

        except Exception:
            pass

        return event


# ==============================================
# CORRELATION ENGINE (THREAT DETECTION)
# ==============================================

class CorrelationEngine:

    def __init__(self, threshold):
        self.threshold = threshold
        self.failed_attempts = defaultdict(int)
        self.suspicious_ips = set()

    def analyze(self, event):

        if event["status"] == "FAILED" and event["ip"]:

            ip = event["ip"]

            self.failed_attempts[ip] += 1

            if self.failed_attempts[ip] >= self.threshold:

                self.suspicious_ips.add(ip)

                return {
                    "type": "BRUTE_FORCE",
                    "ip": ip,
                    "attempts": self.failed_attempts[ip]
                }

        return None


# ==============================================
# ALERT MANAGER
# ==============================================

class AlertManager:

    def __init__(self):
        self.alerts = []

    def send_alert(self, alert):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        alert_record = {
            "timestamp": timestamp,
            "alert": alert
        }

        self.alerts.append(alert_record)

        print("ALERT DETECTED")
        print("Type:", alert["type"])
        print("IP:", alert["ip"])
        print("Attempts:", alert["attempts"])
        print()


# ==============================================
# REPORT GENERATOR
# ==============================================

class ReportGenerator:

    def __init__(self, report_file):
        self.report_file = report_file

    def generate(self, alerts):

        report = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_alerts": len(alerts),
            "alerts": alerts
        }

        with open(self.report_file, "w") as file:
            json.dump(report, file, indent=4)

        print("Report generated:", self.report_file)


# ==============================================
# SIEM ENGINE
# ==============================================

class SIEMSystem:

    def __init__(self):

        self.collector = LogCollector(CONFIG["log_file"])
        self.parser = EventParser()
        self.engine = CorrelationEngine(CONFIG["alert_threshold"])
        self.alert_manager = AlertManager()
        self.reporter = ReportGenerator(CONFIG["report_file"])

    def process_logs(self):

        logs = self.collector.collect_new_logs()

        for log_line in logs:

            event = self.parser.parse(log_line)

            alert = self.engine.analyze(event)

            if alert:
                self.alert_manager.send_alert(alert)

    def run(self):

        print("Starting SIEM Monitoring...")
        print("Press CTRL+C to stop.\n")

        try:

            while True:

                self.process_logs()

                time.sleep(CONFIG["monitor_interval"])

        except KeyboardInterrupt:

            print("Stopping SIEM system...")

            self.reporter.generate(
                self.alert_manager.alerts
            )


# ==============================================
# MAIN ENTRY
# ==============================================

if __name__ == "__main__":

    siem = SIEMSystem()

    siem.run()

# ==============================================
# WEB DASHBOARD (Flask)
# ==============================================
# This lightweight dashboard displays alerts in a browser.
# Install dependency first:
# pip install flask
#
# Run separately:
# python dashboard.py
# Then open:
# http://127.0.0.1:5000
# ==============================================

from flask import Flask, render_template_string, jsonify
import json
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>SIEM Security Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #111;
            color: #fff;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #00ff99;
        }
        .card {
            background: #1e1e1e;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
        }
        .alert {
            color: red;
            font-weight: bold;
        }
    </style>
</head>
<body>

<h1>SIEM Security Dashboard</h1>

<div id="alerts"></div>

<script>

async function loadAlerts() {

    const response = await fetch('/api/alerts');

    const data = await response.json();

    const container = document.getElementById('alerts');

    container.innerHTML = '';

    if (data.alerts.length === 0) {
        container.innerHTML = '<div class="card">No alerts detected</div>';
        return;
    }

    data.alerts.forEach(alert => {

        const div = document.createElement('div');

        div.className = 'card';

        div.innerHTML = `
            <div class="alert">Threat Detected</div>
            <p><strong>Time:</strong> ${alert.timestamp}</p>
            <p><strong>Type:</strong> ${alert.alert.type}</p>
            <p><strong>IP:</strong> ${alert.alert.ip}</p>
            <p><strong>Attempts:</strong> ${alert.alert.attempts}</p>
        `;

        container.appendChild(div);

    });

}

setInterval(loadAlerts, 3000);

loadAlerts();

</script>

</body>
</html>
"""


@app.route('/')
def dashboard():

    return render_template_string(HTML_TEMPLATE)


@app.route('/api/alerts')
def get_alerts():

    report_file = CONFIG["report_file"]

    if not os.path.exists(report_file):
        return jsonify({"alerts": []})

    with open(report_file, 'r') as file:

        data = json.load(file)

    return jsonify(data)


if __name__ == '__main__':

    print("Starting SIEM Web Dashboard...")

    app.run(debug=True)

