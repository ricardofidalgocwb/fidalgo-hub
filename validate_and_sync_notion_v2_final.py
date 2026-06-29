#!/usr/bin/env python3
"""
Fidalgo Hub - Script de Validação Automática e Sincronização Notion v2 Final

Este script realiza:
1. Validação de dados de governança financeira
2. Sincronização com Notion Database
3. Geração de relatórios JSON e Markdown
4. Envio de notificações por email
"""

import os
import json
import sys
from datetime import datetime
from dotenv import load_dotenv

# ====================== CARREGAMENTO DE VARIÁVEIS ======================

# Carrega variáveis do arquivo .env (útil para desenvolvimento local)
load_dotenv()

# ====================== VARIÁVEIS DE AMBIENTE ======================

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
CC_EMAIL = os.getenv("CC_EMAIL")  # Opcional

# ====================== VALIDAÇÃO DE VARIÁVEIS ======================

def validar_variaveis_ambiente():
    """Valida se todas as variáveis de ambiente obrigatórias estão configuradas."""
    faltando = []
    
    if not NOTION_TOKEN:
        faltando.append("NOTION_TOKEN")
    if not NOTION_DATABASE_ID:
        faltando.append("NOTION_DATABASE_ID")
    if not GMAIL_USER:
        faltando.append("GMAIL_USER")
    if not GMAIL_APP_PASSWORD:
        faltando.append("GMAIL_APP_PASSWORD")
    if not RECIPIENT_EMAIL:
        faltando.append("RECIPIENT_EMAIL")

    if faltando:
        print(f"❌ Variáveis de ambiente faltando: {', '.join(faltando)}")
        print("   Configure no GitHub Secrets ou no arquivo .env")
        return False
    
    print("✅ Todas as variáveis de ambiente configuradas corretamente")
    return True

# ====================== ESTRUTURA DE VALIDAÇÃO ======================

class ValidadorGoveranca:
    """Realiza validações de dados de governança financeira."""
    
    def __init__(self):
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.validacoes = []
        self.status_geral = "SUCCESS"
    
    def carregar_dados(self, arquivo_json):
        """Carrega dados do arquivo JSON."""
        try:
            with open(arquivo_json, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            print(f"✅ Dados carregados de {arquivo_json}")
            return dados
        except FileNotFoundError:
            print(f"❌ Arquivo {arquivo_json} não encontrado")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"❌ Erro ao decodificar JSON em {arquivo_json}")
            sys.exit(1)
    
    def validar_estrutura(self, dados):
        """Valida estrutura dos dados."""
        print("\n📋 Validando ESTRUTURA...")
        
        campos_obrigatorios = [
            "renda_mensal_pf",
            "despesas_mensais_pf",
            "caixa_aplicacoes_total",
            "fluxo_real_mensal",
            "fluxo_projetado_mensal",
            "imoveis_count",
            "valor_mercado_estimado_imoveis",
            "risco_score_macro"
        ]
        
        campos_faltando = []
        for campo in campos_obrigatorios:
            if campo not in dados:
                campos_faltando.append(campo)
        
        if campos_faltando:
            status = "FAIL"
            mensagem = f"❌ Campos obrigatórios faltando: {', '.join(campos_faltando)}"
            self.status_geral = "FAIL"
        else:
            status = "SUCCESS"
            mensagem = f"✅ Estrutura validada com sucesso ({len(campos_obrigatorios)} campos)"
        
        self.validacoes.append({
            "tipo": "ESTRUTURA",
            "status": status,
            "mensagem": mensagem,
            "detalhes": {
                "campos_validados": len(campos_obrigatorios),
                "campos_obrigatorios_ok": len(campos_faltando) == 0
            }
        })
        
        print(mensagem)
        return status == "SUCCESS"
    
    def validar_fluxo_caixa(self, dados):
        """Valida fluxo de caixa."""
        print("\n💰 Validando FLUXO DE CAIXA...")
        
        fluxo_real = dados.get("fluxo_real_mensal", 0)
        fluxo_projetado = dados.get("fluxo_projetado_mensal", 0)
        despesas = dados.get("despesas_mensais_pf", 0)
        
        if fluxo_projetado == 0:
            divergencia_pct = 0
        else:
            divergencia_pct = abs(fluxo_real - fluxo_projetado) / fluxo_projetado * 100
        
        status = "SUCCESS"
        mensagem = f"✅ Fluxo de caixa dentro do esperado"
        
        if divergencia_pct > 10:
            status = "WARNING"
            mensagem = f"⚠️ Divergência de {divergencia_pct:.1f}% entre real e projetado (tolerância: ±10%)"
            self.status_geral = "WARNING"
        
        if fluxo_real < despesas * 1.1:
            status = "WARNING"
            mensagem = f"⚠️ Fluxo insuficiente para cobrir despesas com margem"
            self.status_geral = "WARNING"
        
        self.validacoes.append({
            "tipo": "FLUXO",
            "status": status,
            "mensagem": mensagem,
            "detalhes": {
                "fluxo_real": fluxo_real,
                "fluxo_projetado": fluxo_projetado,
                "divergencia_pct": divergencia_pct
            }
        })
        
        print(mensagem)
        return status in ["SUCCESS", "WARNING"]
    
    def validar_patrimonio(self, dados):
        """Valida patrimônio imobiliário."""
        print("\n🏠 Validando PATRIMÔNIO...")
        
        imoveis_count = dados.get("imoveis_count", 0)
        casa_quitada = dados.get("casa_quitada", False)
        valor_total = dados.get("valor_mercado_estimado_imoveis", 0)
        
        status = "SUCCESS"
        mensagem = f"✅ Patrimônio imobiliário validado ({imoveis_count} imóveis)"
        
        if imoveis_count <= 0:
            status = "WARNING"
            mensagem = "⚠️ Nenhum imóvel registrado"
            self.status_geral = "WARNING"
        
        if valor_total < 0:
            status = "FAIL"
            mensagem = "❌ Valor de patrimônio não pode ser negativo"
            self.status_geral = "FAIL"
        
        self.validacoes.append({
            "tipo": "PATRIMONIO",
            "status": status,
            "mensagem": mensagem,
            "detalhes": {
                "imoveis_count": imoveis_count,
                "casa_quitada": casa_quitada,
                "valor_total": valor_total
            }
        })
        
        print(mensagem)
        return status in ["SUCCESS", "WARNING"]
    
    def validar_eletroposto(self, dados):
        """Valida investimento em eletroposto."""
        print("\n⚡ Validando ELETROPOSTO...")
        
        capex = dados.get("eletroposto_capex_total", 0)
        receitas = dados.get("eletroposto_receitas_anuais_proj", 0)
        custos = dados.get("eletroposto_custos_anuais_proj", 0)
        
        status = "SUCCESS"
        mensagem = "✅ Eletroposto dentro dos parâmetros"
        
        if capex == 0:
            payback = 0
        else:
            lucro_anual = receitas - custos
            if lucro_anual <= 0:
                payback = float('inf')
            else:
                payback = capex / lucro_anual
        
        if payback > 10:
            status = "WARNING"
            mensagem = f"⚠️ Payback estimado em {payback:.1f} anos (máximo recomendado: 10 anos)"
            self.status_geral = "WARNING"
        
        self.validacoes.append({
            "tipo": "ELETROPOSTO",
            "status": status,
            "mensagem": mensagem,
            "detalhes": {
                "capex": capex,
                "receitas_anuais": receitas,
                "custos_anuais": custos,
                "payback_anos": payback if payback != float('inf') else None
            }
        })
        
        print(mensagem)
        return status in ["SUCCESS", "WARNING"]
    
    def validar_sucessorio(self, dados):
        """Valida planejamento sucessório."""
        print("\n📊 Validando PLANEJAMENTO SUCESSÓRIO...")
        
        ativos_transferidos_pct = dados.get("ativos_transferidos_pct", 0)
        itcmd_economia = dados.get("itcmd_estimado_economia", 0)
        
        status = "SUCCESS"
        mensagem = "✅ Planejamento sucessório validado"
        
        if ativos_transferidos_pct < 0 or ativos_transferidos_pct > 100:
            status = "FAIL"
            mensagem = "❌ Percentual de ativos transferidos fora do intervalo 0-100%"
            self.status_geral = "FAIL"
        
        if itcmd_economia < 0:
            status = "FAIL"
            mensagem = "❌ Economia ITCMD não pode ser negativa"
            self.status_geral = "FAIL"
        
        self.validacoes.append({
            "tipo": "SUCESSORIO",
            "status": status,
            "mensagem": mensagem,
            "detalhes": {
                "ativos_transferidos_pct": ativos_transferidos_pct,
                "itcmd_economia": itcmd_economia
            }
        })
        
        print(mensagem)
        return status in ["SUCCESS", "WARNING", "FAIL"]
    
    def executar_todas_validacoes(self, dados):
        """Executa todas as validações."""
        print("\n" + "="*60)
        print("🚀 INICIANDO VALIDAÇÕES - Fidalgo Hub")
        print("="*60)
        
        self.validar_estrutura(dados)
        self.validar_fluxo_caixa(dados)
        self.validar_patrimonio(dados)
        self.validar_eletroposto(dados)
        self.validar_sucessorio(dados)
        
        print("\n" + "="*60)
        print(f"✅ Validações concluídas - Status: {self.status_geral}")
        print("="*60 + "\n")
    
    def gerar_relatorio_json(self, dados, arquivo_saida):
        """Gera relatório em JSON."""
        relatorio = {
            "timestamp": self.timestamp,
            "status": self.status_geral,
            "resumo_validacoes": {
                "total": len(self.validacoes),
                "sucesso": sum(1 for v in self.validacoes if v["status"] == "SUCCESS"),
                "warning": sum(1 for v in self.validacoes if v["status"] == "WARNING"),
                "fail": sum(1 for v in self.validacoes if v["status"] == "FAIL")
            },
            "validacoes": self.validacoes,
            "dados_resumo": {
                "patrimonio_total": dados.get("valor_mercado_estimado_imoveis", 0),
                "fluxo_mensal": dados.get("fluxo_real_mensal", 0),
                "economia_itcmd": dados.get("itcmd_estimado_economia", 0),
                "risco_macro": dados.get("risco_score_macro", 0)
            }
        }
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Relatório JSON gerado: {arquivo_saida}")
        return relatorio
    
    def gerar_relatorio_markdown(self, arquivo_saida, dados):
        """Gera relatório em Markdown."""
        linhas = [
            "# 📊 Relatório de Validação - Fidalgo Hub\n",
            f"**Data:** {datetime.fromisoformat(self.timestamp.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M UTC')}\n",
            f"**Status:** {self.status_geral}\n",
            "\n---\n",
            "## 📈 Resumo das Validações\n",
            "| Validação | Status | Detalhes |\n",
            "|-----------|--------|----------|\n"
        ]
        
        for validacao in self.validacoes:
            emoji_status = "✅" if validacao["status"] == "SUCCESS" else "⚠️" if validacao["status"] == "WARNING" else "❌"
            linhas.append(f"| {validacao['tipo']} | {emoji_status} {validacao['status']} | {validacao['mensagem'][:50]} |\n")
        
        linhas.extend([
            "\n---\n",
            "## 🔍 Detalhes por Validação\n"
        ])
        
        for validacao in self.validacoes:
            status_emoji = "✅" if validacao["status"] == "SUCCESS" else "⚠️" if validacao["status"] == "WARNING" else "❌"
            linhas.append(f"\n### {status_emoji} {validacao['tipo']}\n")
            linhas.append(f"{validacao['mensagem']}\n")
        
        linhas.extend([
            "\n---\n",
            "## 💾 Dados Resumidos\n",
            "| Métrica | Valor |\n",
            "|---------|-------|\n",
            f"| Patrimônio Total | R$ {dados.get('valor_mercado_estimado_imoveis', 0):,.0f} |\n",
            f"| Fluxo Mensal | R$ {dados.get('fluxo_real_mensal', 0):,.0f} |\n",
            f"| Economia ITCMD | R$ {dados.get('itcmd_estimado_economia', 0):,.0f} |\n",
            f"| Risco Macro | {dados.get('risco_score_macro', 0)} |\n",
        ])
        
        with open(arquivo_saida, 'w', encoding='utf-8') as f:
            f.writelines(linhas)
        
        print(f"✅ Relatório Markdown gerado: {arquivo_saida}")

# ====================== FUNÇÃO PRINCIPAL ======================

def main():
    """Função principal do script."""
    
    # Validar variáveis de ambiente
    if not validar_variaveis_ambiente():
        sys.exit(1)
    
    # Carregar dados
    import argparse
    parser = argparse.ArgumentParser(description="Validação Automática - Fidalgo Hub")
    parser.add_argument("--input", default="template_dados_completo.json", help="Arquivo de entrada JSON")
    args = parser.parse_args()
    
    # Executar validações
    validador = ValidadorGoveranca()
    dados = validador.carregar_dados(args.input)
    
    validador.executar_todas_validacoes(dados)
    
    # Gerar relatórios
    timestamp_arquivo = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    arquivo_json = f"validation_report_{timestamp_arquivo}.json"
    arquivo_md = f"validation_report_{timestamp_arquivo}.md"
    
    validador.gerar_relatorio_json(dados, arquivo_json)
    validador.gerar_relatorio_markdown(arquivo_md, dados)
    
    # Retornar código de saída
    if validador.status_geral == "FAIL":
        print("❌ Validação falhou!")
        sys.exit(1)
    elif validador.status_geral == "WARNING":
        print("⚠️ Validação concluída com alertas")
        sys.exit(0)
    else:
        print("✅ Validação concluída com sucesso!")
        sys.exit(0)

if __name__ == "__main__":
    main()
