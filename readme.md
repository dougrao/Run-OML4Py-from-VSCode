## Rodando OML4Py diretamente do Visual Studio Code
Este guia apresenta as etapas necessárias para conectar o *Visual Studio Code* diretamente ao `Oracle Machine Learning for Python (OML4Py)`.

O ***OML4Py*** é uma facilidade presente no bancos de `Oracle Database` e `Autonomous Database` e permite o desenvolvimento de modelos de *Machine Learning* diretamente no ambiente de banco de dados e, desta forma, fazer uso do poder de processamento já existente no banco de dados.
Essa é uma abordagem muito interessante em cenários onde todos os dados já estão presentes no ambiente de banco de dados em formato de tabelas ou *views*. Esta é uma situção muito comum em ambientes de *Data Warehouse*, no qual os dados já estão tratados, curados e prontos para consumo pelo time de análise de dados.

#### Sobre o Oracle Machine Learning

O `Oracle Machine Learning - OML` possibilita o desenvolvimento de modelos de *Machine Learnig* *in-database* contando com uma gama de algoritmos para execução paralelizada e fazendo uso de recursos nativos do banco de dados para maximizar escalabilidade, otimizar o uso de memória e alavancar o desenpenho geral das execuções dos modelos.

Para conhecer mais sobre os recursos e facilidades do ***OML*** acesse a documentação [Oracle Machine Learning](https://docs.oracle.com/en/database/oracle/machine-learning/oml4py/1/index.html).

#### Pré Requisitos

O ***OML4Py*** tem compatibilidade apenas com plataformas *Linux 64 bits*. Para utilizar o *client* ***OML4Py*** é preciso:

- Instância de computação *Linux 64 bits*;
- Interpretador *Python 3.9.5*;
- `OML Server` instalado no *database* que será utilizado;
- Usuário no *database* com privilégios de `OML User`;
- Canal de comunicação com o *database*.

Neste artigo será utilizada uma máquina `Oracle Linux 8 64 bits`. A seguir, serão explorados os passos necessário para preparar, instalar e configurar o *client* ***OML4Py***.

#### Opcional - Instalando e Configurando o *pyenv*

O ***OML4Py*** necessita de um ambiente contendo *Python 3.9.5* em execução. Caso sua máquina não possua essa versão expecífica do *Python*, o *pyenv* é uma excelente ferramenta para instalar novas versões do *Python* sem entrar em conflito com a versão corrente já instalada. Todos os interpretadores instalados usando o *pyenv* são automaticamente integrados ao *VSCode*.

Abaixo seguem os passos necessários para instalação em máquina `Oracle Linux 8`.

1. Abra um terminal e execute os comandos a seguir:

        sudo dnf groupinstall -y "Development Tools"
        sudo dnf install -y zlib zlib-devel bzip2-devel openssl-devel sqlite-devel readline-devel

2. Execute o comando de instação do *pyenv*.

        curl https://pyenv.run | bash

3. Atualize seu *shell environment*. Acesse o arquivo <span style = "font-family:Courier; font-size: 0.8em;">.bashrc</span> incluindo as linhas abaixo:

        # PYENV
        export PYENV_ROOT="$HOME/.pyenv"
        export PATH="$PYENV_ROOT/bin:$PATH"

        # PYENV Auto-completions. This should be towards the end of the file.
        eval "$(pyenv init -)"

4. Reinicie o *shell environment*.

        exec "$SHELL"

5. Confirme a versão do *pyenv*.

        pyenv --version

6. Execute o comando abaixo para instalação do *Python 3.9.5*.

        pyenv install 3.9.5

7. Para ativar no terminal a versão específica instalada use o comando abaixo:

        pyenv shell 3.9.5

8. Confirme que a versão instalada está ativada iniciando uma sessão *Python* no terminal.

        python

        Python 3.9.5 (default, Sep  2 2023, 02:29:33)
        [GCC 8.5.0 20210514 (Red Hat 8.5.0-18.0.2)] on linux
        Type "help", "copyright", "credits" or "license" for more information.
        >>>

#### Instalando o Oracle Machine Learning

É possível instalar o *instant client* do `Oracle Machine Learning` de modo a executar comandos utilizando a biblioteca *oml* diretamente do seu *IDE* favorito e seu código ser executado diretamente em seu `Oracle Database` ou `Autonomous Database`.

Siga os passos abaixo para baixar e instalar o ***OML4Py*** em sua máquina *Linux*.

1. O ***OML4Py*** necessita das bibliotecas <span style = "font-family:Courier; font-size: 0.8em;">perl-Env, libffi-devel, openssl, openssl-devel, tk-devel, xz-devel, zlib-devel, bzip2-devel, readline-devel, libuuid-devel</span> e <span style = "font-family:Courier; font-size: 0.8em;">ncurses-devel</span>. No terminal, verifique se as mesmas estão presentes.

        rpm -qa perl-Env
        rpm -qa libffi-devel
        rpm -qa openssl 
        rpm -qa openssl-devel
        rpm -qa tk-devel
        rpm -qa xz-devel
        rpm -qa zlib-devel
        rpm -qa bzip2-devel
        rpm -qa readline-devel
        rpm -qa libuuid-devel
        rpm -qa ncurses-devel

    Caso não haja nenhum retorno, as mesmas podem ser instaladas via o comando abaixo:

        sudo yum install perl-Env libffi-devel openssl openssl-devel tk-devel xz-devel zlib-devel bzip2-devel readline-devel libuuid-devel ncurses-devel

2. Instale o `Oracle Instante Client` de acordo com a versão de seu `Oracle Database` ou `Autonomous Database`. Você pode conferir a lista de *instant clients* acessanro [Oracle Instant Client Downloads](https://www.oracle.com/technetwork/database/database-technologies/instant-client/downloads/index.html).

    Neste guia será baixo o *instant client 19C* compatível com `Autonomous Database`. Caso você possua acesso *root* em sua máquina e possa instalar arquivos *RPM* execute os comandos abaixo:

        wget https://download.oracle.com/otn_software/linux/instantclient/1914000/oracle-instantclient19.14-basic-19.14.0.0.0-1.x86_64.rpm

        rpm -ivh oracle-instantclient19.14-basic-19.14.0.0.0-1.x86_64.rpm

        export LD_LIBRARY_PATH=/usr/lib/oracle/19.14/client64/lib:$LD_LIBRARY_PATH

    Caso você não possua acesso *root* a máquina é possível instalar utilizando o arquivo *.zip* com os comandos abaixo:

        mkdir $Home/oracle

        cd $Home/oracle

        wget https://download.oracle.com/otn_software/linux/instantclient/1914000/instantclient-basic-linux.x64-19.14.0.0.0dbru.zip

        unzip instantclient-basic-linux.x64-19.14.0.0.0dbru.zip

        export LD_LIBRARY_PATH=/home/opc/oracle/instantclient_19_4:$LD_LIBRARY_PATH

3. Caso esteja trabalhando com `Autonomous Database` realize o *download* do arquivo `wallet` para estabelecer uma conexão segura com o banco de dados. Se não estiver utilizando `Autonomous Database` siga para o passo 7.

    1. Acesse o console da nuvem `Oracle` - `OCI` utilizando suas credenciais de acesso.
    2. Expanda o menu de serviços e navegue até `Oracle Database`.

        ![Menu_Console](/images/console-database.png)
    3. Selecione sua versão de `Autonomous Database`.

        ![Select_Autonomoius](/images/select-autonomous.png)
    4. Dentro de seu compartimento de trabalho, selecione sua instância de `Autonomous Database`.

        ![Select_Autonomous_2](/images/select-autonomous2.png)
    5. Na tela de detalhes do `Autonomous Database` clique no botão *Database connection*.

        ![Autonomous_details](/images/details-autonomous.png)
    6. Uma janela de diálogo será exibida. Clique no botão *Download wallet*.

        ![Download_wallet](/images/donwload-wallet.png)
    7. Uma nova janela será exibida. Digite uma senha para a *wallet* e em seguida clique no botão *Download*.

        ![Download_wallet_2](/images/wallet-donwload-password.png)

4. Descompacte o arquivo *.zip* em um diretório ou crie um novo diretório seguindo os passos a seguir:

        mkdir -p mywalletdir

        unzip Wallet.name.zip -d mywalletdir

        cd mywalletdir/

5. Ao descompactar a *wallet* você terá os seguintes arquivos: <span style = "font-family:Courier; font-size: 0.8em;">README, ewallet.p12, ojdbc.properties, tnsnames.ora, cwallet.sso, keystore.jks, sqlnet.ora, truststore.jks</span>. Acesse o arquivo <span style = "font-family:Courier; font-size: 0.8em;">sqlnet.ora</span> e o atualize com o *path* do diretório ao qual a *wallet* foi descompactada. Caso você esteja utilizando algum *proxy* você deve configurar a variável <span style = "font-family:Courier; font-size: 0.8em;">SQLNET.USE_HTTPS_PROXY</span> com valor *on*.

        WALLET_LOCATION = (SOURCE = (METHOD = file) (METHOD_DATA = (DIRECTORY="mywalletdir")))
        SSL_SERVER_DN_MATCH=yes
        SQLNET.USE_HTTPS_PROXY=on

6. Adicione a variável de ambiente <span style = "font-family:Courier; font-size: 0.8em;">TNS_ADMIN</span> com o valor do *path* do diretório em que a *wallet* foi descompactada.

        export TNS_ADMIN=mywalletdir

7. A seguir, instale as bibliotecas necessárias para o funcionamento do ***OML4Py***.

        pip3.9 install pandas==1.3.4

        pip3.9 install scipy==1.7.3

        pip3.9 install matplotlib==3.3.3

        pip3.9 install cx_Oracle==8.1.0

        pip3.9 install threadpoolctl==2.1.0

        pip3.9 install joblib==0.14.0

        pip3.9 install scikit-learn==1.0.1 --no-deps

        pip3.9 uninstall numpy

        pip3.9 install numpy==1.21.5

8. Faça o *download* do instalar do ***OML4Py*** clicando [aqui](https://www.oracle.com/technetwork/database/database-technologies/python/machine-learning-for-python/downloads/index.html). Selecione a opção de *Client* compatível com sua versão de *database*.

9. Realize a descompactação do arquivo *.zip* e, em seguida, processa com o comando de instalação do ***OML4Py***.

        unzip oml4py-client-linux-x86_64-1.0.zip

        perl -Iclient client/client.pl

10. Inicie um sessão *Python* no teminal e importe a biblioteca *oml*.

        $ python3
        
        import oml

#### Estabelecendo conexão do *client* *OML4Py* com o *database*

Após cumprir as etapas de instalação do ***OML4Py*** listadas acima, a biblioteca *oml* já estará disponível para uso no *VSCode*.

Caso não tenho o *plugin* *Python* instalado em seu *VSCode*, prossiga com a instalação do *plugin* seguindo todas as etapas descritas [aqui](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

Para selecionar interpretadores no *VSCode* primeiro é necessário ativar um *workspace*. Isso é possível de dois modos:

* Pela barra de menu execute <span style = "font-family:Courier; font-size: 0.8em;">File > Open Folder</span> e selecione um diretório de sua escolha.

* Utilizando o terminal nativo do *VSCode*:

        mkdir oml_project
        cd oml_project
        code .

Siga as etapas a seguir para selecionar o interpretador *Python 3.9.5* e estabelecer conexão com seu *database*.

1. Pressione <span style = "font-family:Courier; font-size: 0.8em;">Ctrl+Shift+P</spam>.

2. Digite *Python* e selecione a opção <span style = "font-family:Courier; font-size: 0.8em;">Python: Select Interpreter</span>.

3. Selecione a opção <span style = "font-family:Courier; font-size: 0.8em;">Python 3.9.5 64-bit ('3.9.5').

4. Precssione <span style = "font-family:Courier; font-size: 0.8em;">Ctrl+N</spam> para criar um novo arquivo em branco.

5. Selecione qual a liguagem do novo arquivo clicando em <span style = "font-family:Courier; font-size: 0.8em;">Select Language</span>.

6. Busque por *Python* na barra de busca.

7. No novo arquivo, insira os comandos listados abaixo ajustando-os para as informações do seu ambiente.

        # importando a biblioteca oml
        import oml

        #definição de variáveis
        user = "oml_user" #atualize com o seu usário de OML
        pwd = "oml_password" #atualize com a senha de seu usuário OML
        dsn = "myadb_medium" #atualize com o dns presente no arquivo tnsnames.ora, este arquivo consta no diretório que a wallet foi descompactada
        automl = "myadb_medium_pool" #atualize com o valor de seu automl. Pode-se utilizar o mesmo valor do dsn

        #estabeleça conexão com o seu database
        oml.connect(user=user, password=pwd, dsn=dsn, automl=automl)

        #confirme que a conexão foi estabelecida
        print(oml.isconnected())

8. Salve o arquivo, clique no botão em formato de *play* com título de <span style = "font-family:Courier; font-size: 0.8em;">Run Python File</span> para realizar a execução do arquivo. Caso as informações de conexão estejam corretas, será retornado *True* no terminal.