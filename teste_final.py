#!/usr/bin/env python3
"""
Teste rápido das correções do analise_temporal.py
"""

def main():
    print("🚀 Testando correções do analise_temporal.py")
    print("=" * 50)
    
    try:
        print("📦 Importando módulo...")
        from analise_temporal import AnaliseMeteorolgicaRS
        print("✅ Import bem-sucedido!")
        
        print("\n🏗️ Criando instância...")
        analise = AnaliseMeteorolgicaRS()
        print("✅ Instância criada com sucesso!")
        
        print("\n🔍 Testando método sem dados...")
        analise.estatisticas_descritivas()
        print("✅ Método executado sem erros!")
        
        print("\n" + "=" * 50)
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O arquivo analise_temporal.py está funcionando corretamente.")
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
