# Sistema de Agendamento de Barbearia (CLI)

Um sistema simples e eficiente de agendamento para barbearias, desenvolvido em Python com interface de linha de comando (CLI). Ideal para pequenos negócios que desejam organizar seus agendamentos sem necessidade de internet ou instalação de software complexo.

## 📦 Instalação

1. Certifique-se de ter o Python instalado (versão 3.6 ou superior)
2. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/sistema-agendamento-barbearia.git
   cd sistema-agendamento-barbearia
   ```

3. Execute o programa:
   ```bash
   python main.py
   ```

## 🚀 Como Usar

O sistema é totalmente interativo e roda no terminal. Após executar `python main.py`, você verá um menu com as opções disponíveis:

```
=== SISTEMA DE AGENDAMENTO DE BARBEARIA ===
1. Visualizar todos os agendamentos
2. Novo agendamento
3. Cancelar agendamento
4. Buscar agendamentos por cliente
5. Mostrar agenda do dia
6. Sair

Escolha uma opção (1-6): 
```

### Exemplos de Uso

**1. Criar um novo agendamento:**
```
Escolha uma opção: 2
Nome do cliente: João Silva
Serviços disponíveis:
1. Corte de cabelo (R$ 30.00, 30min)
2. Barba (R$ 20.00, 20min)
3. Corte + Barba (R$ 45.00, 50min)
4. Sobrancelha (R$ 10.00, 10min)

Escolha o serviço (1-4): 3
Data (DD/MM/AAAA): 25/12/2023
Hora (HH:MM): 14:30

Agendamento realizado com sucesso!
ID: 1 | João Silva - Corte + Barba em 25/12/2023 às 14:30
```

**2. Visualizar todos os agendamentos:**
```
Escolha uma opção: 1

--- TODOS OS AGENDAMENTOS ---
ID   Cliente              Serviço         Data         Hora     Preço   
----------------------------------------------------------------------
1    João Silva           Corte + Barba   25/12/2023   14:30    R$ 45.00
2    Maria Oliveira       Corte de cabelo 25/12/2023   15:30    R$ 30.00
----------------------------------------------------------------------
Total de agendamentos: 2 | Receita total: R$ 75.00
```

**3. Mostrar agenda do dia:**
```
Escolha uma opção: 5

--- AGENDA DE HOJE (25/12/2023) ---
ID   Cliente              Serviço         Hora     Preço   
------------------------------------------------------------
1    João Silva           Corte + Barba   14:30    R$ 45.00
2    Maria Oliveira       Corte de cabelo 15:30    R$ 30.00
------------------------------------------------------------
Total para hoje: 2 agendamento(s) | Receita: R$ 75.00
```

## ✅ Funcionalidades

- **Agendamento de clientes** com validação de horários
- **Serviços pré-definidos** com preços e durações
- **Verificação de conflitos** de horário
- **Busca por nome do cliente**
- **Visualização da agenda diária**
- **Cancelamento de agendamentos**
- **Armazenamento persistente** em arquivo JSON
- **Tratamento de erros** e entradas inválidas
- **Interface simples e intuitiva** em português

## 🗂 Estrutura de Arquivos

```
sistema-agendamento-barbearia/
├── main.py                 # Código principal do sistema
├── agendamentos.json       # Banco de dados de agendamentos
├── .gitignore              # Arquivos ignorados pelo Git
└── README.md               # Este arquivo de documentação
```

## 🛠 Tecnologias Utilizadas

- Python 3
- JSON para armazenamento de dados
- Bibliotecas padrão: datetime, json, os

## 📝 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.