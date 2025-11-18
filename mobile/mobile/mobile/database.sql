USE portaria;

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
('Laura Mendes', 'lauramendes7212@gmail.com', '123', 1),
('Maria Paula', 'mariapaula@gmail.com', '123', 5);

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