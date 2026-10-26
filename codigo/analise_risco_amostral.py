"""Estudo didático do risco de não detectar uma exceção rara, em amostragem aleatória sem reposição.
Não é procedimento de auditoria realizado na SANEPAR.
"""
import math
import csv
from pathlib import Path

N=500_000
K=428
n=400
# P(X=0) exata hipergeométrica: combinações(N-K,n)/combinações(N,n)
prob_zero=math.exp(sum(math.log1p(-K/(N-i)) for i in range(n)))
# mínimo n para prob detectar >=95%; relação recursiva evita fatorial gigante
p0=1.0; n95=0
while p0 > 0.05:
    p0 *= (N-K-n95)/(N-n95)
    n95 += 1
p=Path(__file__).resolve().parent.parent/'saidas'/'amostra_aleatoria_400.csv'
if not p.exists(): p=Path(__file__).resolve().parent/'amostra_aleatoria_400.csv'
with p.open(encoding='utf-8-sig',newline='') as f:
    lines=list(csv.DictReader(f,delimiter=';'))
found=sum(bool(row['excecoes'].strip()) for row in lines)
assert len(lines)==n
print('UNIVERSO SINTÉTICO:',N)
print('EXCEÇÕES PREVIAMENTE INSERIDAS:',K)
print('AMOSTRA:',n)
print('EXCEÇÕES EFETIVAMENTE NA AMOSTRA:',found)
print('FREQUÊNCIA REAL CONTROLADA:',f'{100*K/N:.4f}%')
print('PROB. DE AMOSTRA COM ZERO EXCEÇÕES:',f'{100*prob_zero:.4f}%')
print('PROB. DE ENCONTRAR AO MENOS UMA:',f'{100*(1-prob_zero):.4f}%')
print('TAMANHO PARA >=95% DE DETECÇÃO DE AO MENOS UMA, SE A TAXA CONTROLADA FOR CONHECIDA:',n95)
print('LIMITE: não é uma amostragem monetária dimensionada por materialidade/tolerância.')
