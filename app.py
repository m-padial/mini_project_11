import pandas as pd
import requests

url = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html"
response = requests.get(url, verify=False)  # ¡Esto desactiva la verificación SSL!

# Advertencia: Esto puede lanzar una advertencia que puedes ignorar o suprimir si quieres
df = pd.read_html(response.text, attrs={'class': "forextable"})[0]
df = df.iloc[:, [0, 2]]

print(df)
