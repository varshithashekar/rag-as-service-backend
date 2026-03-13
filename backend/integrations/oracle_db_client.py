import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

# initialize wallet connection
oracledb.init_oracle_client(
    config_dir=os.getenv("ORACLE_WALLET_LOCATION")
)

def get_connection():
    return oracledb.connect(
        user=os.getenv("ORACLE_USER"),
        password=os.getenv("ORACLE_PASSWORD"),
        dsn=os.getenv("ORACLE_DSN")
    )