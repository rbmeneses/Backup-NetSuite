# Backup NetSuite

Uma ferramenta para realizar o backup de arquivos e pastas do NetSuite utilizando a API REST e OAuth1.

## Descrição

Este script automatiza o backup de arquivos do NetSuite. Ele se conecta à API REST (RESTlets) do NetSuite utilizando OAuth1, recupera a estrutura de pastas e realiza o download dos arquivos de forma recursiva. Uma interface gráfica (GUI) construída com Tkinter facilita a inserção de credenciais e a seleção do diretório de destino para o backup.

## Funcionalidades

- **Autenticação OAuth1:** Conecta à API do NetSuite de forma segura utilizando as credenciais fornecidas.
- **Recuperação da Estrutura de Pastas:** Identifica o ID da pasta raiz e lista conteúdos (pastas e arquivos) de forma recursiva.
- **Download de Arquivos:** Faz o download dos arquivos em chunks, permitindo o manuseio de arquivos grandes.
- **Interface Gráfica (GUI):** Facilita a entrada de credenciais e a escolha do diretório de destino.
- **Logs Detalhados:** Registra todo o processo em arquivos de log salvos na pasta `logs` dentro do diretório de destino.

## Pré-requisitos

- **Python 3.x**

### Bibliotecas Necessárias

- `requests`
- `requests_oauthlib`
- `tkinter` (geralmente incluído com o Python)

Para instalar as dependências, execute:

```bash
pip install requests requests_oauthlib
```

## Configuração

Antes de executar o script, obtenha as seguintes informações da sua conta NetSuite:

- **Account ID:** (exemplo: `123456`)
- **Consumer Key**
- **Consumer Secret**
- **Token Key**
- **Token Secret**

Certifique-se de que as credenciais estejam corretas e que a API REST esteja devidamente configurada em sua conta NetSuite.

## Como Usar

1. **Clone o Repositório:**

   ```bash
   git clone https://github.com/rbmeneses/Backup-NetSuite.git
   ```

2. **Navegue até o Diretório do Projeto:**

   ```bash
   cd backup-netsuite
   ```

3. **Execute o Script:**

   ```bash
   python Bkp_Netsuit_suite3.py
   ```

4. **Utilize a Interface Gráfica:**
   - Insira as credenciais solicitadas (Account ID, Consumer Key, Consumer Secret, Token Key, Token Secret).
   - Selecione a **Pasta de Destino** onde os arquivos serão salvos.
   - Clique em **Iniciar Backup** para iniciar o processo.

Os arquivos serão baixados mantendo a estrutura original de pastas. Os logs do processo serão salvos na subpasta `logs` dentro do diretório de destino.

## Logs

Os arquivos de log são gerados automaticamente na pasta `logs` do diretório de destino e registram detalhes do processo de backup, facilitando a identificação e resolução de possíveis problemas.

## Tratamento de Erros

Caso ocorra algum erro durante o backup (como falha de conexão ou problemas ao baixar arquivos), uma mensagem de erro será exibida na interface gráfica e registrada no log. Isso ajuda na identificação e correção rápida dos problemas.

## Contribuições

Contribuições são bem-vindas! Se você deseja melhorar este projeto ou reportar problemas, por favor, abra uma _issue_ ou envie um _pull request_.

## Licença

Este projeto está licenciado sob a licença [MIT](LICENSE). Consulte o arquivo `LICENSE` para mais informações.

---

Este README foi criado para facilitar a compreensão e utilização do script de backup do NetSuite. Sinta-se à vontade para adaptá-lo conforme as necessidades do projeto.
