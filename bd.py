import cx_Oracle
import vglobal
cx_Oracle.init_oracle_client(lib_dir=r"C:\conec\instantclient_21_10")

class conexao():
    @staticmethod
    def conectar():
        db = conexao = cx_Oracle.connect(vglobal.user, vglobal.senha,
                                         vglobal.host)

        return db

   