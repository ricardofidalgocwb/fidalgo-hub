#!/bin/bash

# Fidalgo Hub - Script de Setup Local
# Este script configura o ambiente local para desenvolvimento

set -e

echo "🚀 Iniciando setup do Fidalgo Hub..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale Python 3.11+"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Criar ambiente virtual
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate || . venv/Scripts/activate

# Atualizar pip
echo "📥 Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -r requirements.txt

# Criar arquivo .env se não existir
if [ ! -f ".env" ]; then
    echo "📝 Criando arquivo .env..."
    cp .env.example .env
    echo "⚠️  Por favor, edite o arquivo .env com seus valores"
fi

echo ""
echo "✅ Setup concluído com sucesso!"
echo ""
echo "🎯 Próximos passos:"
echo "1. Edite o arquivo .env com seus valores"
echo "2. Execute: python validate_and_sync_notion_v2_final.py --input template_dados_completo.json"
echo "3. Para sair do ambiente virtual: deactivate"
echo ""
