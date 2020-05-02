from pexpect import pxssh 
import getpass
import pexpect
import sys 
## comando para exportar a base de dados : curl -X GET -H "Accept:application/x-trig" "http://localhost:7200/repositories/cinema2020/statements?infer=false" > export.rdf .
## enviar o ficheiro de instalação do graph db para a máquina
## criar a pasta graphdb-import na nossa machine
## fazer scp do ficheiro para a nossa machine scp onze@a... file destiny
## instalar o graphDB
## correr o instalador : sudo dpkg -i
## criar a config.ttl na máquina :
#       1 - ir para a pasta GraphDB Free.app/Contents/Java/bin
#       2 - copiar o ficheiro config.ttl para a pasta
## criar o repositorio : ./loadrdf -c config.ttl -m parallel /Users/macz/graphdb-import/output.ttl
## dar start no serviço : ./ Contents/Java/bin/ graphdb
## comando para importar a base de dados :

hostname = '45.76.32.59'
username = 'onze'
f = open('passwords.txt')
passwords = f.readlines()
password = passwords[0] 

if ( len(sys.argv)>2 ):
    try:
        ## exportar a base de dados local
        print(" ## A exportar a base de dados local do GraphDB ##")
        pexpect.run('curl -X GET -H "Accept:application/x-trig" "http://localhost:7200/repositories/cinema2020/statements?infer=false" > export.trig')
        
        ## Enviar o ficheiro de exportação do graphDB
        print(" ## A enviar o ficheiro de exportação do GraphDB ##")
        child = pexpect.spawn ('scp /Users/macz/export.trig  onze@45.76.32.59:/home/onze/GraphDB/graphdb-free-9.2.0/bin')
        value = username + '@'+hostname + '\'s password:'
        child.expect (value)
        child.sendline(password)
        child.expect(pexpect.EOF, timeout=50)

        ## enviar o ficheiro de instalação do graph db
        print(" ## A copiar o ficheiro de instalação do graphDB ##")
        child = pexpect.spawn ('scp -r files/graphdb-free-9.2.0  onze@45.76.32.59:/home/onze/GraphDB')
        value = username + '@'+hostname + '\'s password:'
        child.expect (value)
        child.sendline(password)
        child.expect(pexpect.EOF, timeout=50)
        
        ## enviar o ficheiro de configuração do repositorio
        print(" ## A enviar o ficheiro de configuração do repositorio ##")
        child2 = pexpect.spawn ('scp files/config.ttl onze@45.76.32.59:/home/onze/GraphDB/graphdb-free-9.2.0/bin')
        value = username + '@'+hostname + '\'s password:'
        child.expect (value)
        child.sendline(password)
        child.expect(pexpect.EOF, timeout=50)


        ## Ligar por ssh para executar os comandos de instalação 
        s = pxssh.pxssh()
        s.login(hostname, username, password)

        ## criação de repopositório na base de dados
        
        print("## Criação do repositório  ##")
        s.sendline('cd /home/onze/GraphDB/graphdb-free-9.2.0/bin')
        s.prompt()
        #print(s.before)

        ## Importação dos dados
        print(" ## Importação e criação da base de dados  ##")
        s.sendline('./loadrdf -c config.ttl -m parallel -f export.trig')
        s.prompt()
        #print("\n")
        #print(s.before)

        ## comando so para importação ./loadrdf -c config.ttl -m parallel -f export.trig

        ## Iniciar o serviço 
        print(" ## Iniciar o GraphDB  ## ")
        s.sendline(' ./graphdb &')
        s.prompt()
        # print(s.before)

        s.logout()

    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(e)
else:
    try:
        ## exportar a base de dados local
        print(" ## A exportar a base de dados local do GraphDB ##")
        pexpect.run('curl -X GET -H "Accept:application/x-trig" "http://localhost:7200/repositories/repo_test/statements?infer=false" > export.trig')
        
        print(" ## A enviar o ficheiro de testes ##") 
        child = pexpect.spawn ('scp /Users/macz/export.trig onze@45.76.32.59://home/onze')
        value = username + '@'+hostname + '\'s password:'
        child.expect (value)
        child.sendline(password)
        child.expect(pexpect.EOF, timeout=50)

        ## Enviar o ficheiro de exportação do graphDB
        print(" ## A enviar o ficheiro de exportação do GraphDB ##")
        child = pexpect.spawn ('scp  /Users/macz/export.trig  onze@45.76.32.59:/home/onze/GraphDB/graphdb-free-9.2.0/bin')
        value = username + '@'+hostname + '\'s password:'
        child.expect (value)
        child.sendline(password)
        child.expect(pexpect.EOF, timeout=50)

        ## Ligar por ssh para executar os comandos de instalação 
        s = pxssh.pxssh()
        s.login(hostname, username, password)

        s.sendline('cd /home/onze/GraphDB/graphdb-free-9.2.0/bin')
        s.prompt()

        ## Importação dos dados
        print(" ## Importação e criação da base de dados  ##")
        s.sendline('./loadrdf -c config.ttl -m parallel -f export.trig')
        s.prompt()

        ## Iniciar o serviço 
        print(" ## Iniciar o GraphDB  ## ")
        s.sendline(' ./graphdb &')
        s.prompt()
        s.logout()
        # print(s.before)

    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(e)