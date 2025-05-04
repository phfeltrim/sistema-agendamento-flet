class Paciente:
    def __init__(self, name, cpf, telefone, cep, number, complement, email, status, user, id=None):
        self.id = id
        self.name = name
        self.cpf = cpf
        self.telefone = telefone
        self.cep = cep
        self.number = number
        self.complement = complement
        self.email = email
        self.status = status
        self.user = user
