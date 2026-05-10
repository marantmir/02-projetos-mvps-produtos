# PRD — Radar Cultural AI

## 1. Visão

Criar uma plataforma de inteligência cultural que transforma dados de comportamento digital em recomendações práticas para produção de conteúdo.

O produto não deve ser apenas um dashboard. Ele deve funcionar como um copiloto estratégico para creators, produtores musicais, agências, marcas e times de marketing.

## 2. Problema

Produtores de conteúdo decidem com base em feeling, tendências isoladas e leitura manual de plataformas. Isso gera atraso, baixa previsibilidade e pouca capacidade de escalar a criação.

## 3. Proposta de valor

Unificar sinais de várias plataformas, calcular oportunidade, explicar o motivo da recomendação e gerar um brief criativo pronto para teste.

## 4. Funcionalidades principais

### 4.1 Radar de tendências
- Integra Spotify, YouTube, Google Trends e X.
- Calcula sinais de popularidade, engajamento, crescimento, volume social e novidade.
- Apresenta ranking por score de oportunidade.

### 4.2 Motor de recomendação explicável
- Score de 0 a 100.
- Priorização: Monitorar, Testar, Priorizar, Apostar forte.
- Explicação por fonte e dimensão.

### 4.3 IA criativa
- Gera gancho, roteiro, formato e experimento.
- Pode ser conectado a LLM via API.
- Mantém humanos no controle da decisão final.

### 4.4 Aprendizado contínuo
- Captura resultado real do conteúdo publicado.
- Ajusta pesos do score com feedback.
- Evolui para modelo preditivo com dados históricos.

## 5. Arquitetura recomendada

### MVP
- Streamlit
- Supabase/Postgres
- Python/pandas
- Plotly
- Scikit-learn
- mlxtend

### Escala
- BigQuery como camada analítica
- Cloud Run para deploy
- Cloud Scheduler para coletas
- Pub/Sub ou fila para jobs assíncronos
- Feature Store para sinais culturais
- Vector DB para embeddings semânticos
- LLM Gateway com política de segurança

## 6. Métricas de sucesso

- Tempo economizado na descoberta de pauta.
- Aumento de taxa de acerto dos conteúdos sugeridos.
- Retenção dos vídeos publicados.
- CTR de títulos e thumbnails.
- Comentários por mil visualizações.
- Compartilhamentos por conteúdo.
- Taxa de adoção das recomendações pelo time.

## 7. Modelo de negócio

### Plano Creator
- Radar simples.
- Top oportunidades.
- Briefs limitados.

### Plano Pro
- Múltiplas fontes.
- Histórico.
- Recomendações personalizadas.
- Exportação.

### Plano Enterprise
- Multiusuário.
- Governança.
- API.
- IA privada.
- Integração com BI e data warehouse.

## 8. Roadmap

### Fase 1 — MVP de decisão
- Refatorar código.
- Criar score proprietário.
- Dashboard executivo.
- Brief automático.

### Fase 2 — Dados reais e governança
- APIs reais.
- Supabase/BigQuery.
- Logs e observabilidade.
- Agendamento automático.

### Fase 3 — IA avançada
- Embeddings para similaridade temática.
- Clusterização semântica.
- Geração de roteiros.
- Feedback loop.

### Fase 4 — Produto SaaS
- Login.
- Planos.
- Multiempresa.
- Billing.
- API externa.
