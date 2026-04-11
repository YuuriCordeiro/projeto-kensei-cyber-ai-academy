# Aula 3 - Análise de Dados e Visualização de Ameaças

Esta etapa do projeto foca na transformação de logs brutos de ataques cibernéticos em inteligência acionável. O objetivo é limpar dados ruidosos e gerar visualizações que permitam identificar padrões de ataques.

## Conteúdo da Aula

- **`analyze_cybersecurity_attacks.py`**: Script de ETL (Extração, Transformação e Carga).
    - Realiza a limpeza do dataset original.
    - Trata valores nulos em colunas críticas como `Payload Data` e `Malware Indicators`.
    - Valida intervalos de portas de rede (0-65535) e converte timestamps.
    - Remove duplicatas para garantir a integridade estatística.

- **`ddos_analysis.py`**: Script de análise específica e geração de gráficos.
    - Filtra ataques do tipo DDoS ocorridos no último mês de registro.
    - Agrupa dados geograficamente para identificar origens de ataques.
    - Gera visualizações automáticas em formato PNG.

## Gráficos Gerados

1. **`top_10_paises_ddos.png`**: Identifica as regiões com maior volume de tráfego malicioso de negação de serviço.
2. **`ataques_por_mes.png`**: Mostra a tendência temporal, permitindo identificar picos de atividade hacker ao longo do ano.
3. **`tipos_ataque_distribuicao.png`**: Um panorama global da proporção entre Malware, DDoS, Intrusion e outras ameaças.

## Conclusões da Análise

- **Qualidade de Dados**: A limpeza inicial reduziu o ruído do dataset, tratando portas inválidas e campos vazios que poderiam enviesar modelos de IA no futuro.
- **Geolocalização**: A extração da região através do campo de localização permitiu observar que os ataques não são distribuídos uniformemente, sugerindo a necessidade de políticas de Geo-blocking em firewalls para regiões específicas.
- **Sazonalidade**: A análise de linha do tempo ajuda a equipe de Blue Team (defesa) a prever períodos de maior criticidade.
- **Predomínio de Ameaças**: O gráfico de pizza revela qual vetor de ataque é mais comum, orientando o investimento em ferramentas de defesa (ex: focar em anti-DDoS ou EDR para Malware).

## Como Executar

1. Garanta que o ambiente virtual está ativo.
2. Execute a limpeza:
   ```bash
   python aula-3/analyze_cybersecurity_attacks.py
   ```
3. Gere os gráficos:
   ```bash
   python aula-3/ddos_analysis.py
   ```