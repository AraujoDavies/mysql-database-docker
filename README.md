# mysql-database-docker
banco de dados rodando em container

  docker exec -it my-mysql bash
  
  mysql -u root -p
  
  CREATE DATABASE MYSQLTESTE;
  
  update mysql.user set host='%' where user='root';
  
  FLUSH PRIVILEGES;
  
  docker restart my-mysql
