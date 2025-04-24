import pandas as pd
import requests
import datetime
import boto3
from decimal import Decimal

url = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html"
response = requests.get(url, verify=False)  # ¡Esto desactiva la verificación SSL!

# Advertencia: Esto puede lanzar una advertencia que puedes ignorar o suprimir si quieres
df = pd.read_html(response.text, attrs={'class': "forextable"})[0]
df = df.iloc[:, [0, 2]]

print(df)

# Save in bucket
bucket = 'miax13-project-11'
current_date = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
df.to_csv(f"s3://{bucket}/ccy/{current_date}.csv")

df = df.rename(columns={'Currency': 'ISO_CODE'})

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CCY')

records = df.to_dict(orient='records')
for record in records:
    record['DATE'] = current_date
    print(record)
    
    record['Spot'] = Decimal(str(record.get('Spot')))
    response = table.put_item(
        Item=record
    )