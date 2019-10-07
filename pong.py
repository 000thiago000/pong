import os
import time
import signal
import sys

# verifica CTRL + C
def exit(signum, frame):

    #total pacotes
    total = str(up + down)
    
    #porcentagem de perda dos pacotes
    if down == 0:
        perda = 0
    else:
        perda = ((up + down)/down)*100

    #tempo total em ms
    tempo_total = str(int(round((now - program_starts) * 1000)))

    #avg
    avg = str(float("{0:.3f}".format((min + max) / 2)))

    #mdev
    mdev = str(float("{0:.3f}".format((min + max) / (up + down))))

    #print estatisticas
    print ("\n--- " + host + " ping statistics ---\n" 
    + total +" packets transmitted, " + str(up) + " received, " + str(perda) + "% packet loss, time " + tempo_total + "ms\n"
    "rtt min/avg/max/mdev = " + str(min) + "/" + avg + "/" + str(max) + "/" + mdev + " ms")

    #finaliza script
    sys.exit(1)
signal.signal(signal.SIGINT, exit)

#verifica se o host ja foi informado via terminal
if len(sys.argv) > 1:
    host = sys.argv[1]
else:
    host = raw_input("Host:")

#carregar variaveis
up = 0
down = 0
min = 0
max = 0

#carrega o tempo em que inciou o script
program_starts = time.time()

#loop de ping
while True:

    #carrega o tempo do loop
    now = time.time()

    #executa o ping
    result = os.popen("ping -W 1 -c 1 " + host + " | grep 'bytes from '").read()

    #recupera o tempo do ping
    ciclo = (time.time() - now) * 1000

    #defini o tempo do pacote mais rapido enviado
    if min == 0 or min > ciclo:
        min = float("{0:.3f}".format(ciclo))

    #defini o tempo do pacote mais demorado enviado
    if max == 0 or max < ciclo:
        max = float("{0:.3f}".format(ciclo))

    #resultado de ping UP
    if len(result) > 0:
        tempo = time.strftime("%H:%M:%S %d-%m-%Y ", time.localtime())
        up += 1
        print tempo + "- host " + host + " is \033[0;32mok\033[0m - " + result.splitlines()[0]
        time.sleep(1)

    #resultado de ping DOWN
    else:
        tempo = time.strftime("%H:%M:%S %d-%m-%Y ", time.localtime())
        down += 1
        print tempo + "- host " + host + " is \033[0;31mdown\033[0m"