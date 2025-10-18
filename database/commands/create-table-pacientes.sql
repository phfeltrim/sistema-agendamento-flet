-- Criação da tabela de pacientes

CREATE TABLE IF NOT EXISTS pacientes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  cpf VARCHAR(20),
  telefone VARCHAR(20),
  cep VARCHAR(20),
  numero VARCHAR(10),
  complemento VARCHAR(50),
  email VARCHAR(100),
  status BOOLEAN DEFAULT 1,
  user INT,
  data_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  data_modif DATETIME,
  user_modif INT
)
