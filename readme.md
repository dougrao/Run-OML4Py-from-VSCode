## Rodando OML4Py diretamente do Visual Studio Code
Este guia apresenta as etapas necessárias para conectar o *Visual Studio Code* diretamente ao `Oracle Machine Learning for Python (OML4Py)`.

O ***OML4Py*** é uma facilidade presente no bancos de `Oracle Database` e `Autonomous Database` e permite o desenvolvimento de modelos de *Machine Learning* diretamente no ambiente de banco de dados e, desta forma, fazer uso do poder de processamento já existente no banco de dados.
Essa é uma abordagem muito interessante em cenários onde todos os dados já estão presentes no ambiente de banco de dados em formato de tabelas ou *views*. Esta é uma situção muito comum em ambientes de *Data Warehouse*, no qual os dados já estão tratados, curados e prontos para consumo pelo time de análise de dados.

#### Sobre o Oracle Machine Learning

O `Oracle Machine Learning - OML` possibilita o desenvolvimento de modelos de *Machine Learnig* *in-database* contando com uma gama de algoritmos para execução paralelizada e fazendo uso de recursos nativos do banco de dados para maximizar escalabilidade, otimizar o uso de memória e alavancar o desenpenho geral das execuções dos modelos.

Para conhecer mais sobre os recursos e facilidades do ***OML*** acesse a documentação [Oracle Machine Learning](https://docs.oracle.com/en/database/oracle/machine-learning/oml4py/1/index.html).

#### Pré Requisitos

O ***OML4Py*** tem compatibilidade apenas com plataformas *Linux 64 bits*.

    - Instância de computação *Linux 64 bits*;
    - Python 3.9.5;
    - Conectividade com internet;
    - Canal de comunicação com banco de dados.

Neste artigo será utilizada uma máquina `Oracle Linux 8 64 bits`.

#### Instalando o Oracle Machine Learning

É possível instalar o *instant client* do `Oracle Machine Learning` de modo a executar comandos utilizando a biblioteca *oml* diretamente do seu *IDE* favorito e seu código ser executado diretamente em seu `Oracle Database` ou `Autonomous Database`.

Siga os passos abaixo para baixar e instalar o ***OML4Py*** em sua máquina *Linux*.

1. O ***OML4Py*** necessita das bibliotecas <span style = "font-family:Courier; font-size: 0.8em;">perl-Env, libffi-devel, openssl, openssl-devel, tk-devel, xz-devel, zlib-devel, bzip2-devel, readline-devel, libuuid-devel</span> e <span style = "font-family:Courier; font-size: 0.8em;">ncurses-devel</span>. Verifique se as mesmas estão presentes.

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

3. Caso esteja trabalhando com `Autonomous Database` realize o *download* do arquivo `wallet` para estabelecer uma conexão segura com o banco de dados.

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