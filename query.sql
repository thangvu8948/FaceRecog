go
use master
go
if db_id('FaceData') is not null
	drop database FaceData
create database FaceData
go
use FaceData
go
create table People
(
	Id	char(8) not null,
	Name nvarchar(30) not null,
	Age int,
	Gender bit
	primary key(Id)
)

select * from People