# Trabalho de Auditoria — SANEPAR 2025

**Enzo Wetler Dória — matrícula 231019863 — UnB — Auditoria I**

**ENTREGA EM PARTES:** por limitações de download, o arquivo original de 500 mil registros foi subdividido em 10 arquivos `.csv.gz` de 50 mil linhas. Os 10 arquivos devem ficar em `base_simulada/`. O restante do trabalho está neste repositório. Execute `python codigo/reconstruir_e_testar.py` para conferir a base e reproduzir os testes. A mesma população foi preservada sem alteração de linhas.

**Comece pelo documento principal:** [Abrir dossiê PDF](dossie/Dossie_Auditoria_SANEPAR_2025_Enzo_Doria.pdf) e [planilha Excel](planilhas/Analises_Auditoria_SANEPAR_2025.xlsx).

**Aviso acadêmico:** As informações públicas foram analisadas e os dados e erros individuais são totalmente sintéticos. Não houve testes em sistemas internos ou emissão de opinião de auditoria.

---

# Dossiê de auditoria acadêmica — SANEPAR (exercício 2025)

**Aluno:** Enzo Wetler Dória · **Matrícula:** 231019863  
**Instituição:** Universidade de Brasília (UnB) · **Disciplina:** Auditoria I (CCA0024), turma 02, 2026.2  
**Professor:** Lucas Oliveira Gomes Ferreira · **Data:** 25/10/2026

> **Aviso importante:** Trabalho acadêmico. **Não é auditoria independente da SANEPAR nem opinião profissional sobre suas demonstrações financeiras.** Apenas saldos consolidados e divulgações foram consultados em fontes públicas. Os **500.000 registros analíticos são 100% sintéticos**, incluindo documentos, projetos, datas e erros artificialmente inseridos; nenhuma exceção constitui achado real da SANEPAR. Não houve visita, confirmação externa, entrevista, inspeção ou acesso a sistema interno.

**LEIA PRIMEIRO:** abra o dossiê principal em PDF; os 27 papéis de trabalho editáveis estão em Markdown, um formato de texto que o GitHub exibe no navegador.

## O que há aqui

| Pasta/arquivo | Conteúdo |
|---|---|
| `dossie/Dossie_Auditoria_SANEPAR_2025_Enzo_Doria.pdf` | Dossiê acadêmico consolidado, 31 páginas; 27 papéis de trabalho e conclusão integrada. |
| `papeis_trabalho/PT_*.md` | 27 papéis editáveis: EC, 200–330, 402–530, 540–600, conforme roteiro. |
| `base_simulada/base_intangivel_parte_01.csv.gz` até `base_intangivel_parte_10.csv.gz` | **500.000 linhas** divididas em 10 arquivos gzip independentes de 50 mil linhas cada, para facilitar o download e upload. |
| `base_simulada/README.md`, `controle_geracao.json`, `gabarito_erros_inseridos.csv` | Método, premissas, saldos por categoria e gabarito de anomalias artificiais. |
| `codigo/gerar_base.py`, `testes_auditoria.py`, `reconstruir_e_testar.py`, `analise_risco_amostral.py`, `requirements.txt` | Geração determinística, reconstrução, testes de qualidade e estudo amostral. |
| `planilhas/Analises_Auditoria_SANEPAR_2025.xlsx` | Excel editável com 11 abas, indicadores, matriz de riscos, cobertura, saldos e conciliações. |
| `docs/programas/` | Seis programas didáticos em Markdown: receita, caixa, estoques, imobilizado, passivos e estimativas. |
| `docs/modelos/` | Modelos didáticos em Markdown de carta, governança, deficiências, circularização e representações. **Não enviados**. |
| `fontes/` | Registro de fontes e vigência das normas, além das limitações da pesquisa. |
| `saidas/` | Amostra de 400 itens, arquivo de exceções, resultados dos testes. |
| `CONFERENCIA_ARQUIVOS.txt` | Inventário de arquivos da entrega. |

## Resultados da população sintética

- **500.000 itens únicos**, gerados com semente fixa `20251025`.
- Conciliação matemática por natureza contábil à **Nota 13(b) da DFP 2025 da SANEPAR**: custo R$ 17.778.415 mil, amortização acumulada R$ 5.176.088 mil e valor líquido R$ 12.602.327 mil.
- **428 exceções simuladas**: 180 divergências de recálculo, 123 datas além de 31/12/2025 e 125 referências fictícias ausentes.
- Varredura automatizada encontrou todas as 428 anomalias fabricadas, sem falsos positivos no conjunto controlado; a amostra exploratória de 400 itens não encontrou nenhuma.
- **Limitação central:** reproduzir saldos agregados não comprova existência, direitos, avaliação ou regularidade de ativos individualizados da companhia.

## Como reproduzir sem baixar o CSV

A base e os testes podem ser recriados localmente com Python 3.10+ e NumPy. Execute estes comandos a partir da raiz do repositório:

```bash
python -m pip install -r codigo/requirements.txt
mkdir reproducao
python codigo/gerar_base.py --destino reproducao
python codigo/testes_auditoria.py --destino reproducao
python codigo/analise_risco_amostral.py
```

O gerador e os testes usam semente fixa e arquivos rastreáveis. `reproducao/` está no `.gitignore` para evitar publicar 67 MB descompactados. O gabarito dos erros fica separado do algoritmo que detecta as exceções.

## Como ler e validar os 10 arquivos compactados

Cada arquivo `base_simulada/base_intangivel_parte_XX.csv.gz` é um CSV gzip autônomo com 50 mil registros (UTF-8, separador `;`, valores monetários em centavos inteiros). O conjunto contém 500 mil registros. Para reconstruir e testar: `python codigo/reconstruir_e_testar.py`. Não arredondar nem interpretar os centavos como reais.

## Limitações e revisão

- **EP (evidência pública):** leitura e análise de demonstrações e notas publicadas.
- **SIM (simulação):** 500 mil registros fabricados, gabarito, amostras e testes de regras.
- **PL (planejado):** testes que requerem acesso a registros internos, pessoas, documentos originais ou terceiros. Não foram executados.
- Os papéis incluem referências e localização **indicativa** de itens normativos, que devem ser confirmados diretamente na versão oficial aplicável a 2025; revisão independente não foi realizada.
- A base de 2025 não se confunde com as revisões de NBC TA 240 e 570 com vigência posterior. Conferir `fontes/normas_e_vigencia.md`.

## Fontes públicas

- SANEPAR, **Demonstrações Financeiras Padronizadas 2025**, Nota 13(b): <https://ri.sanepar.com.br/docs/DFP-Sanepar-2025-12-31-BjdwmKcn.pdf>.
- SANEPAR, relações com investidores: <https://ri.sanepar.com.br/pt/apresentacoes-e-relatorios/relatorios-anuais>.
- CFC, NBC TA — auditoria independente: <https://cfc.org.br/tecnica/normas-brasileiras-de-contabilidade/nbc-ta-de-auditoria-independente/>.
- Consulte `fontes/registro_de_fontes.csv` para detalhamento e observações sobre referências.

## Formatos de arquivos: por que alguns não são documentos comuns

Os arquivos `.md` são textos para o GitHub e podem não abrir bem no Windows; mas podem ser lidos diretamente no GitHub; o dossiê principal está em PDF. Os dez `.csv.gz` são as partes compactadas da base (não são PDFs). Os `.py` são programas, não relatórios. Modelos de confirmação externa e assinatura têm campos intencionalmente não preenchidos porque não houve acesso a terceiros.

## Como entregar no GitHub

**Não envie o ZIP de entrega fechado ao GitHub** se quiser que as pastas apareçam como neste README. Extraia `01_DOCUMENTOS_E_CODIGOS.zip` e envie **seu conteúdo interno** ao repositório usando `Add file` → `Upload files`; depois envie as dez partes `.csv.gz` para dentro de `base_simulada/`. O professor deve ver estas pastas diretamente na página inicial, junto deste README. Cada parte tem cerca de 1,4 MB, abaixo do limite de upload pelo navegador.
