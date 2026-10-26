"""Reconstrói arquivo original das 10 partes gzip e executa os testes cegos.
Uso: python codigo/reconstruir_e_testar.py  (na raiz do repositório)
Biblioteca padrão do Python 3.10+.
"""
import csv, gzip, shutil, sys, tempfile, json
from pathlib import Path
base=Path(__file__).resolve().parent.parent
s=base/'base_simulada'
parts=[s/f'base_intangivel_parte_{i:02d}.csv.gz' for i in range(1,11)]
missing=[p.name for p in parts if not p.is_file()]
if missing: raise SystemExit('Faltam partes: '+', '.join(missing))
with tempfile.TemporaryDirectory() as td:
    d=Path(td)
    output=d/'base_intangivel_sintetica.csv'
    with output.open('wb') as dest:
        reference=None; total=0
        for i,p in enumerate(parts):
            with gzip.open(p,'rb') as f:
                header=f.readline()
                if reference is None: reference=header
                if header!=reference: raise SystemExit('Cabeçalho diferente em '+p.name)
                if i==0: dest.write(header)
                count=0
                for line in f:
                    dest.write(line);count+=1
                if count!=50000: raise SystemExit(f'{p.name}: esperadas 50000 linhas, encontrado {count}')
                total+=count
                print(f'OK {p.name}: {count} registros')
    if total!=500000: raise SystemExit(f'Total inválido: {total}')
    for name in ['controle_geracao.json','gabarito_erros_inseridos.csv']:
        shutil.copy2(s/name,d/name)
    sys.path.insert(0,str(base/'codigo'))
    from testes_auditoria import testar
    r=testar(d)
    if r['registros']!=500000 or r['excecoes_detectadas']!=428 or r['falsos_positivos']!=0 or r['falsos_negativos']!=0:
        raise SystemExit('Falha na conferência automática')
    (base/'saidas').mkdir(exist_ok=True)
    for name in ['excecoes_detectadas.csv','amostra_aleatoria_400.csv','resultado_testes.json']:
        shutil.copy2(d/name,base/'saidas'/name)
    print('CONFIRMADO: 500.000 registros, 428 erros sintéticos, conciliação dos totais. Arquivos em saidas/.')
