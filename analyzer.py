from collections import Counter
from datetime import datetime
import re

def analyze_auth_failures(entries):
    auth_failures = []
    failure_pattern = re.compile(r'authentication failure', re.IGNORECASE)
    for entry in entries:
        if entry.direction == '<=' and failure_pattern.search(entry.details):
            auth_failures.append(entry)
    return auth_failures

def analyze_connection_refusals(entries):
    refusal_pattern = re.compile(r'refused', re.IGNORECASE)
    refusals = []
    ip_counter = Counter()
    for entry in entries:
        if refusal_pattern.search(entry.details):
            refusals.append(entry)
            ip_match = re.search(r'\[(\d{1,3}(?:\.\d{1,3}){3})\]', entry.details)
            if ip_match:
                ip = ip_match.group(1)
                ip_counter[ip] += 1
    return ip_counter

def analyze_bounces_deferred(entries):
    bounces = [e for e in entries if e.direction == '<>']
    deferred = [e for e in entries if 'deferred' in e.details.lower()]
    return len(bounces), len(deferred)

def analyze_tls_usage(entries):
    tls_enabled = 0
    tls_disabled = 0
    for entry in entries:
        if 'X=TLS' in entry.details:
            tls_enabled += 1
        else:
            tls_disabled += 1
    return tls_enabled, tls_disabled

def analyze_spam_patterns(entries):
    sent_emails = [e for e in entries if e.direction == '=>']
    sender_counter = Counter()
    for entry in sent_emails:
        sender = entry.email
        sender_counter[sender] += 1
    return sender_counter

def analyze_frozen_messages(entries):
    frozen_messages = [e for e in entries if 'frozen' in e.details.lower()]
    return frozen_messages

def analyze_spam_scores(entries):
    high_spam_scores = []
    spam_pattern = re.compile(r'SpamAssassin.*score=(\d+\.\d+)')
    for entry in entries:
        match = spam_pattern.search(entry.details)
        if match:
            spam_score = float(match.group(1))
            if spam_score > 5.0:
                high_spam_scores.append(entry)
    return high_spam_scores

def analyze_ip_patterns(entries):
    ip_counter = Counter()
    failure_pattern = re.compile(r'(refused|failed|frozen)', re.IGNORECASE)
    for entry in entries:
        if failure_pattern.search(entry.details):
            ip_match = re.search(r'\[(\d{1,3}(?:\.\d{1,3}){3})\]', entry.details)
            if ip_match:
                ip = ip_match.group(1)
                ip_counter[ip] += 1
    return ip_counter

def analyze_ip_send_count(entries, start_date=None, end_date=None, min_sends=1000):
    ip_counter = Counter()
    ip_pattern = re.compile(r'\[(\d{1,3}(?:\.\d{1,3}){3})\]')
    for entry in entries:
        if entry.direction == '=>' and 'smtp' in entry.details:
            if start_date and entry.log_datetime < start_date:
                continue
            if end_date and entry.log_datetime > end_date:
                continue
            ip_match = ip_pattern.search(entry.details)
            if ip_match:
                ip = ip_match.group(1)
                ip_counter[ip] += 1
    return {ip: count for ip, count in ip_counter.items() if count >= min_sends}
