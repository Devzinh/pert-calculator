def ler(prompt):
    while True:
        try:
            return float(input(prompt).replace(",", "."))
        except ValueError:
            print("Erro: digite um número válido")

o = ler("Digite o valor otimista: ")
m = ler("Digite o valor mais provável: ")
p = ler("Digite o valor pessimista: ")

def pert(o, m, p):
    if o <= 0 or m <= 0 or p <= 0:
        raise ValueError("Todos os valores devem ser maiores que zero")
    if not (o <= m <= p):
        raise ValueError("Ordem inválida: Otimista ≤ Mais Provável ≤ Pessimista")
    return (o + 4 * m + p) / 6, (p - o) / 6

try:
    est, dev = pert(o, m, p)
    print(f"\n{'='*50}")
    print(f"Estimativa PERT: {est:.2f} dias")
    print(f"Desvio Padrão: ±{dev:.2f} dias")
    print(f"{'='*50}")
    print(f"\n📊 Interpretação:")
    print(f"• A tarefa deve levar aproximadamente {est:.2f} dias")
    print(f"• Variação esperada: entre {est-dev:.2f} e {est+dev:.2f} dias")
    print(f"• Quanto maior o desvio (±{dev:.2f}), maior a incerteza")
except ValueError as e:
    print(f"Erro: {e}")
