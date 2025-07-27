# 🚀 Deploy no Railway - Guia Passo a Passo

## Pré-requisitos

1. ✅ Conta no [Railway](https://railway.app)
2. ✅ Repositório no GitHub/GitLab com o código
3. ✅ Tokens do GLPI configurados

## Passos para Deploy

### 1. 📁 Preparar Repositório

```bash
# Se ainda não fez, faça push para GitHub/GitLab
git remote add origin https://github.com/seu-usuario/seu-repo.git
git push -u origin main
```

### 2. 🛤️ Configurar no Railway

1. **Acesse [Railway](https://railway.app) e faça login**

2. **Criar novo projeto:**
   - Clique em "New Project"
   - Selecione "Deploy from GitHub repo"
   - Escolha seu repositório

3. **Railway detectará automaticamente:**
   - ✅ `pyproject.toml` (Poetry)
   - ✅ `Procfile` (comando: `poetry run start`)
   - ✅ Python 3.12

### 3. ⚙️ Configurar Variáveis de Ambiente

No dashboard do Railway, vá em **Variables** e adicione:

```bash
GLPI_BASE_URL=https://seu-glpi-server.com/apirest.php
GLPI_APP_TOKEN=seu_app_token_aqui
GLPI_USER_TOKEN=seu_user_token_aqui
```

**⚠️ IMPORTANTE:** Não adicione `PORT` - o Railway configura automaticamente.

### 4. 🚀 Deploy

1. **Deploy automático** acontece após configurar as variáveis
2. **Acompanhe os logs** na aba "Deployments"
3. **URL será gerada** automaticamente (ex: `https://seu-app.railway.app`)

### 5. ✅ Testar Deploy

```bash
# Teste o endpoint principal
curl https://seu-app.railway.app/

# Teste listagem de tickets (se GLPI estiver configurado)
curl https://seu-app.railway.app/tickets
```

## 📋 Checklist de Verificação

- [ ] Código commitado e pushado para GitHub/GitLab
- [ ] Projeto criado no Railway
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy realizado com sucesso
- [ ] API respondendo na URL do Railway
- [ ] Conexão com GLPI funcionando

## 🔄 Deploys Futuros

Após configuração inicial:
1. **Faça mudanças no código**
2. **Commit e push para main**
3. **Deploy automático** acontece em ~2-3 minutos

## 🐛 Troubleshooting

### Erro: "Application failed to respond"
- Verifique se as variáveis de ambiente estão corretas
- Confirme se o GLPI está acessível publicamente

### Erro: "Build failed"
- Verifique os logs de build no Railway
- Confirme se `pyproject.toml` está correto

### Erro: "Poetry not found"
- O Railway detecta automaticamente Poetry via `pyproject.toml`
- Se persistir, adicione `runtime.txt` com `python-3.12`

## 💡 Dicas

1. **Logs em tempo real:** Use a aba "Logs" no Railway
2. **Monitoramento:** Railway fornece métricas automáticas
3. **Domínio customizado:** Disponível nos planos pagos
4. **Variables por ambiente:** Use diferentes tokens para dev/prod

## 🎉 Pronto!

Sua API Python está rodando em produção no Railway! 🚀