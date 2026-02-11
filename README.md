# PERT Calculator

Ferramenta de linha de comando para estimativas de prazo com PERT (Program Evaluation Review Technique), pensada para apoiar **engenharia** e **gerenciamento de projetos**.

## O que o método PERT calcula?

Para cada atividade:
- **Otimista (O)**: cenário mais favorável
- **Mais provável (M)**: cenário esperado
- **Pessimista (P)**: cenário mais desfavorável

Fórmulas:
- `PERT = (O + 4M + P) / 6`
- `Desvio padrão (σ) = (P - O) / 6`
- `Variância = σ²`

## Melhorias implementadas

- Cadastro de **múltiplas atividades** em uma única execução.
- Relatório tabular por atividade com:
  - estimativa PERT,
  - desvio padrão,
  - variância,
  - índice de incerteza,
  - classificação de risco (Baixo/Moderado/Alto).
- Resumo consolidado do projeto com:
  - prazo total esperado,
  - desvio padrão total,
  - faixas de confiança de **68%, 90% e 95%**.
- Mensagens orientadas à tomada de decisão para gestores de projeto.
- Validações robustas de entrada e regra `O ≤ M ≤ P`.

## Como usar

```bash
python main.py
```

### Fluxo

1. Informe o nome da atividade.
2. Preencha O, M e P.
3. Repita para quantas atividades quiser.
4. Pressione ENTER no nome da atividade para encerrar e gerar o relatório.

## Exemplo de aplicação prática

Em cronogramas de engenharia (projeto básico, detalhamento, suprimentos, construção e comissionamento), a ferramenta ajuda a:
- identificar tarefas com maior incerteza;
- construir reservas de contingência com base em risco;
- definir compromissos de prazo com nível de confiança adequado.
