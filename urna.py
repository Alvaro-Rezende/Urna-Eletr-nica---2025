import pickle
import os


def carregar_candidatos():
    dic_candidatos = {}
    try:
        with open("candidatos.txt", "r", encoding="utf-8") as arq:
            for linha in arq:
                linha_limpa = linha.strip()
                if not linha_limpa:
                    continue
                dados = linha.split(",")
                nome = dados[0].strip()
                numero = dados[1].strip()
                partido = dados[2].strip()
                estado = dados[3].strip()
                cargo = dados[4].strip()

                if cargo not in dic_candidatos:
                    dic_candidatos[cargo] = {}

                dic_candidatos[cargo][numero] = {
                    "nome": nome,
                    "partido": partido,
                    "estado": estado
                }
        print("Candidatos carregados com sucesso!")
        return dic_candidatos
    except:
        print("Erro ao carregar o arquivo de candidatos!")
        return {}


def carregar_eleitores():
    dic_eleitores = {}
    try:
        with open("eleitores.txt", "r", encoding="utf-8") as arq:
            for linha in arq:
                linha_limpa = linha.strip()
                if not linha_limpa:
                    continue
                dados = linha.split(",")
                if len(dados) >= 5:
                    nome = dados[0].strip()
                    rg = dados[1].strip()
                    titulo = dados[2].strip()
                    municipio = dados[3].strip()
                    uf = dados[4].strip()

                    dic_eleitores[titulo] = {
                        "nome": nome,
                        "rg": rg,
                        "municipio": municipio,
                        "uf": uf
                    }
        print("Eleitores carregados com sucesso!")
        return dic_eleitores
    except:
        print("Erro ao carregar eleitores!")
        return {}


def verificar_ja_votou(titulo):
    try:
        if not os.path.exists("ja_votaram.txt"):
            return False
        with open("ja_votaram.txt", "r") as arq:
            eleitores_que_votaram = arq.read().splitlines()
        return titulo in eleitores_que_votaram
    except:
        return False


def registrar_que_votou(titulo):
    with open("ja_votaram.txt", "a") as arq:
        arq.write(titulo + "\n")


def iniciar_votacao(candidatos, eleitores):
    if not candidatos or not eleitores:
        print("Erro: Carregue os candidatos e eleitores primeiro.")
        return

    uf_urna = input("Informe a UF da Urna: ").strip().upper()
    titulo = input("Informe o Título de Eleitor: ").strip()

    if titulo not in eleitores:
        print("Eleitor não encontrado!")
        return

    if verificar_ja_votou(titulo):
        print("Atenção: Este eleitor JÁ votou!")
        return

    eleitor = eleitores[titulo]
    print(f"Eleitor: {eleitor['nome']} | Estado: {eleitor['uf']}")

    ordem_votacao = [
        ("Deputado Federal", "F"),
        ("Deputado Estadual", "E"),
        ("Senador", "S"),
        ("Governador", "G"),
        ("Presidente", "P")
    ]

    voto_atual = {"UF_URNA": uf_urna}

    for cargo_nome, codigo_cargo in ordem_votacao:
        confirmado = False
        while not confirmado:
            print(f"\n--- Voto para {cargo_nome} ---")
            numero = input(
                "Digite o número (ou B para Branco): ").strip().upper()

            voto_registrado = "N"

            if numero == "B":
                print("Voto em BRANCO.")
                voto_registrado = "B"
            else:
                candidatos_do_cargo = candidatos.get(codigo_cargo, {})
                if numero in candidatos_do_cargo:
                    cand = candidatos_do_cargo[numero]
                    print(
                        f"Candidato: {cand['nome']} | Partido: {cand['partido']}")

                    if codigo_cargo != "P" and cand["estado"] != eleitor["uf"]:
                        print("ATENÇÃO: Voto NULO (Candidato de outro estado).")
                        voto_registrado = "N"
                    else:
                        voto_registrado = numero
                else:
                    print("Número inválido! Voto NULO.")
                    voto_registrado = "N"

            conf = input("Confirma? (S/N): ").upper()
            if conf == "S":
                voto_atual[codigo_cargo] = voto_registrado
                confirmado = True

    try:
        with open("votos.bin", "ab") as arq:
            pickle.dump(voto_atual, arq)
        registrar_que_votou(titulo)
        print("\n✅ Votação concluída com sucesso!")
    except:
        print("Erro ao salvar o voto.")


def apurar_votos():
    if not os.path.exists("votos.bin"):
        print("Nenhum voto para apurar.")
        return

    contagem = {}
    total_votos = 0

    try:
        with open("votos.bin", "rb") as arq:
            while True:
                try:
                    voto = pickle.load(arq)
                    total_votos += 1
                    for cargo, valor in voto.items():
                        if cargo == "UF_URNA":
                            continue

                        if cargo not in contagem:
                            contagem[cargo] = {}

                        if valor not in contagem[cargo]:
                            contagem[cargo][valor] = 0

                        contagem[cargo][valor] += 1
                except EOFError:
                    break

        print("\n=== APURAÇÃO ===")
        print(f"Total de votos computados: {total_votos}")
        gerar_boletim(contagem, total_votos)

    except:
        print("Erro ao ler arquivo de votos.")


def gerar_boletim(contagem, total_votos):
    try:
        with open("boletim.txt", "w", encoding="utf-8") as arq:
            arq.write("=== BOLETIM DE URNA ===\n")
            arq.write(
                f"Total de Eleitores que compareceram: {total_votos}\n\n")

            cargos_nomes = {"P": "Presidente", "G": "Governador",
                            "S": "Senador", "F": "Dep. Federal", "E": "Dep. Estadual"}

            for cargo_cod, votos_cargo in contagem.items():
                nome_cargo = cargos_nomes.get(cargo_cod, cargo_cod)
                arq.write(f"--- {nome_cargo} ---\n")

                for cand, qtd in votos_cargo.items():
                    if cand == "B":
                        nome_cand = "BRANCO"
                    elif cand == "N":
                        nome_cand = "NULO"
                    else:
                        nome_cand = f"Candidato {cand}"

                    porcentagem = (qtd / total_votos) * 100
                    arq.write(
                        f"{nome_cand}: {qtd} votos ({porcentagem:.2f}%)\n")
                arq.write("\n")
        print("Arquivo 'boletim.txt' gerado com sucesso!")
    except:
        print("Erro ao gravar boletim.")


candidatos_global = {}
eleitores_global = {}

while True:
    print("\n=== SISTEMA DE URNA ELETRÔNICA ===")
    print("1 - Ler arquivo de candidatos")
    print("2 - Ler arquivo de eleitores")
    print("3 - Iniciar votação")
    print("4 - Apurar votos e Gerar Boletim")
    print("6 - Fechar programa")

    try:
        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            candidatos_global = carregar_candidatos()
        elif opcao == 2:
            eleitores_global = carregar_eleitores()
        elif opcao == 3:
            iniciar_votacao(candidatos_global, eleitores_global)
        elif opcao == 4:
            apurar_votos()
        elif opcao == 6:
            print("Saindo...")
            break
        else:
            print("Opção inválida.")
    except ValueError:
        print("Digite apenas números.")
