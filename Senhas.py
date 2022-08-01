import ctypes

# Sistema
from distutils.log import error
import subprocess
import qrcode
import random
from functools import lru_cache
import platform
import os
from qrcode.image.styledpil import StyledPilImage

# Console Interface
import getpass
from time import sleep
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress

sistema = platform.system() 
console = Console()

if sistema == "Windows":
    @lru_cache
    def Scan():
        lista_wifi = subprocess.check_output(['netsh', 'wlan', 'show', 'profile']).decode('utf-8', errors="ignore").split('\n')
        profiles = [i.split(":")[1][1:-1] for i in lista_wifi if "Todos os Perfis de Usurios" in i]
        senha_profiles = []

        with Progress() as progress:
            task = progress.add_task(
                "[green]Processing...", total=len(profiles))
            for i in profiles:
                try:
                    senha = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', f"name={i}", 'KEY=clear']).decode('utf-8', errors="ignore").split('\n')
                    senha = [x.split(":")[1][1:-1] for x in senha if "Contedo da Chave" in x]
                    senha_profiles.append(senha[0])

                except:
                    senha_profiles.append("Não foi encontrada =(")

                progress.update(task, advance=1)

            return profiles, senha_profiles

    def Print(profiles, senha_profiles):
        for i in range(0, len(profiles)):
            console.print(f"\n:computer: [yellow]WIFI[/] = [purple]{profiles[i]}[/] | :key: [yellow]KEY[/] = [green]{senha_profiles[i]}[/]", style="bold")
            sleep(0.2)

    def Search():
        try:
            console.print(subprocess.check_output(['netsh', 'wlan', 'show', 'profile']).decode('utf-8', errors="ignore"), style="bold")
            console.print("\n[yellow]Coloque[/] o [cyan]Nome da Rede Manualmente[/] [red]Aqui[/]: ", style="bold")
            wifi = input()
            dados = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', f"name={wifi}", 'KEY=clear']).decode('utf-8', errors="ignore")
            console.print(dados, style="bold")
            console.print(f"\n[red]{user}[/], deseja [green]Salvar[/] a [cyan]Informações da rede[/] para ler em um [black]Arquivo.txt[/] :floppy_disk::key: ?", style="bold")
            s = Prompt.ask(choices=["S", "N"], default="N")
            s = s.upper()
            if (s == "S"):
                Save(wifi, dados, 1)
        except:
            console.print("\n\n[red]Algo deu Errado [/] :scream:\n", style="bold")

    def Save(wifi, senha, t):
        if not os.path.exists("WIFI"):
            os.makedirs("WIFI")
        if(t == 0):
            with open('WIFI/senhas.txt', 'w') as arquivo:
                print(f"Senhas Salvas no PC\n", file=arquivo)
                for i in range(0, len(wifi)):
                    if(senha[i] != "Não foi encontrada =("):
                        print(f"WIFI = {wifi[i]} | KEY = {senha[i]}", file=arquivo)
                    else:
                        print(f"WIFI = {wifi[i]} | KEY = ", file=arquivo)
                console.print("\n[black]Arquivo[/] [green]Salvo[/] com [green]Sucesso[/] :heart_eyes:", style="bold")
        elif(t == 1):
            with open(f'WIFI/{wifi}.txt', 'w') as arquivo:
                print(f"Dados da Rede {wifi}\n", file=arquivo)
                print(senha, file=arquivo)
                console.print("\n[black]Arquivo[/] [green]Salvo[/] com [green]Sucesso[/] :heart_eyes:", style="bold")
        else:
            print("Sem Função =(")


    def QRCODE(wifi, senha):
        profile = wifi
        profile_senha = senha
        wifi_a = "NULL"
        senha_a = "NULL"
        passe = False
        if not os.path.exists("QRCODE"):
            os.makedirs("QRCODE")
            
        while(passe != True):
            console.print(f"\n[red]{user}[/], [yellow]Coloque[/] o [red]Nome[/] da [black]Rede[/] desejada: [yellow](Coloque os acentos, espaços e todos os caracteres semelhantes ao printado anteriomente)[/]", style="bold")
            wifi = Prompt.ask(default=f"{profile[random.randrange(0, len(profile), 1)]}")
            for i in range(0, len(profile)):
                if profile[i] == wifi:
                    wifi_a = profile[i]
                    senha_a = profile_senha[i]

            if(wifi_a != "NULL"):
                if(os.path.isfile(f"{wifi_a}.png")):
                    os.remove(f"{wifi_a}.png")
                console.print(f"\n[red]{user}[/], qual o [cyan]Tipo de Autenticação da Rede[/] que deseja [yellow]Colocar[/]:", style="bold")
                type = Prompt.ask(choices=["WPA", "WEP", "nopass"], default="WPA")
                console.print(f"\n[red]{user}[/], a rede na qual deseja [yellow]Colocar[/] é [cyan]Escondida[/] ou [red]Não[/]:", style="bold")
                hidden = Prompt.ask(choices=["False", "True"], default="False")
                qr = qrcode.QRCode(version=3, error_correction=qrcode.constants.ERROR_CORRECT_H)
                qr.add_data(f"WIFI:T:{type};S:{wifi_a};P:{senha_a};H:{hidden};;")
                try:
                    img = qr.make_image(image_factory=StyledPilImage, embeded_image_path="imagem/signal.png")
                except:
                    img = qr.make_image()

                img.save(f"QRCODE/{wifi_a}.png")
                console.print("\n[black]Arquivo[/] [green]Salvo[/] com [green]Sucesso[/] :heart_eyes:", style="bold")
                passe = True
            else:
                console.print("\n[red]Você digitou errado, tente novamente[/] :scream:\n", style="bold")
                passe = False



    # Interfaces
    try:
        user = getpass.getuser()
        passed = "S"    
        console.print(f"Olá [red]{user}[/]:busts_in_silhouette: ", style="bold")
        sleep(0.5)
        console.print("[yellow]Bem-Vindo[/] ao Sistema de :mag: [cyan]Encontrar Senhas Salvas[/] :closed_lock_with_key: no seu [black]Computador[/] :computer:", style="bold")
        sleep(0.2)
        console.print(":watch: Aquarde a [green]Barra de Progresso[/] [red]Terminar[/] :watch:\n", style="bold")
        sleep(0.5)

        profiles, senha_profiles = Scan()

        Print(profiles, senha_profiles)

        sleep(0.5)
        console.print(f"\n[red]{user}[/], deseja [green]Salvar[/] as [cyan]Senhas[/] em um [black]Arquivo.txt[/] :floppy_disk::key: ? [yellow](Função Serve para gerar um arquivos com as senhas que acabaste de ver[Caso queira, Responda S])[/]", style="bold")
        s = Prompt.ask(choices=["S", "N"], default="N")
        s = s.upper()
        if (s == "S"):
            Save(profiles, senha_profiles, 0)

        sleep(0.5)
        console.print(f"\n[red]{user}[/], deseja criar um [white]QR[/][black]CODE[/] da [cyan]Senha do Wifi[/] [yellow]Expecifica[/] :computer: ? [yellow](Função Serve só para os dados já cadastrados, [red]sujeito a falhas[/][Caso queira, Responda S])[/]", style="bold")
        q = Prompt.ask(choices=["S", "N"], default="N")
        q = q.upper()
        while(passed != "N"):
            passed = "N"
            if (q == "S"):
                QRCODE(profiles, senha_profiles)
                console.print(f"\n[red]{user}[/], deseja [yellow]Repitir[/]", style="bold")
                passed = Prompt.ask(choices=["S", "N"], default="N")

        passed = "S"

        sleep(0.5)
        console.print(f"\n[red]{user}[/], você achou a [cyan]Senha do Wifi[/] que [yellow]Desejava[/] :computer: ? [yellow](Função Serve também para pegar mais dados da rede[Caso queira, Responda N])[/]", style="bold")
        r = Prompt.ask(choices=["S", "N"], default="S")
        r = r.upper()
        while(passed != "N"):
            passed = "N"
            if (r == "N"):
                Search()
                console.print(f"\n[red]{user}[/], deseja [yellow]Repitir[/]", style="bold")
                passed = Prompt.ask(choices=["S", "N"], default="N")

        sleep(0.2)
        console.print("\n[red]BYE BYE[/] :innocent:", style="bold")
    except:
        console.print("\n\n[red]Algo deu Errado [/] :scream:\n", style="bold")
        console.print(f"[red]{error}[/]")
else:
    console.print("\n\n[red]Está Aplicação só funciona no Windows [/] :scream:\n", style="bold")
    sleep(0.2)
    console.print(f"[red]Está Aplicação não tem suporte para {os} :cold_sweat:[/]\n", style="bold")

