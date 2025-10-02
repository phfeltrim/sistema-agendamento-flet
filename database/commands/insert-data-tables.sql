-- Seleciona o banco de dados correto para garantir que os comandos sejam executados no lugar certo.
USE `agendamento`;

-- Remove dados existentes para evitar duplicatas ao executar o script várias vezes.
-- A ordem é importante para respeitar as chaves estrangeiras (sessoes -> pacientes).
DELETE FROM `sessoes`;
DELETE FROM `pacientes`;
DELETE FROM `usuarios`;
DELETE FROM `configuracoes`;


-- =============================================
-- INSERIR DADOS NA TABELA 'usuarios'
-- =============================================
-- A senha aqui é 'admin123', já convertida para o formato bcrypt.
INSERT INTO `usuarios` (`id`, `nome`, `email`, `senha`, `created_at`) 
VALUES
(1, 'Administrador', 'admin@example.com', '$2b$12$DGIeA82k8Y08z7IB8s56U.V.a5Cg7.K.p2T85e54NvJSHvXf/iDXq', NOW());


-- =============================================
-- INSERIR DADOS NA TABELA 'pacientes'
-- =============================================
-- Todos os pacientes são associados ao usuário com id = 1 (Administrador)
INSERT INTO `pacientes` (`name`, `cpf`, `telefone`, `cep`, `number`, `complement`, `email`, `status`, `user`, `data_stamp`, `data_modif`, `user_modif`)
VALUES
('Ana Silva', '111.222.333-44', '11987654321', '01001-000', '100', 'Apto 22', 'ana.silva@example.com', 1, 1, NOW(), NOW(), 1),
('Bruno Costa', '222.333.444-55', '21912345678', '20040-030', '500', 'Sala 10', 'bruno.costa@example.com', 1, 1, NOW(), NOW(), 1),
('Carla Dias', '333.444.555-66', '31955558888', '30110-000', '32', NULL, 'carla.dias@example.com', 0, 1, NOW(), NOW(), 1);


-- =============================================
-- INSERIR DADOS NA TABELA 'sessoes'
-- =============================================
-- As sessoes são associadas aos pacientes pelos IDs (1 para Ana, 2 para Bruno)
INSERT INTO `sessoes` (`paciente_id`, `data_hora`, `status`, `created_at`)
VALUES
(1, '2025-10-05 10:00:00', 1, NOW()), -- Sessão da Ana Silva
(1, '2025-10-12 10:00:00', 1, NOW()), -- Outra sessão da Ana Silva
(2, '2025-10-07 14:30:00', 1, NOW()); -- Sessão do Bruno Costa


-- =============================================
-- INSERIR DADOS NA TABELA 'configuracoes'
-- =============================================
INSERT INTO `configuracoes` (`chave`, `valor`, `created_at`)
VALUES
('nome_clinica', 'Clínica Foco & Bem-Estar', NOW()),
('horario_abertura', '08:00', NOW()),
('horario_fechamento', '18:00', NOW());