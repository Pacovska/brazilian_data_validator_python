from validate_docbr import CPF, CNPJ
from datetime import datetime, timedelta
import re
import requests

class Documento:

    @staticmethod
    def cria_documento(documento):
        if len(documento) == 11:
            return DocCpf(documento)
        elif len(documento) == 14:
            return DocCnpj(documento)
        else:
            raise ValueError("Quantidade de dígitos incorreta!")



class DocCpf:
    
    def __init__(self, documento):
        if self.valida(documento):
            self.cpf = documento
        else:
            raise ValueError("Cpf inválido!")

    def __str__(self):
        return self.format()

    def valida(self, documento):
        validador = CPF()
        return validador.validate(documento)

    def format(self):
      mascara = CPF()
      return mascara.mask(self.cpf)


class DocCnpj:

    def __init__(self, documento):
        if self.valida(documento):
            self.cnpj = documento
        else:
            raise ValueError("Cnpj inválido!")

    def __str__(self):
        return self.format()

    def valida(self, documento):
        mascara = CNPJ()
        return mascara.validate(documento)

    def format(self):
        mascara = CNPJ()
        return mascara.mask(self.cnpj)


class DocPhone:

    def __init__(self,phone):
        if self.valida_phone(phone):
            self.numero = phone
        else:
            raise ValueError("Número incorreto!")

    def __str__(self):
        return self.format_numero()

    def valida_phone(self,phone):
        padrao = "([0-9]{2,3})?([0-9]{2})([0-9]{4,5})([0-9]{4})"
        resposta = re.findall(padrao,phone)
        if resposta:
            return True
        else:
            return False

    def format_numero(self):
        padrao = "([0-9]{2,3})?([0-9]{2})([0-9]{4,5})([0-9]{4})"
        resposta = re.search(padrao,self.numero)
        numero_formatado = "+{}({}){}-{}".format(
            resposta.group(1),
            resposta.group(2),
            resposta.group(3),
            resposta.group(4)
        )
        return numero_formatado

class DocDate:
    
    def __init__(self):
        self.cadastro = datetime.today()

    def __str__(self) -> str:
        return self.format_date()

    def week(self):
        weekday = [
            "Segunda", "Terça", "Quarta", "Quinta",
            "Sexta", "Sabado", "Domingo"
        ]
        week = self.cadastro.weekday()
        return weekday[week]

    def day(self):
        dia_cadastro = self.cadastro.day
        return dia_cadastro
    
    def month(self):
        meses_do_ano = [
            "Janeiro", "Fevereiro", "Março",
            "Abril", "Maio", "Junho", "Agosto",
            "Setembro", "Outubro",
            "Novembro", "Dezembro"
        ]
        mes_cadastro = self.cadastro.month
        return meses_do_ano[mes_cadastro - 1]

    def year(self):
        ano_cadastro = self.cadastro.year
        return ano_cadastro

    def format_date(self):
        date_format = self.cadastro.strftime("%d/%m/%Y %H:%M")
        return date_format

    def tempo_cadastro(self):
        tempo_cadastro = datetime.today()  - self.cadastro
        return tempo_cadastro

class DocCep:

    def __init__(self, cep):
        cep = str(cep)
        if self.validar_cep(cep):
            self.cep = cep
        else:
            raise ValueError("CEP Invalido!!")
        
    def __str__(self):
        return self.format_cep()

    def validar_cep(self, cep):
        if len(cep) == 8:
            return True
        else: 
            return False
    
    def format_cep(self):
        return "{}-{}".format(self.cep[:5],self.cep[5:])
        
    def acessa_via_cep(self):
        url = "https://viacep.com.br/ws/{}/json/".format(self.cep)
        r = requests.get(url)
        dados = r.json()
        return(
            dados['bairro'],
            dados['localidade'],
            dados['uf']
        )

date = DocDate()
print(date)