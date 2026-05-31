from datetime import datetime, timedelta
import os
import json

ARQUIVO_JSON = "agendamentos.json"


def carregar_agendamentos():
    """Carrega os agendamentos do arquivo JSON. Se não existir, retorna lista vazia."""
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            try:
                dados = json.load(f)
                if isinstance(dados, list):
                    return dados
                return []
            except json.JSONDecodeError:
                return []
    return []


def salvar_agendamentos(agendamentos):
    """Salva a lista de agendamentos no arquivo JSON."""
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(agendamentos, f, ensure_ascii=False, indent=4)


def exibir_menu():
    """Exibe o menu principal com as opções disponíveis."""
    print("
=== SISTEMA DE AGENDAMENTO DE BARBEARIA ===")
    print("1. Ver todos os agendamentos")
    print("2. Novo agendamento")
    print("3. Cancelar agendamento")
    print("4. Buscar agendamentos por cliente")
    print("5. Mostrar agenda do dia")
    print("6. Sair")
    return input("
Escolha uma opção (1-6): ").strip()


def validar_data(data_str):
    """Valida se a string representa uma data válida no formato DD/MM/AAAA."""
    try:
        data = datetime.strptime(data_str, "%d/%m/%Y")
        hoje = datetime.now().date()
        if data.date() < hoje:
            print("Erro: Não é possível agendar em datas passadas.")
            return False
        return True
    except ValueError:
        print("Erro: Formato de data inválido. Use DD/MM/AAAA (ex: 31/12/2023).")
        return False


def validar_hora(hora_str):
    """Valida se a string representa uma hora válida no formato HH:MM."""
    try:
        datetime.strptime(hora_str, "%H:%M")
        return True
    except ValueError:
        print("Erro: Formato de hora inválido. Use HH:MM (ex: 14:30).")
        return False


def obter_servicos():
    """Retorna dicionário com serviços, preços e durações."""
    return {
        "1": ("Corte de cabelo", 30.0, 30),
        "2": ("Barba", 20.0, 20),
        "3": ("Corte + Barba", 45.0, 50),
    }


def obter_duracao_servico(nome_servico):
    """Retorna a duração em minutos de um serviço pelo nome."""
    servicos = obter_servicos()
    for _, (nome, _, duracao) in servicos.items():
        if nome == nome_servico:
            return timedelta(minutes=duracao)
    return timedelta(minutes=30)


def horario_disponivel(agendamentos, data, hora, duracao):
    """Verifica se o horário está disponível considerando a duração do serviço."""
    try:
        hora_inicio = datetime.strptime(f"{data} {hora}", "%d/%m/%Y %H:%M")
        hora_fim = hora_inicio + duracao

        for ag in agendamentos:
            if ag["data"] != data:
                continue

            ag_inicio = datetime.strptime(f'{ag["data"]} {ag["hora"]}', "%d/%m/%Y %H:%M")
            ag_fim = ag_inicio + timedelta(minutes=ag.get("duracao", 30))

            if not (hora_fim <= ag_inicio or hora_inicio >= ag_fim):
                return False

        return True
    except Exception as e:
        print(f"Erro ao verificar disponibilidade: {e}")
        return False


def novo_agendamento(agendamentos):
    """Realiza um novo agendamento com validações."""
    print("
--- NOVO AGENDAMENTO ---")

    while True:
        nome = input("Nome do cliente: ").strip()
        if nome:
            break
        print("O nome do cliente não pode estar vazio.")

    servicos = obter_servicos()
    print("
Serviços disponíveis:")
    for key, (nome, preco, duracao) in servicos.items():
        print(f"{key}. {nome} (R$ {preco:.2f}, {duracao}min)")

    while True:
        escolha = input("
Escolha o serviço (1-3): ").strip()
        if escolha in servicos:
            nome_servico, preco_servico, duracao_servico = servicos[escolha]
            break
        print("Opção inválida. Escolha entre 1 e 3.")

    while True:
        data = input("Data (DD/MM/AAAA): ").strip()
        if validar_data(data):
            break

    while True:
        hora = input("Hora (HH:MM): ").strip()
        if not validar_hora(hora):
            continue

        try:
            hora_check = datetime.strptime(f"{data} {hora}", "%d/%m/%Y %H:%M")
            if hora_check < datetime.now():
                print("Erro: Não é possível agendar em horários passados.")
                continue
        except Exception:
            print("Erro ao validar horário.")
            continue

        break

    if not horario_disponivel(agendamentos, data, hora, timedelta(minutes=duracao_servico)):
        print("
Erro: Horário não disponível. Já existe um agendamento neste período.")
        return

    novo_id = max([ag["id"] for ag in agendamentos], default=0) + 1

    novo = {
        "id": novo_id,
        "nome_cliente": nome,
        "servico": nome_servico,
        "preco": preco_servico,
        "data": data,
        "hora": hora,
        "duracao": duracao_servico
    }

    agendamentos.append(novo)
    salvar_agendamentos(agendamentos)
    print("
Agendamento realizado com sucesso!")


def visualizar_todos(agendamentos):
    """Exibe todos os agendamentos ordenados por data e hora."""
    if not agendamentos:
        print("
Nenhum agendamento encontrado.")
        return

    agendamentos_ordenados = sorted(agendamentos, key=lambda x: (x["data"], x["hora"]))

    print("
--- TODOS OS AGENDAMENTOS ---")
    print(f"{'ID':<4} {'Cliente':<20} {'Serviço':<15} {'Data':<12} {'Hora':<8} {'Preço':<8}")
    print("-" * 70)

    total_receita = 0
    for ag in agendamentos_ordenados:
        print(f"{ag['id']:<4} {ag['nome_cliente']:<20} {ag['servico']:<15} {ag['data']:<12} {ag['hora']:<8} R$ {ag['preco']:<7.2f}")
        total_receita += ag["preco"]

    print("-" * 70)
    print(f"Total de agendamentos: {len(agendamentos_ordenados)} | Receita total: R$ {total_receita:.2f}")


def cancelar_agendamento(agendamentos):
    """Cancela um agendamento pelo ID."""
    if not agendamentos:
        print("
Nenhum agendamento para cancelar.")
        return

    visualizar_todos(agendamentos)

    while True:
        try:
            id_cancelar = int(input("
Digite o ID do agendamento para cancelar (0 para voltar): "))
            if id_cancelar == 0:
                return

            agendamento = next((ag for ag in agendamentos if ag["id"] == id_cancelar), None)
            if agendamento:
                confirm = input(
                    f"Tem certeza que deseja cancelar o agendamento de {agendamento['nome_cliente']} "
                    f"em {agendamento['data']} às {agendamento['hora']}? (s/n): "
                ).strip().lower()

                if confirm == "s":
                    agendamentos.remove(agendamento)
                    salvar_agendamentos(agendamentos)
                    print(f"Agendamento ID {id_cancelar} cancelado com sucesso!")
                    return
                else:
                    print("Cancelamento interrompido.")
                    return
            else:
                print("ID não encontrado. Tente novamente.")
        except ValueError:
            print("Por favor, digite um número válido.")
        except KeyboardInterrupt:
            print("
Operação cancelada.")
            return


def buscar_por_cliente(agendamentos):
    """Busca agendamentos por nome do cliente."""
    if not agendamentos:
        print("
Nenhum agendamento encontrado.")
        return

    nome_busca = input("
Digite o nome do cliente para buscar: ").strip().lower()
    if not nome_busca:
        print("Nome não pode estar vazio.")
        return

    resultados = [ag for ag in agendamentos if nome_busca in ag["nome_cliente"].lower()]

    if resultados:
        print(f"
--- RESULTADOS PARA '{nome_busca.upper()}' ---")
        print(f"{'ID':<4} {'Cliente':<20} {'Serviço':<15} {'Data':<12} {'Hora':<8} {'Preço':<8}")
        print("-" * 70)

        total_receita = 0
        for ag in resultados:
            print(f"{ag['id']:<4} {ag['nome_cliente']:<20} {ag['servico']:<15} {ag['data']:<12} {ag['hora']:<8} R$ {ag['preco']:<7.2f}")
            total_receita += ag["preco"]

        print("-" * 70)
        print(f"Total encontrado: {len(resultados)} agendamento(s) | Receita: R$ {total_receita:.2f}")
    else:
        print(f"
Nenhum agendamento encontrado para o cliente '{nome_busca}'.")


def mostrar_agenda_do_dia(agendamentos):
    """Mostra todos os agendamentos do dia atual."""
    hoje = datetime.now().strftime("%d/%m/%Y")
    agendamentos_hoje = [ag for ag in agendamentos if ag["data"] == hoje]

    if agendamentos_hoje:
        agendamentos_ordenados = sorted(agendamentos_hoje, key=lambda x: x["hora"])

        print(f"
--- AGENDA DE HOJE ({hoje}) ---")
        print(f"{'ID':<4} {'Cliente':<20} {'Serviço':<15} {'Hora':<8} {'Preço':<8}")
        print("-" * 60)

        total_receita = 0
        for ag in agendamentos_ordenados:
            print(f"{ag['id']:<4} {ag['nome_cliente']:<20} {ag['servico']:<15} {ag['hora']:<8} R$ {ag['preco']:<7.2f}")
            total_receita += ag["preco"]

        print("-" * 60)
        print(f"Total para hoje: {len(agendamentos_ordenados)} agendamento(s) | Receita: R$ {total_receita:.2f}")
    else:
        print(f"
Nenhum agendamento para hoje ({hoje}).")


def main():
    """Função principal que executa o loop do sistema."""
    print("Bem-vindo ao Sistema de Agendamento de Barbearia!")
    agendamentos = carregar_agendamentos()

    while True:
        try:
            opcao = exibir_menu()

            if opcao == "1":
                visualizar_todos(agendamentos)
            elif opcao == "2":
                novo_agendamento(agendamentos)
            elif opcao == "3":
                cancelar_agendamento(agendamentos)
            elif opcao == "4":
                buscar_por_cliente(agendamentos)
            elif opcao == "5":
                mostrar_agenda_do_dia(agendamentos)
            elif opcao == "6":
                print("
Obrigado por usar o sistema! Até logo.")
                break
            else:
                print("
Opção inválida. Escolha entre 1 e 6.")
        except KeyboardInterrupt:
            print("

Programa interrompido pelo usuário. Até logo!")
            break
        except Exception as e:
            print(f"
Erro inesperado: {e}")
            print("O programa será encerrado.")
            break


if __name__ == "__main__":
    main()