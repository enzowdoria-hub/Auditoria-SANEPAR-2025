"""Testes cegos: NÃO consulta o gabarito para detectar exceções."""
import csv,json,argparse,random,collections
from pathlib import Path

def testar(destino):
 d=Path(destino);c=collections.Counter();saldos=collections.defaultdict(lambda:[0,0,0,0]);amostra=[];excecoes=[];ids=set();rng=random.Random(20251025)
 with (d/'base_intangivel_sintetica.csv').open(encoding='utf-8-sig',newline='') as fh:
  for i,r in enumerate(csv.DictReader(fh,delimiter=';'),start=1):
   identificador=r['registro_id'];cat=r['categoria_contabil'];custo=int(r['custo_bruto_centavos']);amort=int(r['amortizacao_acumulada_centavos']);liquido=int(r['valor_liquido_registrado_centavos']);esperado=custo-amort
   s=saldos[cat];s[0]+=1;s[1]+=custo;s[2]+=amort;s[3]+=liquido
   erros=[]
   if identificador in ids:erros.append('ID_DUPLICADO')
   ids.add(identificador)
   if liquido!=esperado:erros.append('LIQUIDO_INCONSISTENTE')
   if r['data_entrada_operacao']>'2025-12-31':erros.append('DATA_APOS_CORTE')
   if not r['documento_referencia_sintetico'].strip():erros.append('DOCUMENTO_AUSENTE')
   if custo<0 or amort<0 or amort>custo:erros.append('VALORES_INVALIDOS')
   if erros:
    for erro in erros:c[erro]+=1;excecoes.append([identificador,cat,erro,liquido-esperado])
   # Amostra aleatória simples (reservoir), 400 unidades, reprodutível (PT 530)
   if i<=400:amostra.append([identificador,cat,liquido,','.join(erros)])
   else:
    j=rng.randrange(i)
    if j<400:amostra[j]=[identificador,cat,liquido,','.join(erros)]
 with (d/'excecoes_detectadas.csv').open('w',newline='',encoding='utf-8-sig') as fh:
  w=csv.writer(fh,delimiter=';');w.writerow(['registro_id','categoria','tipo_excecao','diferenca_centavos']);w.writerows(excecoes)
 with (d/'amostra_aleatoria_400.csv').open('w',newline='',encoding='utf-8-sig') as fh:
  w=csv.writer(fh,delimiter=';');w.writerow(['registro_id','categoria','valor_liquido_registrado_centavos','excecoes']);w.writerows(sorted(amostra))
 referencia={x['categoria']:x for x in json.loads((d/'controle_geracao.json').read_text(encoding='utf-8'))['saldos_por_categoria']}
 rel=[]
 for cat,(n,custo,amort,liquido) in saldos.items():
  ref=referencia[cat]
  rel.append({'categoria':cat,'quantidade':n,'custo_centavos':custo,'amortizacao_centavos':amort,'valor_liquido_registrado_centavos':liquido,'valor_liquido_esperado_centavos':custo-amort,'diferenca_registrado_menos_esperado_centavos':liquido-(custo-amort),'custo_confere_DFP':custo==ref['custo_centavos'],'amortizacao_confere_DFP':amort==ref['amortizacao_centavos']})
 gabarito={(r['registro_id'],r['erro_inserido']) for r in csv.DictReader((d/'gabarito_erros_inseridos.csv').open(encoding='utf-8-sig'),delimiter=';')}
 detectado={(x[0],x[2]) for x in excecoes}
 resumo={'registros':sum(x['quantidade'] for x in rel),'n_amostra':len(amostra),'quantidades_excecoes':dict(c),'excecoes_inseridas':len(gabarito),'excecoes_detectadas':len(detectado),'verdadeiros_positivos':len(gabarito&detectado),'falsos_positivos':len(detectado-gabarito),'falsos_negativos':len(gabarito-detectado),'categorias':rel,'custo_total_centavos':sum(x['custo_centavos'] for x in rel),'amort_total_centavos':sum(x['amortizacao_centavos'] for x in rel),'liquido_esperado_centavos':sum(x['valor_liquido_esperado_centavos'] for x in rel),'liquido_registrado_centavos':sum(x['valor_liquido_registrado_centavos'] for x in rel),'limites':'Testes documentais, datas e recálculo exclusivos da população fabricada; não atestam bens reais nem auditoria independente. Amostra de 400 somente exploratória, sem desenho de tolerância ou projeção estatística.'}
 (d/'resultado_testes.json').write_text(json.dumps(resumo,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in resumo.items() if k!='categorias'},ensure_ascii=False,indent=2));return resumo
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--destino',default='.');testar(p.parse_args().destino)
