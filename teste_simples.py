print("🧪 Teste Python Básico")
print("Testando importações...")

# Teste 1: Pandas
try:
    import pandas
    print("✅ Pandas instalado")
except:
    print("❌ Pandas NÃO instalado")

# Teste 2: Numpy  
try:
    import numpy
    print("✅ Numpy instalado")
except:
    print("❌ Numpy NÃO instalado")

# Teste 3: Matplotlib
try:
    import matplotlib
    print("✅ Matplotlib instalado")
except:
    print("❌ Matplotlib NÃO instalado")

print("✅ Teste concluído!")
