#importando s biblioteca oml
import oml

def main():
    #definição de variáveis
    user = "oml_user" #atualize com o seu usário de OML
    pwd = "oml_password" #atualize com a senha de seu usuário OML
    dsn = "myadb_medium" #atualize com o dns presente no arquivo tnsnames.ora, este arquivo consta no diretório que a wallet foi descompactada
    automl = "myadb_medium_pool" #atualize com o valor de seu automl

    #estabeleça conexão com o seu database
    oml.connect(user=user, password=pwd, dsn=dsn, automl=automl)

    #confirme que a conexão foi estabelecida
    print("Is oml connected? ",oml.isconnected())

    #criação dos dataframes a partir de tabelas presentes no schema SH
    CUSTOMERS = oml.sync(query = 'SELECT CUST_ID, CUST_GENDER, CUST_MARITAL_STATUS, CUST_YEAR_OF_BIRTH, CUST_INCOME_LEVEL, CUST_CREDIT_LIMIT FROM SH.CUSTOMERS')
    SUPP_DEM = oml.sync(query = """SELECT CUST_ID, EDUCATION, AFFINITY_CARD, HOUSEHOLD_SIZE, OCCUPATION, YRS_RESIDENCE, Y_BOX_GAMES FROM SH.SUPPLEMENTARY_DEMOGRAPHICS""")

    #join dos dataframe CUSTOMERS e SUPP_DEM a partir da coluna CUST_ID
    CUST_DF = CUSTOMERS.merge(SUPP_DEM, how = "inner", on = 'CUST_ID',suffixes = ["",""])

    #criando um modelo usando o algoritmo SVM
    try:
        oml.drop(model="ANOMALY_DETECTION_MODEL1")
    except:
            pass

    odm_settings = {'SVMS_OUTLIER_RATE' : '0.01',
                            'SVMS_REGULARIZER' : 'SVMS_REGULARIZER_L1',
                            'SVMS_CONV_TOLERANCE': '0.001'
                            }

    svm_mod = oml.svm("anomaly_detection", **odm_settings)
    svm_mod.fit(CUST_DF, None, model_name = 'ANOMALY_DETECTION_MODEL1', case_id = 'CUST_ID')

    #invocando o modelo e pontuado as anomalias
    RES_DF = svm_mod.predict(CUST_DF, supplemental_cols = CUST_DF, proba = True)

    #exibindo as anomalias - as anomalias são indicadas
    print('Exibindo os 5 casos mais anômalos preditos pelo modelo')
    print(RES_DF[RES_DF['PREDICTION']==0][["PREDICTION","PROBABILITY"] + RES_DF.columns].sort_values('PROBABILITY', ascending = False).head(5))

    #salvando o modelo no datastore
    print('Salvando o modelo no datastore')
    oml.ds.save(objs={'svm_mod':svm_mod},
                name="ds_pymodel", grantable=True, overwrite=True)

    #tornando o modelo publico para todos os usuários
    oml.grant(name="ds_pymodel", typ="datastore", user=None)

    #carregando o modelo na memoria
    print('Recarregando o modelo para a memória')
    oml.ds.load(name="ds_pymodel", objs=["svm_mod"])

    #criando uma nova predição
    RES_DF2 = svm_mod.predict(CUST_DF, supplemental_cols = CUST_DF, proba = True)

    #exibindo os 5 casos mais anômalos
    print('Exibindo os 5 casos mais anômalos preditos pelo modelo recarregado')
    print(RES_DF2[RES_DF2['PREDICTION']==0][["PREDICTION","PROBABILITY"] + RES_DF2.columns].sort_values('PROBABILITY', ascending = False).head(5))

if __name__ == '__main__':
     main()