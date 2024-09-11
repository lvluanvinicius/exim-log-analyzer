import matplotlib.pyplot as plt

def report_auth_failures(failures):
    print("=== Falhas de Autenticação ===")
    for entry in failures:
        print(f"[{entry.datetime}] ID: {entry.message_id} - {entry.email} - Detalhes: {entry.details}")
    print(f"Total de falhas de autenticação: {len(failures)}\n")

def report_connection_refusals(refusal_counter, threshold=10):
    print("=== Conexões Recusadas ===")
    for ip, count in refusal_counter.most_common():
        if count >= threshold:
            print(f"IP: {ip} - Recusou {count} conexões")
    print()

def report_bounces_deferred(bounces, deferred):
    print("=== Mensagens de Bounce e Deferred ===")
    print(f"Total de mensagens de bounce (sem remetente): {bounces}")
    print(f"Total de mensagens deferred: {deferred}\n")

def report_tls_usage(tls_enabled, tls_disabled):
    print("=== Uso de TLS ===")
    print(f"Mensagens com TLS: {tls_enabled}")
    print(f"Mensagens sem TLS: {tls_disabled}\n")

def report_spam_patterns(sender_counter, threshold=100):
    print("=== Padrões de Spam ===")
    for sender, count in sender_counter.most_common():
        if count >= threshold:
            print(f"Remetente: {sender} - Enviou {count} mensagens")
    print()

def report_frozen_messages(frozen_messages):
    print("=== Mensagens Congeladas ===")
    for entry in frozen_messages:
        print(f"[{entry.datetime}] ID: {entry.message_id} - {entry.email} - Detalhes: {entry.details}")
    print(f"Total de mensagens congeladas: {len(frozen_messages)}\n")

def report_spam_scores(high_spam_scores, spam_threshold=5.0):
    print(f"=== Mensagens com Pontuação de Spam Acima de {spam_threshold} ===")
    for entry in high_spam_scores:
        print(f"[{entry.datetime}] ID: {entry.message_id} - {entry.email} - Pontuação de Spam: {entry.details}")
    print(f"Total de mensagens com pontuação de spam alta: {len(high_spam_scores)}\n")

def report_ip_analysis(ip_counter, threshold=5):
    print("=== IPs Relacionados a Falhas de Autenticação e Mensagens Congeladas ===")
    for ip, count in ip_counter.items():
        if count >= threshold:
            print(f"IP: {ip} - Apareceu em {count} logs")
    print()

def report_ip_send_count(ip_send_counter, threshold=1000):
    print("=== Contagem de Envios por IP ===")
    for ip, count in ip_send_counter.items():
        if count >= threshold:
            print(f"IP: {ip} - Envios: {count}")
    print(f"Total de IPs com mais de {threshold} envios: {len(ip_send_counter)}\n")

def plot_connection_refusals(refusal_counter, top_n=10):
    top_refusals = refusal_counter.most_common(top_n)
    if not top_refusals:
        print("Nenhuma conexão recusada para plotar.\n")
        return
    ips, counts = zip(*top_refusals)
    
    plt.figure(figsize=(10, 6))
    plt.bar(ips, counts, color='red')
    plt.xlabel('Endereço IP')
    plt.ylabel('Número de Conexões Recusadas')
    plt.title('Top 10 IPs com Mais Conexões Recusadas')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('connection_refusals.png')
    plt.close()
    print("Gráfico de conexões recusadas salvo como 'connection_refusals.png'\n")

def plot_spam_senders(sender_counter, top_n=10):
    top_senders = sender_counter.most_common(top_n)
    if not top_senders:
        print("Nenhum remetente de spam para plotar.\n")
        return
    senders, counts = zip(*top_senders)
    
    plt.figure(figsize=(10, 6))
    plt.bar(senders, counts, color='blue')
    plt.xlabel('Remetente')
    plt.ylabel('Número de Emails Enviados')
    plt.title('Top 10 Remetentes com Maior Envio de Emails')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('spam_senders.png')
    plt.close()
    print("Gráfico de remetentes de spam salvo como 'spam_senders.png'\n")

def plot_frozen_messages(frozen_messages):
    """
    Gera um gráfico de barras com o número de mensagens congeladas por hora.
    """
    if not frozen_messages:
        print("Nenhuma mensagem congelada para plotar.\n")
        return

    frozen_by_hour = {}
    for entry in frozen_messages:
        hour = entry.datetime.strftime("%Y-%m-%d %H:00")
        frozen_by_hour[hour] = frozen_by_hour.get(hour, 0) + 1

    hours = list(frozen_by_hour.keys())
    counts = list(frozen_by_hour.values())

    plt.figure(figsize=(10, 6))
    plt.bar(hours, counts, color='purple')
    plt.xlabel('Hora')
    plt.ylabel('Mensagens Congeladas')
    plt.title('Mensagens Congeladas por Hora')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('frozen_messages.png')
    plt.close()
    print("Gráfico de mensagens congeladas salvo como 'frozen_messages.png'\n")
