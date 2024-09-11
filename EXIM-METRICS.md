# Análise de Logs do Exim - `exim_mainlog`

Este documento fornece uma visão geral sobre a análise do log principal do Exim, o `exim_mainlog`. O Exim é um Mail Transfer Agent (MTA) amplamente utilizado para gerenciar o envio e recebimento de e-mails. Através desta documentação, você aprenderá a extrair métricas importantes e a entender o desempenho do seu servidor de e-mail usando comandos de análise de logs.

## Estrutura do `exim_mainlog`

O arquivo de log contém informações detalhadas sobre cada e-mail processado. Cada linha segue o formato:

- **Data e Hora**: Quando o evento ocorreu.
- **ID da Mensagem**: Identificador único para cada mensagem.
- **Direção**:
  - **<=**: Mensagem recebida.
  - **=>**: Mensagem enviada.
  - **==**: Tentativa de entrega falhou.
  - **<>**: Mensagem de bounce (sem remetente).
- **Remetente e Destinatário**: Endereços de e-mail.
- **Tamanho**: Tamanho da mensagem (em bytes).
- **Código de Retorno**: Resultado da entrega.
- **Serviço de Entrega**: Método utilizado (ex.: `smtp`, `local`).

### Exemplo de Linha de Log

```bash
2024-09-10 11:15:37 1Z6CcP-0002LU-3E <= sender@example.com H=mail.example.com [192.168.1.1] P=esmtpsa X=TLS1.2:ECDHE_RSA_AES_256_GCM_SHA384:256 S=12345 id=123456@example.com
```

Neste exemplo:

- **Data e Hora**: `2024-09-10 11:15:37`
- **ID da Mensagem**: `1Z6CcP-0002LU-3E`
- **Remetente**: `sender@example.com`
- **Tamanho**: `S=12345` (bytes)
- **Entrega Criptografada com TLS**: `X=TLS1.2:ECDHE_RSA_AES_256_GCM_SHA384`

---

## Comandos para Análise de Logs do Exim

### 1. Contar o Total de Mensagens Enviadas

Este comando conta todas as mensagens que foram enviadas com sucesso pelo servidor.

```bash
grep "=> " /var/log/exim_mainlog | wc -l
```

- **Explicação**: O comando `grep "=> "` busca todas as linhas no log que indicam uma entrega bem-sucedida (linhas marcadas com `=>`). O `wc -l` conta o número de linhas, ou seja, o número total de mensagens enviadas.

---

### 2. Contar o Total de Mensagens Recebidas

Este comando retorna o número total de mensagens recebidas pelo servidor.

```bash
grep "<= " /var/log/exim_mainlog | wc -l
```

- **Explicação**: O `grep "<= "` encontra todas as linhas que indicam mensagens recebidas (marcadas com `<=`). O `wc -l` conta essas linhas, fornecendo o total de mensagens recebidas.

---

### 3. Listar as 10 Maiores Mensagens

Este comando mostra as 10 maiores mensagens recebidas em termos de tamanho (bytes).

```bash
grep "<= " /var/log/exim_mainlog | awk '{print $NF, $0}' | sort -nr | head -10
```

- **Explicação**: O `grep "<= "` busca mensagens recebidas. O `awk '{print $NF, $0}'` extrai o tamanho da mensagem (último campo `S=`) e imprime junto com o resto da linha. O `sort -nr` organiza as mensagens por tamanho em ordem decrescente, e o `head -10` mostra as 10 maiores.

---

### 4. Contar Mensagens que Falharam na Entrega

Este comando conta todas as tentativas de entrega que falharam.

```bash
grep "== " /var/log/exim_mainlog | wc -l
```

- **Explicação**: O `grep "== "` busca linhas que indicam falha na entrega, marcadas com `==`. O `wc -l` conta essas linhas, fornecendo o total de falhas de entrega.

---

### 5. Contar Mensagens de Bounce (sem remetente)

Este comando encontra e conta todas as mensagens de bounce (sem remetente).

```bash
grep "<> " /var/log/exim_mainlog | wc -l
```

- **Explicação**: O `grep "<> "` busca mensagens de bounce (sem remetente), que são geralmente falhas de entrega que resultam no retorno da mensagem ao remetente original. O `wc -l` conta essas linhas.

---

### 6. Listar os 10 Destinatários Mais Frequentes

Este comando exibe os 10 destinatários que mais receberam e-mails no servidor.

```bash
grep "=> " /var/log/exim_mainlog | awk '{print $7}' | sort | uniq -c | sort -nr | head -10
```

- **Explicação**: O `grep "=> "` encontra as mensagens enviadas. O `awk '{print $7}'` extrai o endereço de e-mail do destinatário, e o `sort | uniq -c` contabiliza cada endereço. O `sort -nr` organiza os destinatários em ordem decrescente, e o `head -10` mostra os 10 mais frequentes.

---

### 7. Contar Mensagens Atrasadas

Este comando conta todas as mensagens que foram adiadas ou postergadas.

```bash
grep "deferred" /var/log/exim_mainlog | wc -l
```

- **Explicação**: O `grep "deferred"` busca por mensagens que foram adiadas (deferred), geralmente devido a problemas temporários. O `wc -l` conta essas linhas.

---

### 8. Analisar Conexões Recusadas

Este comando exibe todas as conexões que foram recusadas pelo servidor.

```bash
grep "refused" /var/log/exim_mainlog
```

- **Explicação**: O `grep "refused"` busca todas as conexões recusadas, o que pode indicar problemas de rede ou políticas de rejeição de conexões.

---

### 9. Listar os 10 Remetentes Mais Frequentes

Este comando mostra os remetentes que mais enviaram mensagens para o servidor.

```bash
grep "<= " /var/log/exim_mainlog | awk '{print $6}' | sort | uniq -c | sort -nr | head -10
```

- **Explicação**: O `grep "<= "` busca todas as mensagens recebidas. O `awk '{print $6}'` extrai o endereço do remetente, e o `sort | uniq -c` contabiliza cada um. O `sort -nr` organiza em ordem decrescente e o `head -10` mostra os 10 remetentes mais frequentes.

---

### 10. Verificar Mensagens Enviadas com TLS

Este comando encontra todas as mensagens enviadas com criptografia TLS.

```bash
grep "X=TLS" /var/log/exim_mainlog
```

- **Explicação**: O `grep "X=TLS"` busca por mensagens que foram transmitidas utilizando TLS (Transport Layer Security). Isso garante que a mensagem foi enviada de forma criptografada.

---

## Rastrear Mensagens por ID

Para obter o histórico completo de uma mensagem específica pelo seu ID, utilize:

```bash
grep "ID_da_Mensagem" /var/log/exim_mainlog
```

- **Explicação**: O `grep "ID_da_Mensagem"` busca todas as ocorrências de uma mensagem específica usando seu identificador único. Isso permite rastrear todo o ciclo de vida da mensagem no servidor.

---

## Conclusão

Este conjunto de comandos permite que você monitore e depure o desempenho do Exim e identifique problemas como falhas de entrega, atrasos e segurança. Use essas métricas para melhorar a administração do seu servidor de e-mails.
