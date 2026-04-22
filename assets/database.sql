DROP DATABASE IF EXISTS appstore_wallet;

CREATE DATABASE appstore_wallet 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE appstore_wallet;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    senha VARCHAR(250)
);

CREATE TABLE eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    data DATE NOT NULL,
    local VARCHAR(255) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    capacidade INT DEFAULT 100,
    ingressos_vendidos INT DEFAULT 0,
    imagem VARCHAR(500),
    usuario_id INT NOT NULL,
    CONSTRAINT fk_dono_evento 
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
);

CREATE TABLE ingressos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    evento_id INT,
    data_compra DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_ingresso_usuario 
        FOREIGN KEY (usuario_id) 
        REFERENCES usuarios(id) 
        ON DELETE CASCADE,

    CONSTRAINT fk_ingresso_evento 
        FOREIGN KEY (evento_id) 
        REFERENCES eventos(id) 
        ON DELETE CASCADE,

    CONSTRAINT unique_ingresso 
        UNIQUE (usuario_id, evento_id)
);

INSERT INTO usuarios (nome, email, senha)
VALUES (
    "Admin", 
    "admin@email.com", 
    "$2y$10$t61kBiULXzirkkctBXSb9.KItW8tQwi6S2wil7TnM19JF3ln17k32"
);

INSERT INTO eventos 
(nome, data, local, preco, capacidade, ingressos_vendidos, imagem, usuario_id)
VALUES
('Festival da Ilha Mako', '2026-04-25', 'São Paulo', 80.00, 100, 10,
 'https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=800', 1),
('Noite Encantada', '2026-05-10', 'Rio de Janeiro', 120.00, 150, 120,
 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800', 1);

CREATE TABLE favoritos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    evento_id INT NOT NULL,
    data_adicionado DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_favorito_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    CONSTRAINT fk_favorito_evento FOREIGN KEY (evento_id) REFERENCES eventos(id) ON DELETE CASCADE,
    UNIQUE KEY unique_favorito (usuario_id, evento_id)
);