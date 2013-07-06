BEGIN;
CREATE TABLE gerenciador_testes_casodeteste (
    id integer NOT NULL PRIMARY KEY,
    titulo varchar(200) NOT NULL,
    caminhoSikuli varchar(200) NOT NULL
);
CREATE TABLE gerenciador_testes_casodetestepasso (
    id integer NOT NULL PRIMARY KEY,
    casoDeTeste_id integer NOT NULL REFERENCES gerenciador_testes_casodeteste (id),
    nPasso integer NOT NULL,
    descr varchar(200) NOT NULL,
    resultExperado varchar(200) NOT NULL
)
;
CREATE TABLE gerenciador_testes_projeto (
    id integer NOT NULL PRIMARY KEY,
    nomeProjeto varchar(200) NOT NULL,
    dataAbertura date NOT NULL
)
;
CREATE TABLE gerenciador_testes_casodetesteemprojeto (
    id integer NOT NULL PRIMARY KEY,
    projeto_id integer NOT NULL REFERENCES gerenciador_testes_projeto (id),
    casoDeTeste_id integer NOT NULL REFERENCES gerenciador_testes_casodeteste (id)
)
;
CREATE TABLE gerenciador_testes_testset (
    id integer NOT NULL PRIMARY KEY,
    nome varchar(200) NOT NULL,
    dataAbertura date NOT NULL,
    dataFechamento date
)
;
CREATE TABLE gerenciador_testes_casodetestevstestset (
    id integer NOT NULL PRIMARY KEY,
    casoDeTeste_id integer NOT NULL REFERENCES gerenciador_testes_casodeteste (id),
    testSet_id integer NOT NULL REFERENCES gerenciador_testes_testset (id)
)
;
COMMIT;
