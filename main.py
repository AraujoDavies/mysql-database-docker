import os
import subprocess
import datetime
import schedule
from pathlib import Path
import logging
import time
import zipfile


logging.basicConfig(
    level=logging.INFO,
    encoding='utf-8',
    format="%(asctime)s - %(levelname)s: %(message)s"
)


def dump(bkp: dict):
    usuario = bkp['usuario']
    senha = bkp['senha']
    host = bkp['host']
    porta = bkp['porta']
    schema = bkp['schema']
    tabelas = bkp['tabelas']
    
    DESTINO = Path("./")
    data = datetime.datetime.now().strftime("%d-%m-%Y")
    arquivo_gz = f"./bkps/{schema}_{data}.gz"

    logging.info('Dump do schema: %s...', schema)
    arquivos_para_zip = []
    for tabela in tabelas:
        comando_dump = ["mysqldump", "-u", usuario, f"-p{senha}", '-h', host, '-P', porta, schema, tabela]
        arquivo_sql = DESTINO / f"{schema}_{tabela}_{data}.sql"
        arquivos_para_zip.append(arquivo_sql)
        
        # Executa mysqldump e salva ZIP
        try:
            with open(arquivo_sql, "w") as f:
                subprocess.run(
                    comando_dump,
                    stdout=f,
                    check=True
                )
        except:
            logging.critical('FALHA no BKP %s -> %s', schema, tabela)
    

    with zipfile.ZipFile(arquivo_gz, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for arquivo in arquivos_para_zip:
            arcname = os.path.basename(arquivo).replace(f'{schema}_', '').replace(f'_{data}', '')
            zipf.write(arquivo, arcname=arcname)

    logging.info('FINISH!')


# Configurações
MEUS_BKPS = {
    'localhost': {
        'host': 'db',
        'porta': '3306',
        'usuario': 'root', 
        'senha': 'admin',
        'schema': 'schema_exemplo_1',
        'tabelas': ['tbl1', 'tbl2']
    },
    'new': {
        'host': '',
        'porta': '',
        'usuario': '',
        'senha': '',
        'schema': '',
        'tabelas': ['', '']
    },
}

# TZ está UTC no dockerfile - para configuração do schedule
schedule.every().friday.at("02:55").do(dump, bkp=MEUS_BKPS['localhost']) 
# schedule.every().tuesday.do(dump, bkp=MEUS_BKPS['localhost'])
# schedule.every().sunday.do(dump, bkp=MEUS_BKPS['localhost'])

logging.info('BKP Schedulado init...')
while True:
    schedule.run_pending()
    time.sleep(10)
