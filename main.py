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


def coletar_atividades() -> List[AtividadePERT]:
    print("\n=== Planejamento PERT para Engenharia e Gestão de Projetos ===")
    print("Cadastre uma ou mais atividades. Pressione ENTER no nome para encerrar.\n")

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
                o = ler_float_positivo("  Otimista (O): ")
                m = ler_float_positivo("  Mais provável (M): ")
                p = ler_float_positivo("  Pessimista (P): ")
                validar_ordem(o, m, p)
                atividades.append(AtividadePERT(nome, o, m, p))
                print("  ✓ Atividade adicionada com sucesso.\n")
                break
            except ValueError as erro:
                print(f"  Erro: {erro} Tente novamente.\n")

    return atividades


def imprimir_relatorio_atividades(atividades: List[AtividadePERT]) -> None:
    print("\n" + "=" * 95)
    print("RELATÓRIO DE ATIVIDADES")
    print("=" * 95)
    cabecalho = (
        f"{'Atividade':<26} {'PERT':>10} {'Desvio':>10} {'Variância':>11} "
        f"{'Incerteza':>11} {'Risco':>10}"
    )
    print(cabecalho)
    print("-" * 95)

    for atividade in atividades:
        print(
            f"{atividade.nome:<26.26} "
            f"{atividade.estimativa:>10.2f} "
            f"{atividade.desvio_padrao:>10.2f} "
            f"{atividade.variancia:>11.2f} "
            f"{atividade.indice_incerteza:>10.1%} "
            f"{atividade.classificacao_risco:>10}"
        )


def imprimir_resumo_projeto(atividades: List[AtividadePERT]) -> None:
    media_total = sum(atividade.estimativa for atividade in atividades)
    variancia_total = sum(atividade.variancia for atividade in atividades)
    desvio_total = variancia_total**0.5

    print("\n" + "=" * 95)
    print("RESUMO CONSOLIDADO DO PROJETO")
    print("=" * 95)
    print(f"Atividades analisadas: {len(atividades)}")
    print(f"Estimativa total PERT: {media_total:.2f} dias")
    print(f"Desvio padrão total: ±{desvio_total:.2f} dias")

    niveis: Dict[float, str] = {
        0.68: "68%",
        0.90: "90%",
        0.95: "95%",
    }

    print("\nFaixas de prazo por nível de confiança:")
    for confianca, rotulo in niveis.items():
        inicio, fim = calcular_intervalo_confianca(media_total, desvio_total, confianca)
        print(f"• {rotulo:>3}: {inicio:.2f} a {fim:.2f} dias")

    print("\nLeitura gerencial:")
    print("• Use a faixa de 90% para compromissos com cliente e governança.")
    print("• Use 95% em contextos com alta criticidade de prazo (obras, comissionamento, startup).")
    print("• Atividades com risco ALTO merecem plano de resposta e buffer dedicado.")


def main() -> None:
    atividades = coletar_atividades()
    imprimir_relatorio_atividades(atividades)
    imprimir_resumo_projeto(atividades)


if __name__ == "__main__":
    main()
