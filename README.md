# PortScanner

Este é um simples **scanner de portas TCP** desenvolvido em Python. Ele permite escanear um **host ou uma rede inteira**, identificando **portas abertas, fechadas e filtradas**. Além disso, tenta capturar banners de serviços para identificar o sistema operacional do alvo.

---

## 📌 Funcionalidades:
✅ **Escaneamento de um único host** (IP ou domínio)  
✅ **Escaneamento de uma rede inteira** (formato CIDR)  
✅ **Definição de intervalo de portas**  
✅ **Identificação de serviços conhecidos (Well-Known Ports)**  
✅ **Detecção do estado das portas** (aberta, fechada ou filtrada)  
✅ **Identificação do sistema operacional pelo banner de resposta**  

---

## 🛠️ Como Usar:

1. **Instale as dependências** (caso ainda não tenha o `tabulate` instalado):  
   ```
   pip install -r requirements.txt
   ```

2. **Execute o script:**  
   ```
   python portscanner.py
   ```

3. **Escolha uma opção:**  
   - `1` para escanear um único host  
   - `2` para escanear uma rede inteira  
   - `3` para sair  

4. **Informe o IP/dominio ou rede + intervalo de portas**  
   - Exemplo de host: `192.168.1.1` ou `google.com`  
   - Exemplo de rede: `192.168.1.0/24`  
   - Exemplo de intervalo de portas: `20-100`  

---

## 📌 Exemplo de Saída:

```
Escaneando host 192.168.1.1 nas portas 20-100...

[ABERTA] Porta 22 (SSH) - Banner: OpenSSH_8.0
[ABERTA] Porta 80 (HTTP) - Banner: Apache/2.4.41

+--------+----------+----------------+----------------------+
| Porta  | Serviço  | Banner         | SO                   |
+--------+----------+----------------+----------------------+
| 22     | SSH      | OpenSSH_8.0    | Linux (Ubuntu/Debian)|
| 80     | HTTP     | Apache/2.4.41  | Linux (Apache)       |
+--------+----------+----------------+----------------------+
```

---

## ⚠️ Observações:
- O escaneamento **requer permissões de administrador** para algumas portas.  
- Pode ser **bloqueado por firewalls ou sistemas de segurança**.  
- **Use com responsabilidade!** Não escaneie redes sem permissão.  

---