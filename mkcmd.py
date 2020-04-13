from threading import Thread
from paramiko import SSHClient, AutoAddPolicy, ssh_exception


class MkCmd(Thread):
    """Executa comandos MK"""

    def __init__(self, ip, usuario, senha):
        Thread.__init__(self)
        self.ip = ip
        self.usuario = usuario
        self.senha = senha

    def run(self):
        """Comando Mk"""

        try:
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(self.ip,
                        timeout=15,
                        username=self.usuario,
                        password=self.senha,
                        look_for_keys=False,
                        allow_agent=False)
            # cmd1 = "ip dns set allow-remote-requests=no\n"
            # cmd2 = "system package update install\n"
            cmd1 = "system routerboard upgrade\n"
            cmd2 = "system reboot\n"
            stdin, stdout, stderr = ssh.exec_command(cmd1)
            # print('Comando executado - %s' % self.ip)
            stdin, stdout, stderr = ssh.exec_command(cmd2)
            print('Atualizando - %s' % self.ip)
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
