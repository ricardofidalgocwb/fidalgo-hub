#!/bin/bash

# Fidalgo Hub - Script de Teste Local
# Executa validações localmente sem GitHub Actions

set -e

echo "🧪 Iniciando testes locais do Fidalgo Hub..."
echo ""

# Verificar se o .env existe
if [ ! -f ".env" ]; then
    echo "❌ Arquivo .env não encontrado"
    echo "Por favor, copie .env.example para .env e configure"
    exit 1
fi

# Carregar variáveis de ambiente
export $(cat .env | grep -v '^#' | xargs)

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado"
    exit 1
fi

# Verificar se o script existe
if [ ! -f "validate_and_sync_notion_v2_final.py" ]; then
    echo "❌ Script validate_and_sync_notion_v2_final.py não encontrado"
    exit 1
fi

# Verificar se o template existe
if [ ! -f "template_dados_completo.json" ]; then
    echo "❌ Template template_dados_completo.json não encontrado"
    exit 1
fi

echo "✅ Pré-requisitos validados"
echo ""

if command -v python3 >/dev/null && python3 -c "import pytest" 2>/dev/null; then
  echo "🧪 Máquina de status + guarda n8n..."
  python3 -m pytest tests/ -q
  echo ""
fi

# Executar script
echo "🚀 Executando validações..."
echo ""

python3 validate_and_sync_notion_v2_final.py --input template_dados_completo.json

echo ""
echo "✅ Testes concluídos!"
echo ""
echo "📁 Arquivos gerados:"
ls -lh validation_report_*.* validation_output.log 2>/dev/null || echo "Nenhum arquivo gerado"
echo ""
