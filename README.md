# Analisador de Logs do Exim com Foco em Segurança

Este projeto consiste em uma ferramenta desenvolvida em Python para analisar os logs do Exim (`exim_mainlog`) com foco em identificar eventos relacionados à segurança, como falhas de autenticação, conexões recusadas, mensagens de bounce, uso de TLS e padrões de spam.

## Funcionalidades

- **Falhas de Autenticação**: Identifica tentativas de login falhadas.
- **Conexões Recusadas**: Detecta IPs que estão recusando conexões repetidamente.
- **Mensagens de Bounce e Deferred**: Conta mensagens que falharam na entrega ou foram adiadas.
- **Uso de TLS**: Verifica o uso de criptografia TLS nas transmissões.
- **Padrões de Spam**: Identifica remetentes que enviam grandes volumes de e-mails.

## Requisitos

- Python 3.6 ou superior
- Bibliotecas Python listadas em `requirements.txt`

## Instalação

1. **Clone o Repositório**

   ```bash
   git clone https://github.com/lvluanvinicius/exim-log-analyzer.git
   cd exim-log-analyzer
   ```
