# -*- coding: utf-8 -*-
"""
Spyder Editor

Este é um arquivo de script temporário.
"""
import pandas as pd
import pulp

dados_fabrica = pd.read_csv('dados.csv')
otimizar_lucro_fabrica = pulp.LpProblem("Otimizar Lucro Fabrica", pulp.LpMaximize)
"""
horasDisponiveis = B
tempoDeTroca = T
custoMensalProducao = F
numProdutos = Conjunto de produdos
numMateriaPrima = Conjunto de materia prima
custoVenda = valor da venda do produto (R)
custoProducao = custo de produção de um produto (b)
custoLote = custo de compra do lote (C)
materiaPrimaLote = quantidade de materia prima em um lote (L)
"""
#RECOLHE OS DADOS DE ENTRADA DO ARQUIVO CSV
numProdutos = int(dados_fabrica.numProdutos.get_value(0))
numMateriaPrima = int(dados_fabrica.numMateriaPrima.get_value(0))
horasDisponiveis = dados_fabrica.horasDisponiveis.get_value(0)
tempoDeTroca = dados_fabrica.tempoDeTroca.get_value(0)
custoMensalProducao = dados_fabrica.custoMensalProducao.get_value(0)
custoVenda = dados_fabrica.custoVenda.tolist()
DMIN = dados_fabrica.DMIN.tolist()
DMAX = dados_fabrica.DMAX.tolist()
custoProducao = dados_fabrica.custoProducao.tolist()
custoLote = dados_fabrica.custoLote.dropna().tolist()
materiaPrimaLote = dados_fabrica.materiaPrimaLote.dropna().tolist()


materiaPrimaProduto = []
for i in range(1, numMateriaPrima+1):
    materiaPrimaProduto.append(dados_fabrica['MAT'+str(i)].tolist())


#DEFINIÇÃO DE VARIAVEIS
w = []
Q = []
Y = []

#INICIALIZA AS VARIÁVEIS NO PULP
for i in range(numProdutos):
    w.append(pulp.LpVariable('w'+str(i), lowBound=0, upBound=1, cat='Binary', e=None))
for i in range(numProdutos):
    Q.append(pulp.LpVariable('Q'+str(i), lowBound=0, cat='Integer', e=None))
for j in range(numMateriaPrima):
    Y.append(pulp.LpVariable('Y'+str(j), lowBound=0, cat='Integer', e=None))
z = pulp.LpVariable('z', lowBound=0, upBound=1, cat='Binary', e=None)

# FUNÇÃO OBJETIVO
otimizar_lucro_fabrica += pulp.lpSum([(custoVenda[i]*Q[i]) for i in range(numProdutos)]) + (custoMensalProducao*z + pulp.lpSum([(custoLote[j]*Y[j]) for j in range(numMateriaPrima)])) * -1, "Z"

#RESTRIÇÕES
hr = (horasDisponiveis*z)
termo = pulp.lpSum([w[i] for i in range(numProdutos)])
otimizar_lucro_fabrica += pulp.lpSum([(custoProducao[i]*Q[i]) for i in range(numProdutos)]) + (termo - 1)*tempoDeTroca <= hr,""
for i in range(numProdutos):
    otimizar_lucro_fabrica += DMIN[i]*w[i] <= Q[i], ""
    otimizar_lucro_fabrica += DMAX[i]*w[i] >= Q[i],""
for j in range(numMateriaPrima):
    #print(pulp.lpSum([(materiaPrimaProduto[j][i]*Q[i]) for i in range(numProdutos)]) <= materiaPrimaLote[j]*Y[j])
    otimizar_lucro_fabrica += pulp.lpSum([(materiaPrimaProduto[j][i]*Q[i]) for i in range(numProdutos)]) <= materiaPrimaLote[j]*Y[j],""


otimizar_lucro_fabrica.writeLP('fabrica.lp')

#INICIA O SOLVER

while True:
    otimizar_lucro_fabrica.solve(pulp.GLPK())
    #EXIBE O ESTADO DA SOLUÇÃO NA TELA
    print("Status:", pulp.LpStatus[otimizar_lucro_fabrica.status])
    #EXIBE A SOLUÇÃO SE O VALOR OTIMO FOR ENCONTRADO
    if pulp.LpStatus[otimizar_lucro_fabrica.status] == "Optimal":
        print("SOLUÇÃO OTIMA ENCONTRADA")
        for variable in otimizar_lucro_fabrica.variables():
            print("{} = {}".format(variable.name, variable.varValue))
        print('Custo total = ' + str(pulp.value(otimizar_lucro_fabrica.objective)))
        break
    else:
        print("SOLUCAO OTIMA NAO ENCONTRADA")
        for variable in otimizar_lucro_fabrica.variables():
            print("{} = {}".format(variable.name, variable.varValue))










