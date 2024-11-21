import time
import whois
import pandas as pd

input_file = "domainList.txt"
error_file = "error_whois_domainList.txt"
output_file = "whois_results_domainList.csv"

def flatten_json(json_data, prefix=''):
    flat_dict = {}
    for key, value in json_data.items():
        if isinstance(value, dict):
            flat_dict.update(flatten_json(value, f"{prefix}{key}_"))
        elif isinstance(value, list):
            flat_dict[f"{prefix}{key}"] = "; ".join(map(str, value))
        else:
            flat_dict[f"{prefix}{key}"] = value
    return flat_dict

domains = [line.strip() for line in open(input_file).readlines()]
results = []
errors = []

for domain in domains:
    try:
        print(f"WHOIS para: {domain}")
        w = whois.whois(domain)
        flat_data = flatten_json(w)
        flat_data["Domain"] = domain
        results.append(flat_data)
        print(f"Consulta de {domain} finalizada.")
    except Exception as e:
        errors.append({"Domain": domain, "Error": str(e)})
        print(f"Erro ao consultar WHOIS {domain}: {e}")
        time.sleep(1)

df_results = pd.DataFrame(results)
df_results.to_csv(output_file, index=False)

if errors:
    df_errors = pd.DataFrame(errors)
    df_errors.to_csv(error_file, index=False)

print(f"Pesquisa encerrada. Os protocolos WHOIS foram salvos em '{output_file}' e os erros em '{error_file}'.")
