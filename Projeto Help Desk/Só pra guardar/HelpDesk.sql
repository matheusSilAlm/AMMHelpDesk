Create database HDesk;
use Hdesk;

create table Pessoa( 
IDPessoa int primary key, 
NomePessoa varchar(80),
Cpf_cnpj char(14),				
Email varchar(80),
Telefone varchar(10)
);

create table Usuario (
IDUsuario int not null,
IDPessoa int not null, 
Setor varchar(50),
Turno varchar(1),
Usuario_Ativo char(1),
primary key (IDUsuario),
foreign key(IDPessoa) references Pessoa(IDPessoa)
);

 create table Solicitacao(
 IDSolicitacao int primary key,
 IDUsuario int, 
 IDTipo_Servico smallint,		 
 IDPrioridade smallint,
 Data_Solicitacao datetime,
 Descricao text,
 SolicitacaoaAtivo Char(1),
 foreign key(IDUsuario) references Usuario(IDUsuario)
 );
 
 create table SolicitacaoAnexo (
 IDSolicitacaoAnexo int primary key,
 IDSolicitacao int,
 NomeArquivoAnexo varchar(50),
 Path_ varchar(250),
 foreign key(IDSolicitacao) references Solicitacao(IDSolicitacao)
 );
 
 create table Status_ (
 IDStatus smallint primary key, 
 NomeStatus varchar(20),
 Status_Ativo char(1)
 );
 
 create table SolicitacaoStatus(
 IDSolicitacaoStatus int primary key, 
 IDSolicitacao int, 
 IDStatus smallint, 					
 IDUsuario int,
 DataStatus Datetime,
 foreign key(IDUsuario) references Usuario(IDUsuario),
 foreign key(IDSolicitacao) references Solicitacao(IDSolicitacao),
 foreign key(IDStatus) references Status_(IDStatus)
 );
 
 create table Prioridade (
 IDPrioridade smallint primary key,
 IDSolicitacao int,
 NomePrioridade varchar(20),
 PrioridadeAtivo char(1),
 foreign key(IDSolicitacao ) references Solicitacao(IDSolicitacao)
 );

    SELECT * FROM atendimento;
    SELECT * FROM atendimento WHERE status_ = 'aberto';

    INSERT INTO atendimento () VALUES ();

    UPDATE atendimento set status_ = "" where id =1;

    DELETE FROM atendimento WHERE id = 1;
