# Base sintética — versão dividida para GitHub

A população é **exclusivamente sintética**. Nenhuma linha representa lançamento real da SANEPAR.

Os arquivos `base_intangivel_parte_01.csv.gz` a `base_intangivel_parte_10.csv.gz` contêm 50.000 linhas cada (total 500.000). Todos são CSV comprimidos por gzip, delimitados por `;` e com cabeçalho repetido. São arquivos autônomos que podem ser lidos por Python/pandas.

Não descompacte nem renomeie as partes para fazer o upload. Coloque as 10 partes **nesta pasta**. Rode da raiz do projeto:

```bash
python codigo/reconstruir_e_testar.py
```

O script verifica as 10 partes, reconstrói o CSV temporário, roda `testes_auditoria.py`, salva resultados na pasta `saidas/` e remove o CSV temporário. Requer Python 3, somente biblioteca padrão. Conferência esperada: 500000 registros; 428 erros artificiais detectados.

Custo R$ 17.778.415.000, amortização acumulada R$ 5.176.088.000, valor líquido sintético corrigido R$ 12.602.327.000 (saldos divulgados na Nota 13(b) da DFP 2025 da SANEPAR). Os erros são injetados deliberadamente e explicados em `gabarito_erros_inseridos.csv`.
