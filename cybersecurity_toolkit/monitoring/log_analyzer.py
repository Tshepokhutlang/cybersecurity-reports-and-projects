import re
from collections import defaultdict
from datetime import datetime

class LogAnalyzer:

    def __init__(self, log_file):
        self.log_file = log_file
        self.failed_logins = 0
        self.success_logins = 0
        self.ip_attempts = defaultdict(int)
        self.suspicious_ips = []

    def analyze_logs(self):

        print("Starting log analysis...\n")

        with open(self.log_file, "r") as file:

            for line in file:

                if "LOGIN FAILED" in line:
                    self.failed_logins += 1

                    ip = self.extract_ip(line)

                    if ip:
                        self.ip_attempts[ip] += 1

                elif "LOGIN SUCCESS" in line:
                    self.success_logins += 1

        self.detect_brute_force()

        self.print_summary()

        self.save_report()

    def extract_ip(self, line):

        match = re.search(r'ip=(\d+\.\d+\.\d+\.\d+)', line)

        if match:
            return match.group(1)

        return None

    def detect_brute_force(self):

        for ip, attempts in self.ip_attempts.items():

            if attempts >= 3:
                self.suspicious_ips.append(ip)

    def print_summary(self):

        print("Log Analysis Summary")
        print("--------------------")

        print("Failed Logins:", self.failed_logins)
        print("Successful Logins:", self.success_logins)

        print("\nSuspicious IP Addresses:")

        if self.suspicious_ips:

            for ip in self.suspicious_ips:
                print("-", ip)

        else:
            print("None detected")

    def save_report(self):

        with open("reports/report.txt", "w") as report:

            report.write("SECURITY LOG REPORT\n")
            report.write(str(datetime.now()) + "\n")
            report.write("-------------------\n")

            report.write(
                f"Failed Logins: {self.failed_logins}\n"
            )

            report.write(
                f"Successful Logins: {self.success_logins}\n"
            )
            

            report.write("\nSuspicious IPs:\n")

            if self.suspicious_ips:

                for ip in self.suspicious_ips:
                    report.write(f"{ip}\n")

            else:
                report.write("None\n")


if __name__ == "__main__":

    analyzer = LogAnalyzer("logs/security.log")

    analyzer.analyze_logs()