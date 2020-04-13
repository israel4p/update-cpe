import subprocess
from threading import Thread

from paramiko import AutoAddPolicy, SSHClient, ssh_exception
from scp import SCPClient


class ClientesMk():
    def __init__(self, ip_rb, porta_rb, usuario_rb, senha_rb):
        self.ip_rb = ip_rb
        self.porta_rb = porta_rb
        self.usuario_rb = usuario_rb
        self.senha_rb = senha_rb

    def mk(self):
        try:
            lista_ips = []

            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(
                self.ip_rb,
                port=int(self.porta_rb),
                username=self.usuario_rb,
                password=self.senha_rb,
                allow_agent=False,
                look_for_keys=False)

            stdin, stdout, stderr = ssh.exec_command("/ppp active print\n")
            clientes = stdout.readlines()

            ssh.close()

            # Cria lista de IP
            for cliente in clientes:
                if "pppoe" in cliente:
                    ips = cliente.lstrip().split()
                    if len(ips) >= 7:
                        lista_ips.append(ips[5])

        except ssh_exception.AuthenticationException:
            print('Erro ao acessar o concentrador: Usuário ou senha inválida')
        except ssh_exception.NoValidConnectionsError:
            print('Sem conexão ssh')
        except ConnectionRefusedError:
            print('Permissão negada')

        return lista_ips


class Atualiza():
    """Atualização do firmware Ubiquiti"""

    def __init__(self, ip, usuario, senha, fw=None):
        self.ip = ip
        self.usuario = usuario
        self.senha = senha
        self.fw = fw

    def AtualizaFw(self):
        try:
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(self.ip, username=self.usuario, password=self.senha)
            scp = SCPClient(ssh.get_transport())

            scp.put(self.fw, '/tmp/fwupdate.bin')
            stdin, stdout, stderr = ssh.exec_command('/sbin/fwupdate -m\n')
            print("Firmware atualizado - %s" % self.ip)
            ssh.close()

        except ConnectionResetError:
            ssh.close()
        except ConnectionRefusedError:
            ssh.close()
        except OSError:
            ssh.close()
        except ssh_exception.AuthenticationException:
            ssh.close()
        except ssh_exception.SSHException:
            ssh.close()
        except AttributeError:
            ssh.close()
        except Exception:
            ssh.close()
        except:
            ssh.close()


class Ubnt(Thread):
    """Identifica versão do firmware"""

    def __init__(self, ip, usuario, senha):
        Thread.__init__(self)
        self.ip = ip
        self.usuario = usuario
        self.senha = senha

    def run(self):
        """Faz a conexão e identifica a versão do firmware"""
        try:
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(
                self.ip,
                timeout=15,
                username=self.usuario,
                password=self.senha)
            # Requisitando versão do firmware
            stdin, stdout, stderr = ssh.exec_command("cat /etc/version\n")
            versao = stdout.readlines()
            ssh.close()
        except OSError:
            ssh.close()
        except ConnectionResetError:
            ssh.close()
        except ConnectionRefusedError:
            ssh.close()
        except ssh_exception.AuthenticationException:
            ssh.close()
        except ssh_exception.SSHException:
            ssh.close()
        except AttributeError:
            ssh.close()
        except Exception:
            ssh.close()
        except:
            ssh.close()
        else:
            # Identificação do firmware
            try:
                if "XM" in versao[0]:
                    cmd = "ls | grep XM"
                    fw = subprocess.check_output(
                        cmd, shell=True).decode("utf-8")[:-1]

                    # if versao[0][:-1] not in fw:
                    update = Atualiza(self.ip, self.usuario, self.senha, fw)
                    update.AtualizaFw()
                    # else:
                    #    print("Firmware já está na ultima versão - %s" % (
                    #        self.ip)
                    #    )

                if "XW" in versao[0]:
                    cmd = "ls | grep XW"
                    fw = subprocess.check_output(
                        cmd, shell=True).decode("utf-8")[:-1]

                    # if versao[0][:-1] not in fw:
                    update = Atualiza(self.ip, self.usuario, self.senha, fw)
                    update.AtualizaFw()
                    # else:
                    #    print("Firmware já está na ultima versão - %s" % (
                    #        self.ip)
                    #    )
            except:
                print("CPE não é Ubiquiti")
