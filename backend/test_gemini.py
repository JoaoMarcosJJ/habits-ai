import os
import google.generativeai as genai

# Tenta ler a chave diretamente do ambiente
api_key = os.getenv("GEMINI_API_KEY")

print("--- DIAGNÓSTICO DO GEMINI ---")

if not api_key:
    print("❌ ERRO CRÍTICO: A variável GEMINI_API_KEY não foi encontrada!")
    print("Verifique se ela está no arquivo .env e no docker-compose.yml")
    exit(1)

print(f"✅ API Key encontrada: {api_key[:5]}...{api_key[-5:]}")

try:
    genai.configure(api_key=api_key)
    
    print("\n1. Testando conexão e listando modelos disponíveis...")
    found_flash = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"   - {m.name}")
            if 'gemini-1.5-flash' in m.name:
                found_flash = True

    if found_flash:
        print("\n✅ Modelo 'gemini-1.5-flash' está disponível para sua chave!")
    else:
        print("\n⚠️ AVISO: 'gemini-1.5-flash' não apareceu na lista. Talvez sua chave não tenha acesso.")

    print("\n2. Tentando gerar uma resposta simples...")
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Responda apenas com: O sistema está a funcionar.")
    
    print(f"\n🤖 RESPOSTA DA IA: {response.text}")
    print("\n✅ SUCESSO TOTAL! O problema não é a conexão nem a chave.")

except Exception as e:
    print(f"\n❌ FALHA NO TESTE: {e}")
    print("\nPossíveis causas:")
    print("- Nome do modelo errado (se for 404)")
    print("- Chave inválida ou sem permissão (se for 400/403)")
    print("- Bloqueio de rede/firewall (se for timeout)")