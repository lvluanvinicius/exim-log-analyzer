import argparse
from parser import parse_log_file

from analyzer import (
    analyze_auth_failures,
    analyze_connection_refusals,
    analyze_bounces_deferred,
    analyze_tls_usage,
    analyze_spam_patterns,
    analyze_frozen_messages,
    analyze_spam_scores,
    analyze_ip_patterns,
    analyze_ip_send_count
)
from reporter import (
    report_auth_failures,
    report_connection_refusals,
    report_bounces_deferred,
    report_tls_usage,
    report_spam_patterns,
    report_frozen_messages,
    report_spam_scores,
    report_ip_analysis,
    report_ip_send_count,
    plot_connection_refusals,
    plot_spam_senders,
    plot_frozen_messages
)
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Analisador de Logs do Exim com Foco em Segurança")
    parser.add_argument('logfile', help='Caminho para o arquivo exim_mainlog')
    parser.add_argument('--auth-failures', action='store_true', help='Relatar falhas de autenticação')
    parser.add_argument('--connection-refusals', action='store_true', help='Relatar conexões recusadas')
    parser.add_argument('--bounces-deferred', action='store_true', help='Relatar bounces e deferred')
    parser.add_argument('--tls-usage', action='store_true', help='Relatar uso de TLS')
    parser.add_argument('--spam-patterns', action='store_true', help='Relatar padrões de spam')
    parser.add_argument('--frozen-messages', action='store_true', help='Relatar mensagens congeladas')
    parser.add_argument('--spam-scores', action='store_true', help='Relatar pontuações de spam')
    parser.add_argument('--ip-analysis', action='store_true', help='Relatar IPs associados a falhas e mensagens congeladas')
    parser.add_argument('--ip-send-count', action='store_true', help='Relatar contagem de envios por IP')
    parser.add_argument('--start-date', help='Data de início (formato YYYY-MM-DD)', type=str)
    parser.add_argument('--end-date', help='Data de fim (formato YYYY-MM-DD)', type=str)
    parser.add_argument('--min-sends', type=int, default=1000, help='Mínimo de envios por IP para o relatório (padrão: 1000)')
    parser.add_argument('--threshold', type=int, default=10, help='Limite para relatórios de conexões recusadas, spam e IPs (default: 10 para recusadas, 100 para spam)')

    args = parser.parse_args()

    # Parse dates
    start_date = datetime.strptime(args.start_date, "%Y-%m-%d") if args.start_date else None
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d") if args.end_date else None

    print("Lendo o arquivo de log...")
    entries = parse_log_file(args.logfile)
    print(entries)
    print(f"Total de entradas parseadas: {len(entries)}\n")

    if args.auth_failures:
        print("Analisando falhas de autenticação...")
        auth_failures = analyze_auth_failures(entries)
        report_auth_failures(auth_failures)

    if args.connection_refusals:
        print("Analisando conexões recusadas...")
        refusal_counter = analyze_connection_refusals(entries)
        report_connection_refusals(refusal_counter, threshold=args.threshold)
        plot_connection_refusals(refusal_counter)

    if args.bounces_deferred:
        print("Analisando mensagens de bounce e deferred...")
        bounces, deferred = analyze_bounces_deferred(entries)
        report_bounces_deferred(bounces, deferred)

    if args.tls_usage:
        print("Analisando uso de TLS...")
        tls_enabled, tls_disabled = analyze_tls_usage(entries)
        report_tls_usage(tls_enabled, tls_disabled)

    if args.spam_patterns:
        print("Analisando padrões de spam...")
        spam_counter = analyze_spam_patterns(entries)
        report_spam_patterns(spam_counter, threshold=100)  # Padrão de 100 para spam
        plot_spam_senders(spam_counter)

    if args.frozen_messages:
        print("Analisando mensagens congeladas...")
        frozen_messages = analyze_frozen_messages(entries)
        report_frozen_messages(frozen_messages)
        plot_frozen_messages(frozen_messages)

    if args.spam_scores:
        print("Analisando pontuações de spam...")
        high_spam_scores = analyze_spam_scores(entries)
        report_spam_scores(high_spam_scores, spam_threshold=5.0)

    if args.ip_analysis:
        print("Analisando padrões de IP relacionados a falhas e mensagens congeladas...")
        ip_counter = analyze_ip_patterns(entries)
        report_ip_analysis(ip_counter, threshold=args.threshold)

    if args.ip_send_count:
        print("Analisando contagem de envios por IP...")
        ip_send_counter = analyze_ip_send_count(entries, start_date=start_date, end_date=end_date, min_sends=args.min_sends)
        report_ip_send_count(ip_send_counter, threshold=args.min_sends)

    print("Análise concluída.")

if __name__ == "__main__":
    main()
