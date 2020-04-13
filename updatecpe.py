#!/usr/bin/env python3
import argparse
from ubnt import Ubnt
from ubnt import ClientesMk
from reboot import Reboot
from mkcmd import MkCmd

if __name__ == '__main__':
    choices = ['reboot', 'update', 'mkcmd']

    parser = argparse.ArgumentParser(description='Atualização Ubiquiti')

    parser.add_argument(
        'role', choices=choices, action='store',
        help='reiniciar/atualizar/comando'
    )
    # Acesso Mikrotik
    parser.add_argument(
        '--mkip', metavar='IP', action='store', required=True,
        help='IP do concentrador PPPoE'
    )
    parser.add_argument(
        '--mkuser', metavar='USER', action='store', required=True,
        help='Usuário do concentrador PPPoE'
    )
    parser.add_argument(
        '--mkport', metavar='PORT', action='store', required=True,
        help='Porta do concentrador PPPoE'
    )
    parser.add_argument(
        '--mkpasswd', metavar='PASSWORD', action='store', required=True,
        help='Senha do concentrador PPPoE'
    )
    # Acesso Ubiquiti
    parser.add_argument(
        '--cliuser', metavar='USER', action='store', required=True,
        help='Usuário da CPE'
    )
    parser.add_argument(
        '--clipasswd', metavar='PASSWORD', action='store', required=True,
        help='Senha da CPE'
    )

    args = parser.parse_args()

    # Lista IPs conectados no momento
    clientesmk = ClientesMk(args.mkip, args.mkport, args.mkuser, args.mkpasswd)
    lista_ips = clientesmk.mk()

    # Atualiza antena dos clientes
    if args.role == 'update' and lista_ips:
        print('Atualizando...')
        for ip in lista_ips:
            atualizar = Ubnt(ip, args.cliuser, args.clipasswd)
            atualizar.start()

    # Reinicia antena dos clientes
    if args.role == 'reboot' and lista_ips:
        print('Reiniciando...')
        for ip in lista_ips:
            reinicia = Reboot(ip, args.cliuser, args.clipasswd)
            reinicia.start()

    # Executa comando MK
    if args.role == "mkcmd" and lista_ips:
        print("Executando comando")
        for ip in lista_ips:
            cmd = MkCmd(ip, args.cliuser, args.clipasswd)
            cmd.start()
