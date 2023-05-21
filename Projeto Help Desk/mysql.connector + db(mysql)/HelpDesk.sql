Create database HDesk;
use Hdesk;

create table Cliente(
IDCliente int primary key auto_increment,
NomeCliente varchar(80) not null,
Cpf_cnpj int not null,				
Email_Cliente varchar(80) not null,
Telefone_Cliente varchar(10) not null,
Assunto ENUM('NOSSOS APLICATIVOS','DÚVIDAS FINANCEIRAS','SUPORTE TÉCNICO', 'RECLAMAÇÕES', 'OUTRAS INFORMAÇÕES'),
Descricao text(300)
);

create table Usuario(
IDUsuario int primary key auto_increment, 
NomeUsuario varchar(100) not null,
Email_Usuario varchar(80) not null,
Setor varchar(50),
Turno varchar(1),
Usuario_Ativo char(1)
);

 create table Solicitacao(
 IDSolicitacao int primary key auto_increment,
 IDCliente int,
 IDUsuario int, 
 Assunto ENUM('NOSSOS APLICATIVOS','DÚVIDAS FINANCEIRAS','SUPORTE TÉCNICO', 'RECLAMAÇÕES', 'OUTRAS INFORMAÇÕES'),		 
 Prioridade ENUM('BAIXA', 'MÉDIA', 'ALTA'),
 Data_Solicitacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
 SolicitacaoaAtivo Char(1),
 foreign key(IDUsuario) references Usuario(IDUsuario),
 foreign key(IDCliente) references Cliente(IDCliente)
 );
 
 create table SolicitacaoStatus(
 IDSolicitacaoStatus int primary key auto_increment,
 IDSolicitacao int, 
 IDStatus ENUM('ABERTO','FECHADO', 'EM ANDAMENTO'),
 IDUsuario int,
 DataStatus Datetime, 														
 foreign key(IDUsuario) references Usuario(IDUsuario),
 foreign key(IDSolicitacao) references Solicitacao(IDSolicitacao)
 );

    SELECT * FROM atendimento;
    SELECT * FROM atendimento WHERE status_ = 'aberto';

    INSERT INTO atendimento () VALUES ();

    UPDATE atendimento set status_ = "" where id =1;

    DELETE FROM atendimento WHERE id = 1;
