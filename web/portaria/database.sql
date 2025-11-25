-- Criar a base de dados
CREATE DATABASE portaria;

-- Tabela de usuários
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(255) NOT NULL,
    email_usuario VARCHAR(255) NOT NULL UNIQUE,
    senha_usuario VARCHAR(255) NOT NULL
);

INSERT INTO usuarios (nome_usuario, email_usuario, senha_usuario) VALUES ('admin', 'usuario.nextsoft@gmail.com', '123');

CREATE TABLE moradores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_morador VARCHAR(255) NOT NULL,
    email_morador VARCHAR(255) NOT NULL UNIQUE,
    cpf_morador VARCHAR(255) NOT NULL UNIQUE,
    telefone_morador VARCHAR(255) NOT NULL UNIQUE,
    nascimento_morador DATE NOT NULL,
    apartamento_morador VARCHAR(255) NOT NULL,
    bloco_morador VARCHAR(255) NOT NULL,
    moradia_morador VARCHAR(255) NOT NULL,
    quantidade_morador VARCHAR(255) NOT NULL,
    foto_morador VARCHAR(255) NULL,
    face_descriptor TEXT NULL
);

CREATE TABLE veiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(10) NOT NULL UNIQUE,
    modelo VARCHAR(50) NULL,
    cor VARCHAR(30) NULL,
    apartamento VARCHAR(50) NOT NULL,
    morador_id INT,
    CONSTRAINT fk_morador FOREIGN KEY (morador_id) REFERENCES moradores(id) ON DELETE CASCADE
);

CREATE TABLE historico (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(255) NOT NULL,
    acao VARCHAR(255) NOT NULL,
    entidade VARCHAR(100) NOT NULL,
    data_registro DATE NOT NULL,
    hora_registro TIME NOT NULL
);

CREATE TABLE acessos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    morador_id INT NOT NULL,
    data_registro DATE NOT NULL,
    hora_registro TIME NOT NULL,
    FOREIGN KEY (morador_id) REFERENCES moradores(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Tabela de usuários mobile vinculada a moradores
CREATE TABLE usuarios_mobile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(100) NOT NULL,
    email_usuario VARCHAR(100) NOT NULL UNIQUE,
    senha_usuario VARCHAR(100) NOT NULL,
    morador_id INT,  -- vínculo com moradores
    CONSTRAINT fk_morador_mobile FOREIGN KEY (morador_id)
        REFERENCES moradores(id)
        ON DELETE CASCADE
);

-- Exemplo de inserção de usuários mobile já vinculados a moradores existentes
INSERT INTO usuarios_mobile (nome_usuario, email_usuario, senha_usuario, morador_id) 
VALUES 
('Laura Mendes', 'lauramendes@gmail.com', '123', 1);

-- Tabela de códigos gerados pelos moradores
CREATE TABLE codigos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10) NOT NULL,
    morador_id INT NOT NULL,
    validade_horas INT NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (morador_id) REFERENCES moradores(id)
);

-- Tabela de acessos de visitantes
CREATE TABLE acessos_visitantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_id INT NOT NULL,          -- código usado
    morador_id INT NOT NULL,         -- quem gerou
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (codigo_id) REFERENCES codigos(id),
    FOREIGN KEY (morador_id) REFERENCES moradores(id)
);