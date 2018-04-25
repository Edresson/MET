# MET

Software para maquina de ensaio de tração e compressão:

veja detalhes no artigo: Em breve


Descrição dos arquivos:

O arquivo “Pinagem-Descricao.txt”  possui uma breve descrição dos pinos conectados no Raspberry Pi 3.

O arquivo “IP-Raspberry.txt” possui o IP do Raspberry como ele é um servidor, onde tratará de todas as comunicações feitas através entre ele e o notebook, é essencial que o mesmo possua um IP fixo, se outro IP tiver que ser usado para ele é necessário apenas excluir o atual e colocar o novo IP.

O arquivo “MET_Logs.log” é utilizado para fazer log de algumas coisas importantes como a comunicação, se o Programa não abrir você deve consultar esse arquivo para saber qual pode ser o problema.


O arquivo “conf_celulas.txt” possui a configuração de todas as celulas de cargas cadastras no software.


O arquivo “Fator_Calibracao.txt” possui o Fator de calibração da celula de carga atual escolhida para os testes.

Todos os arquivos acima são muito importantes, portanto não exclua nenhum.

A pasta “Ensaios” possui todos os ensaios realizados na maquina, e um arquivo chamado Ensaio_Atual.pdf dentro desta pasta é o ultimo ensaio realizado na maquina, para facilitar a busca do mesmo. O Ensaios são divididos em pastas seguindo o ano,mes,dia e o nome do pdf é formado pela  hora do teste. O Arquivo save.txt dentro do diretorio do teste refere-se a uma especie de backup de todo o teste desta forma é  possível continuar um teste antigo pela função “Browser Ensaio” disponibilizada na Interface.
