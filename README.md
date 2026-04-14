# SOC Projects Portfolio

A collection of cybersecurity projects built as part of my studies in cybersecurity. Each project covers practical skills used in a SOC.

---

## Projects

| # | Project | Category | Description |
|---|---------|----------|-------------|
| 01 | [Brute Force Detector](./01-brute-force-detector/) | Log Analysis | Reads SSH auth logs and flags IPs with too many failed logins |
| 02 | [SIEM Log Normalizer](./02-siem-log-normalizer/) | SIEM | Collects logs from multiple sources and shows them with severity levels |
| 03 | [Incident Response Playbook](./03-incident-response-playbook/) | Incident Response | Full 7-phase IR playbook with diagram and checklist tool |
| 04 | [URL Phishing Analyser](./04-url-analyser/) | Phishing Detection | Checks a URL for suspicious patterns like IP hosts, stacked subdomains, and phishing keywords |
| 05 | [Port Scanner](./05-port-scanner/) | Network Monitoring | Scans a host for open ports and shows what services are running |
| 06 | [Hash Identifier](./06-hash-identifier/) | Password Security | Identifies hash types and checks if they match known weak passwords |
| 07 | [DNS Lookup Tool](./07-dns-lookup/) | Threat Intel | Looks up DNS records for a domain and flags phishing keywords |
| 08 | [Auth Log Analyzer](./08-auth-log-analyzer/) | Log Analysis | Parses SSH auth logs to count failed logins, track successful ones, and flag brute force sources |
| 09 | [File Integrity Monitor](./09-file-integrity-monitor/) | Endpoint Security | Hashes every file in a directory and alerts when files are added, modified, or deleted |
| 10 | [IP Reputation Checker](./10-ip-reputation-checker/) | OSINT and Threat Intel | Checks IP addresses against a local threat database and assigns a risk score with category and country |
| 11 | [Email Header Parser](./11-email-header-parser/) | Phishing Detection | Parses raw email headers and checks for SPF, DKIM, DMARC failures and address mismatches |
| 12 | [IOC Extractor](./12-ioc-extractor/) | Threat Detection | Pulls IP addresses, domains, URLs, hashes, and emails out of raw text |
| 13 | [Firewall Log Analyzer](./13-firewall-log-analyzer/) | Log Analysis | Reads firewall logs to count blocked IPs, find targeted ports, and flag port scans and brute force attempts |
| 14 | [Password Strength Checker](./14-password-strength-checker/) | Password Security | Scores a password based on length, character variety, and patterns then gives clear feedback on how to improve it |
| 15 | [Alert Correlator](./15-alert-correlator/) | SIEM Concepts | Groups security alerts by source IP to classify severity and spot sources triggering multiple attack types |
| 16 | [Process Monitor](./16-process-monitor/) | Incident Response | Scans running processes and flags any that match known malicious tools |
| 17 | [Syslog Analyzer](./17-syslog-analyzer/) | Log Analysis | Reads system logs and flags suspicious events like SSH brute force, bad sudo commands, and root account creation |
| 18 | [Domain Info Lookup](./18-domain-info-lookup/) | OSINT and Threat Intel | Looks up DNS records and reverse DNS for a domain to help with SOC investigations |
| 19 | [SSL Certificate Checker](./19-ssl-certificate-checker/) | Network Monitoring | Checks SSL/TLS certificates for any domain and flags ones that are expiring soon or already expired |

---

##  License

MIT
