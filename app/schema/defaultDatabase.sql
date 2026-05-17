CREATE TABLE IF NOT EXISTS usuarios (
id SERIAL PRIMARY KEY,
nome VARCHAR(100),
login VARCHAR(50),
senha VARCHAR(50),
email VARCHAR(120) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS lancamentos (
id SERIAL PRIMARY KEY,
descricao VARCHAR(200),
valor NUMERIC(10,2),
tipo CHAR(1),
usuario_id INTEGER,
data DATE DEFAULT CURRENT_DATE,
status BOOLEAN DEFAULT TRUE,

CONSTRAINT fk_usuario
    FOREIGN KEY (usuario_id)
    REFERENCES usuarios(id)
    ON DELETE CASCADE
);

INSERT INTO usuarios (nome, login, senha, email)
SELECT 'Admin', 'admin', '123', 'julio.schneider1@universo.univates.br'
WHERE NOT EXISTS (
SELECT 1
FROM usuarios
WHERE login = 'admin'
);