import random

API_URL = "http://127.0.0.1/appstore_wallet/index.php?action=eventos&rand="+str(random.randint(1, 2000))
API_URL_COMPRAR = "http://127.0.0.1/appstore_wallet/index.php?action=comprar"
API_MEUS_INGRESSOS = "http://127.0.0.1/appstore_wallet/index.php?action=meus_ingressos"
LOGIN_API = "http://127.0.0.1/appstore_wallet/login.php"
CADASTRO_API = "http://127.0.0.1/appstore_wallet/cadastro.php"
