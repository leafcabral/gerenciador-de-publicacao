DROP SCHEMA IF EXISTS publicacao ;
CREATE SCHEMA IF NOT EXISTS publicacao DEFAULT CHARACTER SET utf8MB4;
USE publicacao ;

CREATE TABLE livraria (
	ID_LIVRARIA char(4) NOT NULL,
	NOME_LIVRARIA varchar(40) DEFAULT NULL,
	ENDERECO varchar(40) DEFAULT NULL,
	CIDADE varchar(20) DEFAULT NULL,
	ESTADO char(2) DEFAULT NULL,
	CEP varchar(5) DEFAULT NULL,
	PRIMARY KEY (ID_LIVRARIA));

INSERT INTO livraria (ID_LIVRARIA, NOME_LIVRARIA, ENDERECO, CIDADE, ESTADO, CEP) VALUES 
('6380','Leitura Final Livros','Av. Cataguases, 788','Ribeirão Preto','SP','98056'),
('7066','Livraria Guanabara','Av. Passo Fundo, 567','Galeão','RJ','92789'),
('7067','Cultura Geral','Rua Primeiro de Maio, 577','São Paulo','SP','96745'),
('7131','Qualidade em Livros','Via Expressa, Km 22','Porto Alegre','RS','98014'),
('7896','Shopping dos Livros','Av. Madison Square, s/n','Vitória','ES','90019'),
('8042','Livraria Italiana','Rua Carson City, 679','Curitiba','PR','89076');

--
-- Table structure for table editoras
--


CREATE TABLE editoras (
	ID_EDITORA int(8) NOT NULL AUTO_INCREMENT,
	NOME_EDITORA varchar(40) DEFAULT NULL,
	CIDADE varchar(20) DEFAULT NULL,
	ESTADO char(2) DEFAULT NULL,
	NOME_PAIS varchar(30) DEFAULT NULL,
	PRIMARY KEY (ID_EDITORA)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8MB4;

--
-- Dumping data for table editoras
--

INSERT INTO editoras (ID_EDITORA, NOME_EDITORA, CIDADE, ESTADO, NOME_PAIS) VALUES 
(736,'Editora Lunar','São Paulo','SP','Brasil'),
(877,'Bonnie e Clyde Editora','Brasília','DF','Brasil'),
(1389,'Algodata Infosystems','Salvador','BA','Brasil'),
(1622,'Cinco Lagos Publicações','Recife','PE','Brasil'),
(1756,'Ramona Editoras','Belém','PA','Brasil'),
(9901,'Loucas Horas','Dusseldorf',NULL,'Alemanha'),
(9952,'Editora Viajantes Sem Rumo Ltda','Rio de Janeiro','RJ','Brasil'),
(9999,'Lucerne Publicações','Paris',NULL,'França');

--
-- Table structure for table titulos
--


CREATE TABLE titulos (
	ID_TITULO int(8) NOT NULL AUTO_INCREMENT,
	TITULO_LIVRO varchar(80) NOT NULL,
	TIPO_LIVRO varchar(12) NOT NULL,
	ID_EDITORA int(8) DEFAULT NULL,
	PRECO decimal(15,2) DEFAULT NULL,
	TOTAL_VENDA decimal(15,2) DEFAULT NULL,
	ROYALTY int(8) DEFAULT NULL,
	MEDIA_QUANT_VENDAS int(8) DEFAULT NULL,
	OBSERVACOES varchar(200) DEFAULT NULL,
	DATA_PUBLICACAO date NOT NULL,
	PRIMARY KEY (ID_TITULO),
	KEY ID_EDITORA (ID_EDITORA),
	CONSTRAINT titulos_ibfk_1 FOREIGN KEY (ID_EDITORA) REFERENCES editoras (ID_EDITORA)
) ENGINE=InnoDB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8MB4;

--
-- Dumping data for table titulos
--

INSERT INTO titulos (ID_TITULO, TITULO_LIVRO, TIPO_LIVRO, ID_EDITORA, PRECO, TOTAL_VENDA, ROYALTY, MEDIA_QUANT_VENDAS, OBSERVACOES, DATA_PUBLICACAO) VALUES (1032,'Banco de Dados Guia para o Executivo Ocupado','negocios',1389,19.99,5000.00,10,4095,'Um overview dos bancos de dados disponíveis, enfatizando as aplicações de negócios. Ilustrado.','1991-06-12'),
(1035,'Mas ele é mesmo amigável para o Usuário?','computacao',1389,22.95,7000.00,16,8780,'Um guia de softwares para novos usuários, focando na sua interface \'amigável\'.','1997-06-30'),
(1111,'Cozinha utilizando Computadores: Um balanço Sincero','negocios',1389,11.95,5000.00,10,3876,'Útil para quem quer utilizar os recursos eletrônicos para tirar vantagem dos computadores.','1991-06-09'),
(1372,'Variações Comportamentais de fobias individuais de computadores','psicologia',877,21.59,7000.00,10,375,'O melhor para os especialistas, este livro relata as diferenças entre aqueles que odeiam e aqueles que têm medo de computadores. O que fazer e o que não fazer.','2001-10-21'),
(2075,'Você pode combater o Stress Computacional!','negocios',736,2.99,10125.00,24,18722,'As mais recentes técnicas médicas e psicológicas para viver no ofício dos computadores. Explicações claras.','1998-06-30'),(2091,'É ele o Inimigo?','psicologia',736,10.95,2275.00,12,2045,'Estudo cuidadosamente feito sobre os efeitos de fortes emoções sobre o corpo. Mapas de metabolismo incluído.','1998-06-15'),
(2106,'Vivendo sem medo','psicologia',736,7.00,6000.00,10,111,'Novos exercícios, meditação, e técnicas nutricionais que podem reduzir o choque das iterações diárias. Inclui exemplos de menus, Vídeo (não incluído).','1999-10-05'),(2222,'Tratamento Gastronômico do Vale do Paraíba','culinaria',877,19.99,0.00,12,2032,'Receits favoritas, rápido, fácil e elegante.','1992-06-09'),(3021,'O Gourmet com Microondas','culinaria',877,2.99,15000.00,24,22246,'Gourmets da culinária tradicional francesa se adaptam à vida moderna utilizando microondas na cozinha.','2000-06-18'),(3026,'A psicologia dos computadores na cozinha','Indefinido',877,NULL,NULL,NULL,NULL,NULL,'2005-03-21'),
(3218,'Alho, Cebola e Alho Poró: Segredos da culinária do Mediterrâneo','culinaria',877,20.95,7000.00,10,375,'Fartamente ilustrado em cores, o que faz dessa obra um ótimo presente para os amigos que gostam de cozinhar.','2000-10-21'),(3333,'Prolongando a Privação de Doentes Mentais: Quatro Estudos de Caso','psicologia',736,19.99,2000.00,10,4072,'O que acontece quando o processamento das mensagens mentais são interceptadas? Pesquisas de Avaliação e informação dos seus efeitos.','1992-06-01'),(4203,'Cinco anos na cozinha do Palácio do Planalto','culinaria',877,11.95,4000.00,14,15096,'Mais piadas descrevendo o ambiente culinário da cozinha presidencial.','1997-06-12'),
(7777,'Segurança Emocional: Uma nova visão','psicologia',736,7.99,4000.00,10,3336,'Protegendo você mesmo e os que você ama do stress emocional do mundo moderno. Ênfase em computadores e nutrição.','1991-06-12'),
(7832,'Falando francamente sobre computadores','negocios',1389,19.99,5000.00,10,4095,'Análises Anotadas do que os computadores podem fazer por você: Um guia para usuários críticos.','2005-06-22'),
(8888,'Segredos do Vale do Silício','computacao',1389,20.00,8000.00,10,4095,'História dos maiores computadores do mundo e seus fabricantes.','1994-12-06'),(9999,'Etiqueta de Rede','computacao',1389,NULL,NULL,NULL,NULL,'Leitura obrigatória para conferências computacionais.','2005-03-21');

--
-- Table structure for table autores
--


CREATE TABLE autores (
	ID_AUTOR char(11) NOT NULL,
	NOME varchar(40) NOT NULL,
	SOBRENOME varchar(20) NOT NULL,
	TELEFONE varchar(12) NOT NULL,
	ENDERECO varchar(40) DEFAULT NULL,
	CIDADE varchar(20) DEFAULT NULL,
	ESTADO char(2) DEFAULT NULL,
	CEP varchar(5) DEFAULT NULL,
	TIPO_CONTRATO char(1) NOT NULL,
	PRIMARY KEY (ID_AUTOR)
) ENGINE=InnoDB DEFAULT CHARSET=utf8MB4;

INSERT INTO autores (ID_AUTOR, NOME, SOBRENOME, TELEFONE, ENDERECO, CIDADE, ESTADO, CEP, TIPO_CONTRATO) VALUES 
('172-32-1176','Johnson','White','408 496-7223','Rodovia Bigge, 10932','Eunápolis','BA','94025','1'),
('213-46-8915','Ana','Marjorie','415 986-7020','Av Transamazonica, 411','Manaus','AM','94618','1'),
('238-95-7766','Carlos','Cherry','415 548-7723','Rua Darwin, 589','Belem','PA','94705','1'),
('267-41-2394','O\'Lauro','Maciel','408 286-2428','Av. Cleveland, 2214','Itabunas','BA','95128','1'),
('274-80-9391','James','Dean','415 834-2919','Av. Telégrafo, 5420','Paulo Afonso','BA','94609','1'),
('341-22-1782','Mauro','Smith','913 843-0462','Alameda Mississippi, 10','São Paulo','SP','66044','0'),
('409-56-7008','Benedito','Abraao','415 658-9932','Rua Batman, 623','Itaberaba','GO','94705','1'),
('427-17-2319','Anne','Dull','415 836-7128','Av. Blonde, 3410','Santo Antonio Jesus','BA','94301','1'),
('472-27-2349','Barbara','Berta','707 938-6445','Caixa Postal 792','Madre de Deus','BA','95428','3'),
('486-29-1786','Charlene','Souza','415 585-4620','Av. Broadway, 18','Feira de Santana','BA','94130','1'),
('527-72-3246','Gena','Minister','615 297-2723','Rodovia BR-222, Km 123','Palmas','TO','37215','0'),
('648-92-1872','Reginaldo','Rossi','503 745-6402','Ed. Hillsdale, Apto A2','Rio de Janeiro','RJ','97330','1'),
('672-71-3249','Akiko','Yokomoto','415 935-4228','Beco Silver, 3','Alagoinhas','BA','94595','1'),
('712-45-1867','Ines','Castillo','615 996-8275','Esplanada dos Ministérios, 2286','Brasília','DF','48105','1'),
('722-51-5454','Francis','Miguel','219 547-9982','Rua Palm Beach','Goiania','GO','46403','1'),
('724-08-9931','Dico','Stringer','415 843-2991','Av. Telégrafo, 5420','Paulo Afonso','BA','94609','0'),
('724-80-9391','Stenio','Garamound','415 354-7128','Hotel Upland, 66','Paulo Afonso','BA','94612','1'),
('756-30-7391','Livia','Karsen','415 534-9219','Av. Maculelê, 5720','Paulo Afonso','BA','94609','1'),
('807-91-6654','Wanderley','Silvino','301 946-8853','Rua Arlindo Santos','Vila Formosa','SP','20853','1'),
('846-92-7186','Sheryl','Hunt','415 836-7128','Av. Blonde, 3410','Santo Antonio Jesus','BA','94301','1'),
('893-72-1158','Hilton','Souza','707 448-4982','Rua Putnam, 301','Paulo Afonso','BA','95688','0'),
('899-46-2035','Anne','Santos','801 826-0752','Sétima Avenida, 67','Sete Quedas','RS','84152','1'),
('998-72-3567','Alberto','Santos','801 826-0752','Sétima Avenida, 67','Sete Quedas','RS','84152','1');
--
-- Table structure for table autoria
--


CREATE TABLE autoria (
	ID_AUTOR char(11) NOT NULL,
	ID_TITULO int(8) NOT NULL,
	ORDEM_AUTORIA smallint(6) DEFAULT NULL,
	PERCENTUAL_ROYALTY smallint(6) DEFAULT NULL,
	PRIMARY KEY (ID_AUTOR,ID_TITULO),
	KEY ID_TITULO (ID_TITULO),
	CONSTRAINT autoria_ibfk_2 FOREIGN KEY (ID_TITULO) REFERENCES titulos (ID_TITULO),
	CONSTRAINT autoria_ibfk_1 FOREIGN KEY (ID_AUTOR) REFERENCES autores (ID_AUTOR)
) ENGINE=InnoDB DEFAULT CHARSET=utf8MB4;

--
-- Dumping data for table autoria
--

INSERT INTO autoria (ID_AUTOR, ID_TITULO, ORDEM_AUTORIA, PERCENTUAL_ROYALTY) VALUES ('172-32-1176',3333,1,100),
('213-46-8915',1032,2,40),('213-46-8915',2075,1,100),('238-95-7766',1035,1,100),('267-41-2394',1111,2,40),
('267-41-2394',7777,2,20),('274-80-9391',7832,1,100),('409-56-7008',1032,1,60),('427-17-2319',8888,1,50),
('472-27-2349',7777,3,20),('486-29-1786',7777,1,40),('486-29-1786',9999,1,100),('648-92-1872',4203,1,100),
('672-71-3249',7777,4,20),('712-45-1867',2222,1,100),('722-51-5454',3021,1,75),('724-80-9391',1111,1,60),
('724-80-9391',1372,2,25),('756-30-7391',1372,1,75),('807-91-6654',3218,1,100),('846-92-7186',8888,2,50),
('899-46-2035',2091,2,50),('899-46-2035',3021,2,25),('998-72-3567',2091,1,50),('998-72-3567',2106,1,100);
--
-- Table structure for table cargos
--


CREATE TABLE cargos (
	ID_CARGO smallint(6) NOT NULL AUTO_INCREMENT,
	DESCRICAO varchar(50) NOT NULL,
	NIVEL_MINIMO smallint(6) NOT NULL,
	NIVEL_MAXIMO smallint(6) NOT NULL,
	PRIMARY KEY (ID_CARGO)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8MB4;

--
-- Dumping data for table cargos
--

INSERT INTO cargos (ID_CARGO, DESCRICAO, NIVEL_MINIMO, NIVEL_MAXIMO) VALUES 
(1,'Novas contratações - Cargo não Especificado',10,10),
(2,'Diretor Financeiro',200,250),
(3,'Diretor de Publicação',175,225),
(4,'Diretor Comercial',175,250),
(5,'Editor I',150,250),
(6,'Gerente de Apoio Administrativo',140,225),
(7,'Gerente de Marketing',120,200),
(8,'Gerente de Relações Públicas',100,175),
(9,'Gerente de Vendas',75,175),
(10,'Gerente de Apoio Operacional',75,165),
(11,'Gerente de Compras',75,150),
(12,'Editor II',25,100),
(13,'Representante de Vendas',25,100),
(14,'Designer',25,100),
(15,'Presidente',250,300),
(16,'Gerente de Contabilidade e Custos',200,250),
(17,'Chefe de Departamento',175,225),
(18,'Chefe de Divisão',150,250),
(19,'Analista de Negócios',150,200),
(20,'Engenheiro Ambiental',150,200),
(21,'Analista Contábil',150,200),
(22,'Analista de Compras',150,200),
(23,'Técnico de Vendas',100,120),
(24,'Técnico de Compras',100,120),
(25,'Técnico de Segurança do Trabalho',100,120),
(26,'Motorista',90,110),
(27,'Técnico Compras no Atacado',100,120);

--
-- Table structure for table lotacao
--


CREATE TABLE lotacao (
	ID_LOTACAO char(5) NOT NULL,
	DSC_LOTACAO varchar(50) NOT NULL,
	ID_LOTACAO_SUP char(5) DEFAULT NULL,
	MATR_CHEFE int DEFAULT NULL,
	PRIMARY KEY (ID_LOTACAO),
	KEY ID_LOTACAO_SUP (ID_LOTACAO_SUP),
	KEY MATR_CHEFE (MATR_CHEFE),
	CONSTRAINT lotacao_ibfk_1 FOREIGN KEY (ID_LOTACAO_SUP) REFERENCES lotacao (ID_LOTACAO)
) ENGINE=InnoDB DEFAULT CHARSET=utf8MB4;

--
-- Dumping data for table lotacao
--

INSERT INTO lotacao (ID_LOTACAO, DSC_LOTACAO, ID_LOTACAO_SUP, MATR_CHEFE) VALUES 
('10000','Presidência',NULL,1205),
('11000','Diretoria de Publicação','10000',1010),
('11100','Gerência de Marketing','11000',1118),
('11110','Departamento de Publicidade e Propaganda','11100',1183),
('11200','Gerência de Relações Públicas','11000',1125),
('11210','Departamento de Controle Ambiental','11200',1231),
('12000','Diretoria Comercial','10000',1022),
('12100','Gerência de Apoio Administrativo','12000',1104),
('12110','Departamento de Recursos Humanos','12100',1240),
('12111','Divisão de Folha de Pagamento','12110',NULL),
('12200','Gerência de Vendas','12000',1131),
('13000','Diretoria Financeira','10000',1005),
('13100','Gerência de Apoio Operacional','13000',1149),
('13110','Departamento de Transportes','13100',1255),
('13111','Divisão de Segurança Patrimonial','13110',NULL),
('13200','Gerência de Compras','13000',1157),
('13210','Departamento de Compras a Varejo','13200',1264),
('13220','Departamento de Compras no Atacado','13200',1278),
('13300','Gerência de Contabilidade e Custos','13000',1214),
('13310','Departamento de Contas a Pagar','13300',1286),
('13320','Departamento de Contas a Receber','13300',1293);

--
-- Table structure for table empregados
--


CREATE TABLE empregados (
	MATRICULA int(8) NOT NULL AUTO_INCREMENT,
	NOME varchar(20) NOT NULL,
	SOBRENOME varchar(30) NOT NULL,
	ID_CARGO smallint(6) NOT NULL,
	NIVEL_CARGO smallint(6) DEFAULT NULL,
	ID_EDITORA int(8) NOT NULL,
	DT_CONTRATACAO date DEFAULT NULL,
	ID_LOTACAO char(5) DEFAULT NULL,
	PRIMARY KEY (MATRICULA),
	KEY ID_CARGO (ID_CARGO),
	KEY ID_EDITORA (ID_EDITORA),
	KEY ID_LOTACAO (ID_LOTACAO),
	CONSTRAINT empregados_ibfk_3 FOREIGN KEY (ID_LOTACAO) REFERENCES lotacao (ID_LOTACAO),
	CONSTRAINT empregados_ibfk_1 FOREIGN KEY (ID_CARGO) REFERENCES cargos (ID_CARGO),
	CONSTRAINT empregados_ibfk_2 FOREIGN KEY (ID_EDITORA) REFERENCES editoras (ID_EDITORA)
) ENGINE=InnoDB AUTO_INCREMENT=1454 DEFAULT CHARSET=utf8MB4;

--
-- Dumping data for table empregados
--

INSERT INTO empregados (MATRICULA, NOME, SOBRENOME, ID_CARGO, NIVEL_CARGO, ID_EDITORA, DT_CONTRATACAO, ID_LOTACAO) VALUES (1005,'Felipe','Ferreira',2,215,9952,'1989-11-11','11200'),(1010,'Anne','Pádua',3,200,9952,'1991-07-16','12200'),(1022,'Francisco','Chang',4,227,9952,'1990-11-03','13100'),(1034,'Laurence','Lebihan',5,175,736,'1990-06-03','13200'),(1048,'Paulo','Henrique',5,159,877,'1993-08-19','11110'),(1052,'Steve','Pereira',5,150,1389,'1991-04-05','12200'),(1066,'Rita','Muller',5,190,1622,'1993-10-09','11110'),(1070,'Maria','Pontes',5,190,1756,'1989-03-01','12111'),(1086,'Janine','Lorena',5,190,9901,'1991-05-26','10000'),(1090,'Carlos','Ernandes',5,170,9999,'1999-04-21','13300'),(1104,'Vitoria','Oliveira',6,140,877,'1990-09-13','11110'),(1118,'Wesley','Branco',7,120,877,'1991-02-13','11210'),(1125,'Anabela','Domingues',8,175,877,'1993-01-27','12110'),(1131,'Martins','Hans',9,170,877,'1992-02-05','13110'),(1149,'Pedro','Frankmar',10,175,877,'1992-05-17','13210'),(1157,'Daniel','Tonini',11,190,877,'1990-01-01','13220'),(1165,'Helen','Bennetton',12,90,877,'1989-09-21','13310'),(1170,'Paulo','Augusto',13,70,877,'1992-08-27','12111'),(1183,'Elizabeth','Lincoln',14,65,877,'1990-07-24','13111'),(1198,'Mateus','Parreira',19,160,736,'1994-05-01','13320'),(1205,'Paulo','Ibsen',15,280,736,'1993-05-09','13310'),(1214,'Maria','Severina',16,160,736,'1993-06-29','13111'),(1222,'Geraldo','Thomas',17,170,736,'1988-08-09','13310'),(1231,'Martinho','Silva',17,165,736,'1990-04-13','11210'),(1240,'José','Parreira',17,175,736,'1991-09-05','11210'),(1255,'Helio','CastroNeves',17,180,736,'1988-11-19','13300'),(1264,'Timothy','Sant\'ana',17,175,736,'1988-06-19','13310'),(1278,'Karine','Kirmair',17,180,736,'2000-10-17','13320'),(1286,'Diego','Joelson',17,185,1389,'1991-12-16','13110'),(1293,'Maria','Larissa',17,178,1389,'1992-03-27','13220'),(1308,'Paula','Parente',18,120,1389,'1994-01-19','13220'),(1312,'Margarete','Gaigher',18,120,1389,'1988-09-29','12111'),(1321,'MAria','Cruz',19,100,1389,'1991-10-26','13111'),(1337,'Miguel','Paulino',19,112,1389,'1992-12-07','12200'),(1349,'Yoshi','Latimer',19,123,1389,'1989-06-11','13320'),(1350,'Carina','Schmitt',19,127,1389,'1992-07-07','13310'),(1365,'Pedro','Afonso',20,110,1389,'1990-12-24','11210'),(1373,'Janete','Orlinda',20,152,9999,'1990-02-21','11210'),(1381,'Nagib','Souza',21,120,9999,'1993-03-19','13300'),(1390,'Manuel','Pereira',21,101,9999,'1989-01-09','13310'),(1406,'Karla','Jacobian',21,170,9999,'1994-03-11','13320'),(1413,'Pedro','Kristofesson',26,80,9999,'1993-11-29','13110'),(1429,'Patricia','Moreira',27,90,9999,'2000-08-01','13220'),(1450,'João','Libório',27,100,736,'1990-09-01','13220'),(1451,'Pedro','Haschimaniov',19,111,877,'1995-10-10','12111'),(1452,'Annabela','Callot',25,110,736,'1991-11-08','13111'),(1453,'Fábio','Krusk',23,90,1389,'1997-12-31','12200');

--
-- Table structure for table faixa_royalty
--


CREATE TABLE faixa_royalty (
	ID_TITULO int(8) NOT NULL,
	LIMITE_INFERIOR int(8) NOT NULL DEFAULT '0',
	LIMITE_SUPERIOR int(8) DEFAULT NULL,
	ROYALTY int(8) DEFAULT NULL,
	PRIMARY KEY (ID_TITULO,LIMITE_INFERIOR),
	CONSTRAINT faixa_royalty_ibfk_1 FOREIGN KEY (ID_TITULO) REFERENCES titulos (ID_TITULO)
) ENGINE=InnoDB DEFAULT CHARSET=utf8MB4;

--
-- Dumping data for table faixa_royalty
--

INSERT INTO faixa_royalty (ID_TITULO, LIMITE_INFERIOR, LIMITE_SUPERIOR, ROYALTY) VALUES 
(1032,0,5000,10),(1032,5001,50000,12),(1035,0,2000,10),(1035,2001,3000,12),(1035,3001,4000,14),(1035,4001,10000,16),(1035,10001,50000,18),(1111,0,4000,10),(1111,4001,8000,12),(1111,8001,10000,14),(1111,12001,16000,16),(1111,16001,20000,18),(1111,20001,24000,20),(1111,24001,28000,22),(1111,28001,50000,24),(1372,0,10000,10),(1372,10001,20000,12),(1372,20001,30000,14),(1372,30001,40000,16),(1372,40001,50000,18),(2075,0,1000,10),(2075,1001,3000,12),(2075,3001,5000,14),(2075,5001,7000,16),(2075,7001,10000,18),(2075,10001,12000,20),(2075,12001,14000,22),(2075,14001,50000,24),(2091,0,1000,10),(2091,1001,5000,12),(2091,5001,10000,14),(2091,10001,50000,16),(2106,0,2000,10),(2106,2001,5000,12),(2106,5001,10000,14),(2106,10001,50000,16),(2222,0,2000,10),(2222,2001,4000,12),(2222,4001,8000,14),(2222,8001,12000,16),(2222,12001,20000,18),(2222,20001,50000,20),(3021,0,1000,10),(3021,1001,2000,12),(3021,2001,4000,14),(3021,4001,6000,16),(3021,6001,8000,18),(3021,8001,10000,20),(3021,10001,12000,22),(3021,12001,50000,24),(3218,0,2000,10),(3218,2001,4000,12),(3218,4001,6000,14),(3218,6001,8000,16),(3218,8001,10000,18),(3218,10001,12000,20),(3218,12001,14000,22),(3218,14001,50000,24),(3333,0,5000,10),(3333,5001,10000,12),(3333,10001,15000,14),(3333,15001,50000,16),(4203,0,2000,10),(4203,2001,8000,12),(4203,8001,16000,14),(4203,16001,24000,16),(4203,24001,32000,18),(4203,32001,40000,20),(4203,40001,50000,22),(7777,0,5000,10),(7777,5001,50000,12),(7832,0,5000,10),(7832,5001,10000,12),(7832,10001,15000,14),(7832,15001,20000,16),(7832,20001,25000,18),(7832,25001,30000,20),(7832,30001,35000,22),(7832,35001,50000,24),(8888,0,5000,10),(8888,5001,10000,12),(8888,10001,15000,14),(8888,15001,50000,16);

--
-- Table structure for table livraria
--

--
-- Table structure for table vendas
--


CREATE TABLE vendas (
	ID_LIVRARIA char(4) NOT NULL,
	NUM_PEDIDO varchar(20) NOT NULL,
	ID_TITULO int(8) NOT NULL,
	DATA_PEDIDO date NOT NULL,
	QUANT_VENDAS smallint(6) NOT NULL,
	CONDICOES_PAGTO varchar(12) NOT NULL,
	PRIMARY KEY (ID_LIVRARIA,NUM_PEDIDO,ID_TITULO),
	KEY ID_TITULO (ID_TITULO),
	CONSTRAINT vendas_ibfk_1 FOREIGN KEY (ID_LIVRARIA) REFERENCES livraria (ID_LIVRARIA),
	CONSTRAINT vendas_ibfk_2 FOREIGN KEY (ID_TITULO) REFERENCES titulos (ID_TITULO)
) ENGINE=InnoDB DEFAULT CHARSET=utf8MB4;

--
-- Dumping data for table vendas
--

INSERT INTO vendas (ID_LIVRARIA, NUM_PEDIDO, ID_TITULO, DATA_PEDIDO, QUANT_VENDAS, CONDICOES_PAGTO) VALUES ('6380','6871',1032,'1994-09-14',5,'60 dias'),
('6380','722a',2091,'1994-09-13',3,'60 dias'),
('7066','A2976',8888,'2001-05-24',50,'30 dias'),
('7066','QA7442.3',2091,'1994-09-13',75,'A vista'),
('7067','D4482',2091,'1994-09-14',10,'60 dias'),
('7067','P2121',3218,'1992-06-15',40,'30 dias'),
('7067','P2121',4203,'1992-06-15',20,'30 dias'),
('7067','P2121',7777,'1992-06-10',20,'30 dias'),
('7131','N914008',2091,'1994-09-14',20,'30 dias'),
('7131','N914014',3021,'1994-09-14',25,'30 dias'),
('7131','P3087a',1372,'2001-05-29',20,'60 dias'),
('7131','P3087a',2106,'2001-05-29',25,'60 dias'),
('7131','P3087a',3333,'2001-05-29',15,'60 dias'),
('7131','P3087a',7777,'2001-05-29',25,'60 dias'),
('7896','QQ2299',7832,'2001-10-28',15,'60 dias'),
('7896','TQ456',2222,'2001-12-12',10,'60 dias'),
('7896','X999',2075,'2001-02-21',35,'A vista'),
('8042','423LL922',3021,'1994-09-14',15,'A vista'),
('8042','423LL930',1032,'1994-09-14',10,'A vista'),
('8042','P723',1111,'2001-03-11',25,'30 dias'),
('8042','QA879.1',1035,'2001-05-22',30,'30 dias');

/* Cria a chave estrangeira MATR_CHEFE A PARTIR DA TABELA EMPREGADOS */

ALTER TABLE LOTACAO ADD CONSTRAINT lotacao_ibfk_2 FOREIGN KEY (MATR_CHEFE) REFERENCES empregados (MATRICULA);