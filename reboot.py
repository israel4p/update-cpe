from threading import Thread
from paramiko import SSHClient, AutoAddPolicy, ssh_exception


class Reboot(Thread):
    """Reinicia CPE"""

    def __init__(self, ip, usuario, senha):
        Thread.__init__(self)
        self.ip = ip
        self.usuario = usuario
        self.senha = senha

    def run(self):
        """Reinicia CPE"""

        try:
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            ssh.connect(self.ip,
                        timeout=15,
                        username=self.usuario,
                        password=self.senha)
            # Requisitando versão do firmware
            stdin, stdout, stderr = ssh.exec_command("reboot\n")
            print('Reiniciando - %s' % self.ip)
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
