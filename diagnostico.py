"""
🔧 Teste Simplificado do Sistema
Diagnóstico básico para identificar problemas
"""

print("🔧 DIAGNÓSTICO SIMPLIFICADO")
print("=" * 40)

# Teste 1: Python básico
print("\n1. Testando Python básico...")
try:
    import sys
    print(f"✅ Python {sys.version[:5]} funcionando")
except Exception as e:
    print(f"❌ Erro Python: {e}")

# Teste 2: Bibliotecas básicas
print("\n2. Testando bibliotecas básicas...")

bibliotecas = [
    ('pandas', 'pd'),
    ('numpy', 'np'),
    ('matplotlib.pyplot', 'plt'),
    ('seaborn', 'sns'),
]

for lib_nome, alias in bibliotecas:
    try:
        exec(f"import {lib_nome} as {alias}")
        print(f"✅ {lib_nome}: OK")
    except ImportError as e:
        print(f"❌ {lib_nome}: FALTANDO - {e}")
    except Exception as e:
        print(f"⚠️ {lib_nome}: ERRO - {e}")

# Teste 3: Bibliotecas avançadas
print("\n3. Testando bibliotecas avançadas...")

bibliotecas_avancadas = [
    'plotly.express',
    'sklearn.ensemble',
    'scipy.stats'
]

for lib in bibliotecas_avancadas:
    try:
        exec(f"import {lib}")
        print(f"✅ {lib}: OK")
    except ImportError as e:
        print(f"❌ {lib}: FALTANDO - {e}")
    except Exception as e:
        print(f"⚠️ {lib}: ERRO - {e}")

# Teste 4: Arquivo principal
print("\n4. Testando arquivo principal...")
try:
    with open('analise_temporal.py', 'r', encoding='utf-8') as f:
        conteudo = f.read()
    print(f"✅ Arquivo analise_temporal.py existe ({len(conteudo)} chars)")
    
    # Verificar se contém a classe
    if 'class AnaliseMeteorolgicaRS' in conteudo:
        print("✅ Classe AnaliseMeteorolgicaRS encontrada")
    else:
        print("❌ Classe AnaliseMeteorolgicaRS NÃO encontrada")
        
except FileNotFoundError:
    print("❌ Arquivo analise_temporal.py NÃO encontrado")
except Exception as e:
    print(f"⚠️ Erro ao ler arquivo: {e}")

# Teste 5: Tentar importar a classe
print("\n5. Testando importação da classe...")
try:
    from analise_temporal import AnaliseMeteorolgicaRS
    print("✅ Importação da classe: OK")
    
    # Tentar instanciar
    try:
        analise = AnaliseMeteorolgicaRS()
        print("✅ Instanciação da classe: OK")
    except Exception as e:
        print(f"❌ Erro na instanciação: {e}")
        
except ImportError as e:
    print(f"❌ Erro na importação: {e}")
except Exception as e:
    print(f"⚠️ Erro inesperado: {e}")

print("\n" + "=" * 40)
print("🏁 DIAGNÓSTICO CONCLUÍDO")
print("=" * 40)
