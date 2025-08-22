# mysql-database-docker
banco de dados rodando em container

  docker exec -it my-mysql bash
  
  mysql -u root -p
  
  CREATE DATABASE MYSQLTESTE;
  
  update mysql.user set host='%' where user='root';
  
  FLUSH PRIVILEGES;
  
  docker restart my-mysql


# main.py

Serve para BKP (Dumps)

Necessário configurar variavel MEUS_BKPS e schedule com novo item do dict
