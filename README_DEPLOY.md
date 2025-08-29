# Guia de Deploy no Render - Banco de Questões

## Estrutura do Projeto
Este é um aplicativo full-stack com:
- **Backend**: Python Flask (API + servidor de arquivos estáticos)
- **Frontend**: React com Vite
- **Banco de dados**: SQLite

## Arquivos de Configuração Criados

### 1. `render.yaml`
Arquivo de configuração principal do Render que define:
- Tipo de serviço (web)
- Comandos de build
- Comando de start
- Variáveis de ambiente

### 2. `build.sh`
Script que automatiza o processo de build:
- Instala dependências do Python
- Instala Node.js e pnpm
- Faz build do frontend React
- Copia arquivos buildados para o diretório static do Flask

### 3. `Procfile`
Define como o Render deve iniciar a aplicação

### 4. `runtime.txt`
Especifica a versão do Python a ser usada

## Passos para Deploy no Render

### 1. Preparar o Repositório
Certifique-se de que todos os arquivos estão commitados no seu repositório GitHub:

```bash
git add .
git commit -m "Adicionar configurações de deploy para Render"
git push origin main
```

### 2. Configurar no Render
1. Acesse [render.com](https://render.com)
2. Faça login com sua conta GitHub
3. Clique em "New +" → "Web Service"
4. Conecte seu repositório `banco-questoes-mvp-5`
5. Configure as seguintes opções:

**Configurações Básicas:**
- **Name**: `banco-questoes-mvp-5`
- **Environment**: `Python`
- **Region**: `Oregon (US West)` ou `Frankfurt (EU Central)`
- **Branch**: `main`

**Comandos de Build e Start:**
- **Build Command**: `./build.sh`
- **Start Command**: `python src/main.py`

**Configurações Avançadas:**
- **Python Version**: `3.11.0`
- **Auto-Deploy**: `Yes` (para deploy automático quando fizer push)

### 3. Variáveis de Ambiente (se necessário)
Se precisar de variáveis de ambiente específicas, adicione na seção "Environment Variables":
- `PORT`: será definido automaticamente pelo Render
- Outras variáveis conforme necessário

### 4. Deploy
1. Clique em "Create Web Service"
2. O Render começará o processo de build automaticamente
3. Aguarde o build completar (pode levar alguns minutos)
4. Quando concluído, você receberá uma URL pública para acessar sua aplicação

## Estrutura Final dos Arquivos

```
banco-questoes-mvp-5/
├── frontend/                 # Código fonte do React
│   ├── src/
│   ├── package.json
│   └── ...
├── src/                     # Código fonte do Flask
│   ├── main.py             # Arquivo principal
│   ├── models/
│   ├── routes/
│   ├── database/
│   └── static/             # Arquivos buildados do React (criado automaticamente)
├── build.sh                # Script de build
├── Procfile                # Configuração de processo
├── render.yaml             # Configuração do Render
├── requirements.txt        # Dependências Python
├── runtime.txt            # Versão do Python
└── README_DEPLOY.md       # Este arquivo
```

## Troubleshooting

### Build Falha
- Verifique os logs de build no dashboard do Render
- Certifique-se de que o `build.sh` tem permissões de execução
- Verifique se todas as dependências estão listadas corretamente

### Aplicação não Carrega
- Verifique se o Flask está configurado para servir arquivos estáticos
- Confirme se os arquivos do React foram copiados para `src/static/`
- Verifique os logs da aplicação no dashboard do Render

### Problemas de CORS
- O Flask já está configurado com CORS habilitado
- Se necessário, ajuste as configurações em `src/main.py`

## Próximos Passos
Após o deploy bem-sucedido:
1. Teste todas as funcionalidades da aplicação
2. Configure um domínio personalizado (opcional)
3. Configure monitoramento e alertas
4. Considere usar um banco de dados PostgreSQL para produção (opcional)

