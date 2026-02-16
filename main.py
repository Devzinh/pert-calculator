from __future__ import annotations

from dataclasses import dataclass
from statistics import NormalDist
from typing import Dict, List, Tuple


@dataclass
class AtividadePERT:
    nome: str
    otimista: float
    mais_provavel: float
    pessimista: float

    @property
    def estimativa(self) -> float:
        return (self.otimista + 4 * self.mais_provavel + self.pessimista) / 6

    @property
    def desvio_padrao(self) -> float:
        return (self.pessimista - self.otimista) / 6

    @property
    def variancia(self) -> float:
        return self.desvio_padrao**2

    @property
    def indice_incerteza(self) -> float:
        if self.estimativa == 0:
            return 0.0
        return self.desvio_padrao / self.estimativa

    @property
    def classificacao_risco(self) -> str:
        indice = self.indice_incerteza
        if indice < 0.10:
            return "Baixo"
        if indice < 0.20:
            return "Moderado"
        return "Alto"


def imprimir_linha(largura: int = 90) -> None:
    print("─" * largura)


def imprimir_titulo(titulo: str, subtitulo: str | None = None) -> None:
    largura = 90
    print("\n" + "═" * largura)
    print(titulo.center(largura))
    if subtitulo:
        print(subtitulo.center(largura))
    print("═" * largura)


def exibir_boas_vindas() -> None:
    imprimir_titulo(
        "CALCULADORA PERT PARA ENGENHARIA",
        "Planejamento didático, objetivo e orientado à decisão",
    )
    print("Como preencher cada atividade:")
    print("  1) Otimista (O): melhor cenário realista.")
    print("  2) Mais provável (M): cenário esperado na rotina.")
    print("  3) Pessimista (P): pior cenário plausível.")
    print("\nFórmula PERT: (O + 4M + P) / 6")
    print("Regra obrigatória: O ≤ M ≤ P")
    print("Dica: use a mesma unidade para todo o projeto (dias, horas, semanas etc.).")


def ler_float_positivo(prompt: str) -> float:
    while True:
        entrada = input(prompt).strip().replace(",", ".")
        try:
            valor = float(entrada)
            if valor <= 0:
                print("Erro: informe um número maior que zero.")
                continue
            return valor
        except ValueError:
            print("Erro: digite um número válido (ex.: 10.5).")


def ler_nome_atividade() -> str:
    while True:
        nome = input("Nome da atividade (ENTER para finalizar): ").strip()
        if nome:
            return nome
        return ""


def ler_unidade_tempo() -> str:
    print("\nUnidade de tempo do projeto")
    imprimir_linha()
    print("1) Dias")
    print("2) Horas")
    print("3) Semanas")
    print("4) Personalizada")

    while True:
        escolha = input("Escolha [1-4]: ").strip()
        opcoes = {"1": "dias", "2": "horas", "3": "semanas"}
        if escolha in opcoes:
            return opcoes[escolha]
        if escolha == "4":
            unidade = input("Digite a unidade desejada: ").strip().lower()
            if unidade:
                return unidade
            print("Erro: informe um nome de unidade válido.")
            continue
        print("Erro: escolha uma opção entre 1 e 4.")


def validar_ordem(o: float, m: float, p: float) -> None:
    if not (o <= m <= p):
        raise ValueError("Ordem inválida: use Otimista ≤ Mais Provável ≤ Pessimista.")


def calcular_intervalo_confianca(
    media: float, desvio: float, confianca: float
) -> Tuple[float, float]:
    if desvio == 0:
        return media, media

    z = NormalDist().inv_cdf((1 + confianca) / 2)
    margem = z * desvio
    return media - margem, media + margem


def coletar_atividades(unidade_tempo: str) -> List[AtividadePERT]:
    print("\nCadastro de atividades")
    imprimir_linha()
    print("Pressione ENTER no nome quando terminar o cadastro.\n")

    atividades: List[AtividadePERT] = []

    while True:
        nome = ler_nome_atividade()
        if not nome:
            if atividades:
                break
            print("Você precisa cadastrar pelo menos uma atividade.")
            continue

        while True:
            try:
                o = ler_float_positivo(f"  Otimista (O) em {unidade_tempo}: ")
                m = ler_float_positivo(f"  Mais provável (M) em {unidade_tempo}: ")
                p = ler_float_positivo(f"  Pessimista (P) em {unidade_tempo}: ")
                validar_ordem(o, m, p)
                atividade = AtividadePERT(nome, o, m, p)
                atividades.append(atividade)
                print(
                    f"  ✓ Atividade adicionada | PERT: {atividade.estimativa:.2f} {unidade_tempo} | "
                    f"Risco: {atividade.classificacao_risco}\n"
                )
                break
            except ValueError as erro:
                print(f"  Erro: {erro} Tente novamente.\n")

    return atividades


def imprimir_relatorio_atividades(atividades: List[AtividadePERT], unidade_tempo: str) -> None:
    imprimir_titulo("RELATÓRIO DE ATIVIDADES")
    cabecalho = (
        f"{'Atividade':<24} {'PERT':>11} {'Desvio':>11} {'Variância':>11} "
        f"{'Incerteza':>11} {'Risco':>10}"
    )
    print(cabecalho)
    imprimir_linha()

    for atividade in atividades:
        print(
            f"{atividade.nome:<24.24} "
            f"{atividade.estimativa:>8.2f} {unidade_tempo[:2]:>2} "
            f"{atividade.desvio_padrao:>8.2f} {unidade_tempo[:2]:>2} "
            f"{atividade.variancia:>11.2f} "
            f"{atividade.indice_incerteza:>10.1%} "
            f"{atividade.classificacao_risco:>10}"
        )


def imprimir_resumo_projeto(atividades: List[AtividadePERT], unidade_tempo: str) -> None:
    media_total = sum(atividade.estimativa for atividade in atividades)
    variancia_total = sum(atividade.variancia for atividade in atividades)
    desvio_total = variancia_total**0.5

    imprimir_titulo("RESUMO CONSOLIDADO DO PROJETO")
    print(f"Atividades analisadas: {len(atividades)}")
    print(f"Estimativa total PERT: {media_total:.2f} {unidade_tempo}")
    print(f"Desvio padrão total: ±{desvio_total:.2f} {unidade_tempo}")

    niveis: Dict[float, str] = {
        0.68: "68%",
        0.90: "90%",
        0.95: "95%",
    }

    print("\nFaixas de prazo por nível de confiança:")
    for confianca, rotulo in niveis.items():
        inicio, fim = calcular_intervalo_confianca(media_total, desvio_total, confianca)
        print(f"• {rotulo:>3}: {inicio:.2f} a {fim:.2f} {unidade_tempo}")

    print("\nLeitura gerencial sugerida:")
    print("• 68%: bom para simulações rápidas e alinhamentos internos.")
    print("• 90%: recomendável para compromissos com cliente e governança.")
    print("• 95%: usar em cenários críticos de segurança, obra ou comissionamento.")
    print("• Atividades com risco ALTO pedem plano de mitigação e contingência dedicada.")


def imprimir_encerramento() -> None:
    imprimir_linha()
    print("Fim da análise. Use este relatório para orientar prazo, risco e contingência.")
    imprimir_linha()


def main() -> None:
    exibir_boas_vindas()
    unidade_tempo = ler_unidade_tempo()
    atividades = coletar_atividades(unidade_tempo)
    imprimir_relatorio_atividades(atividades, unidade_tempo)
    imprimir_resumo_projeto(atividades, unidade_tempo)
    imprimir_encerramento()


if __name__ == "__main__":
    main()
