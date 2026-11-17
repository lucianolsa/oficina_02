create table main.proprietarios
(
    id                INTEGER      not null
        primary key,
    nome              VARCHAR(100) not null,
    telefone          VARCHAR(20)  not null,
    email             VARCHAR(100) not null
        unique,
    cpf_hash          VARCHAR(64)  not null
        unique,
    cpf_criptografado VARCHAR(500) not null,
    criado_em         DATETIME default CURRENT_TIMESTAMP
);

create table main.carros
(
    id              INTEGER      not null
        primary key,
    modelo          VARCHAR(100) not null,
    placa           VARCHAR(10)  not null
        unique,
    proprietario_id INTEGER      not null
        references main.proprietarios
);

create table main.agendamentos
(
    id        INTEGER      not null
        primary key,
    data_hora DATETIME     not null,
    servico   VARCHAR(100) not null,
    carro_id  INTEGER      not null
        references main.carros,
    criado_em DATETIME default CURRENT_TIMESTAMP
);



create table main.usuarios
(
    id         INTEGER      not null
        primary key,
    name       VARCHAR(50)  not null,
    email      VARCHAR(120) not null
        unique,
    senha_hash VARCHAR(255) not null,
    criado_em  DATETIME default CURRENT_TIMESTAMP
);

