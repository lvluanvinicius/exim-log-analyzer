import re
from datetime import datetime

class EximLogEntry:
    def __init__(self, log_datetime, message_id, direction, email, details, spam_score=None, auth_failure=False, frozen=False, ip=None):
        self.log_datetime = log_datetime
        self.message_id = message_id
        self.direction = direction
        self.email = email
        self.details = details
        self.spam_score = spam_score
        self.auth_failure = auth_failure
        self.frozen = frozen
        self.ip = ip

def parse_log_line(line):
    """
    Parse uma linha do log principal do Exim.
    Retorna:
        EximLogEntry ou None se a linha não corresponder ao formato esperado.
    """
    log_pattern = re.compile(
        r'(?P<date>\d{4}-\d{2}-\d{2})\s+'            # Data (YYYY-MM-DD)
        r'(?P<time>\d{2}:\d{2}:\d{2})\s+'            # Hora (HH:MM:SS)
        r'(?P<host>[\w.-]+)\s+'                      # Nome do host
        r'(?P<message_id>[A-F0-9-]+):\s+'            # ID da mensagem (alfanumérico, com possível hífen)
        r'(?P<direction><=|=>|==|<>)\s+'             # Direção da mensagem
        r'(?P<email>[\w\.-]+@[\w\.-]+)\s*'           # Email
        r'(?P<details>.*)'                           # Detalhes restantes (livres)
    )

    # Padrões adicionais para extrações específicas
    spam_score_pattern = re.compile(r'SpamAssassin.*score=(\d+\.\d+)')
    auth_failure_pattern = re.compile(r'dovecot_login authenticator failed for .* \[(.*)\]:\d+: 535 Incorrect authentication data')
    frozen_message_pattern = re.compile(r'Message is frozen')

    match = log_pattern.match(line)
    if match:
        date_str = match.group('date')
        time_str = match.group('time')
        message_id = match.group('message_id')
        direction = match.group('direction')
        email = match.group('email')
        details = match.group('details')

        datetime_str = f"{date_str} {time_str}"
        try:
            log_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None

        # Verificação de spam score
        spam_match = spam_score_pattern.search(details)
        spam_score = None
        if spam_match:
            spam_score = float(spam_match.group(1))

        # Verificação de falhas de autenticação
        auth_failure_match = auth_failure_pattern.search(details)
        auth_failure = False
        ip = None
        if auth_failure_match:
            auth_failure = True
            ip = auth_failure_match.group(1)

        # Verificação de mensagens congeladas
        frozen_match = frozen_message_pattern.search(details)
        frozen = frozen_match is not None

        return EximLogEntry(
            log_datetime=log_datetime,
            message_id=message_id,
            direction=direction,
            email=email,
            details=details,
            spam_score=spam_score,
            auth_failure=auth_failure,
            frozen=frozen,
            ip=ip
        )
    return None

def parse_log_file(file_path):
    """
    Analisa o arquivo de log principal do Exim.
    Args:
        file_path (str): Caminho para o arquivo exim_mainlog.
    Returns:
        List[EximLogEntry]: Lista de entradas de log analisadas.
    """
    entries = []
    with open(file_path, 'r') as f:
        for line in f:
            entry = parse_log_line(line)
            if entry:
                entries.append(entry)
            else:
                print(f"Linha não corresponde ao padrão: {line.strip()}")
    return entries
