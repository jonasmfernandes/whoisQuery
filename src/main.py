import time
import whois

input_file = "domainList.txt"
error_file = "error_whois_domainList.txt"
output_file = "whois_results_domainList.txt"

with open (input_file) as f:
    domains = [line.strip() for line in f.readlines()]

with open(output_file, "w", encoding = "utf-8") as result_file, open(error_file, "w") as err_file:
    for domain in domains:
        try:
            print("WHOIS para: {domain}")
            w = whois.whois(domain)
            result_file.write(f"WHOIS DE {domain} \n{w}\n\n")
            print(f"Consulta de {domain} finalizada.")
        except Exception as e:
            err_file.write(f"{domain}: {e}\n")
            print(f"Erro ao consultar WHOIS {domain}: {e}")
            time.sleep(1)

print(f"Pesquisa encerrada. Os protocolos WHOIS foram salvos em '{output_file}' e os erros em '{error_file}'.")