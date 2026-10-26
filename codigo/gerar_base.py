"""SANEPAR 2025 — GERADOR EXCLUSIVAMENTE SINTÉTICO. Python 3 + numpy.
Não se trata de registros reais, de achados de auditoria, nem de cadastro da SANEPAR.
"""
import csv, json, argparse
from pathlib import Path
import numpy as np

SEED=20251025
# Referência: DFP SANEPAR 2025, Nota 13(b), valores originais em R$ MIL.
# Contagem de registros por categoria é 100% HIPOTÉTICA.
CATEGORIAS=[
 ('Sistemas de Água',230000,8129035,2588194),
 ('Sistemas de Esgoto',225000,8730506,2287135),
 ('Resíduos Sólidos',1000,7577,7577),
 ('Direitos de Uso e Operação de Sistemas',2000,125120,83089),
 ('Direito de Uso em Arrendamento',4000,202115,36694),
 ('Sistemas de Informática em Implantação',5000,120623,0),
 ('Outros Ativos Intangíveis',33000,463439,173399),
]
CAMPOS=['registro_id','categoria_contabil','grupo_projeto_sintetico','tipo_bem_sintetico','data_entrada_operacao','prazo_estimado_meses','custo_bruto_centavos','amortizacao_acumulada_centavos','valor_liquido_registrado_centavos','documento_referencia_sintetico','classificacao_sintetica','observacao']

def repartir_total(total, pesos):
    """Inteiros exatamente conciliados via maior resto, sem replicação artificial de valores."""
    raw=(pesos/pesos.sum())*total
    a=np.floor(raw).astype(np.int64)
    resto=int(total-a.sum())
    if resto: a[np.argpartition(raw-a,-resto)[-resto:]]+=1
    assert int(a.sum())==total
    return a

def gerar(destino):
    destino=Path(destino);destino.mkdir(parents=True,exist_ok=True)
    rng=np.random.default_rng(SEED)
    gabarito=[];saldos=[];contador=0
    with (destino/'base_intangivel_sintetica.csv').open('w',newline='',encoding='utf-8-sig') as out:
        w=csv.writer(out,delimiter=';');w.writerow(CAMPOS)
        for categoria,n,custo_mil,amort_mil in CATEGORIAS:
            # Centavos exatos, controle por classe da Nota 13(b)
            pesos=rng.lognormal(mean=0,sigma=0.9,size=n)
            custo=repartir_total(custo_mil*100000,pesos)
            ratio=amort_mil/custo_mil
            # atribuição proporcional; diferenças de centavos distribuídas exatamente
            amort=repartir_total(amort_mil*100000,custo.astype(float)) if amort_mil else np.zeros(n,dtype=np.int64)
            assert np.all(amort<=custo)
            liquido=custo-amort
            # 180 distorções deliberadas em valores apresentados, SOMENTE no campo líquido registrado
            indices_val=set(rng.choice(n,size=min(n,round(n*0.00036)),replace=False).tolist())
            disponiveis=np.array([i for i in range(n) if i not in indices_val],dtype=np.int32)
            # Não usar flags do gabarito na detecção; classes de falhas sem sobreposição
            sel=rng.choice(disponiveis,size=min(len(disponiveis),round(n*0.0005)),replace=False)
            indices_data=set(map(int,sel[:len(sel)//2]));indices_doc=set(map(int,sel[len(sel)//2:]))
            tipo=rng.choice(['rede','estacao','instalacao','benfeitoria','equipamento','sistema','direito'],size=n)
            anos=rng.integers(1998,2026,size=n);meses=rng.integers(1,13,size=n);dias=rng.integers(1,29,size=n)
            prazo=rng.integers(120,601,size=n)
            for i in range(n):
                contador+=1;ident=f'INT-{contador:06d}'
                dt=f'{anos[i]:04d}-{meses[i]:02d}-{dias[i]:02d}'
                documento=f'DOC-SIM-{contador:06d}'
                registrado=int(liquido[i]);tipo_erro=''
                if i in indices_val:
                    delta=int(rng.integers(100000,10000000)) * (1 if i%2 else -1)
                    registrado+=delta;tipo_erro='LIQUIDO_INCONSISTENTE'
                elif i in indices_data:
                    dt=f'2026-{meses[i]:02d}-{dias[i]:02d}';tipo_erro='DATA_APOS_CORTE'
                elif i in indices_doc:
                    documento='';tipo_erro='DOCUMENTO_AUSENTE'
                classe='IMPLANTACAO' if 'Implantação' in categoria else 'INTANGIVEL'
                w.writerow([ident,categoria,f'PRJ-SIM-{contador//30:06d}',str(tipo[i]),dt,int(prazo[i]),int(custo[i]),int(amort[i]),registrado,documento,classe,'DADO SINTETICO'])
                if tipo_erro:gabarito.append([ident,categoria,tipo_erro, int(registrado-int(liquido[i]))])
            saldos.append({'categoria':categoria,'n':n,'custo_centavos':int(custo.sum()),'amortizacao_centavos':int(amort.sum()),'liquido_correto_centavos':int(liquido.sum())})
    with (destino/'gabarito_erros_inseridos.csv').open('w',newline='',encoding='utf-8-sig') as fh:
        w=csv.writer(fh,delimiter=';');w.writerow(['registro_id','categoria_contabil','erro_inserido','diferenca_centavos']);w.writerows(gabarito)
    (destino/'controle_geracao.json').write_text(json.dumps({'aviso':'BASE TOTALMENTE SINTETICA; NAO REPRESENTA CADASTRO REAL DA SANEPAR','seed':SEED,'registros':contador,'saldos_por_categoria':saldos,'erros_inseridos':len(gabarito),'fonte':'SANEPAR DFP 2025, Nota 13(b), valores em R$ mil'},indent=2,ensure_ascii=False),encoding='utf-8')
    print('GERADOS',contador,'REGISTROS; ERROS',len(gabarito),'TOTAL LÍQUIDO ORIGINAL CENTAVOS',sum(v['liquido_correto_centavos'] for v in saldos))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--destino',default='.');gerar(p.parse_args().destino)
