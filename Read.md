# Rodopar Interface

Aplicação desktop desenvolvida para **automatizar o preenchimento de formulários** em um sistema de gestão logística, eliminando trabalho manual repetitivo e reduzindo erros de digitação em operações de transporte de cargas.

---

## O problema

Operadores precisavam inserir manualmente dezenas de campos em formulários do sistema interno toda vez que um novo documento fiscal chegava — um processo lento, sujeito a erros e que precisava ser repetido centenas de vezes por dia.

## A solução

Uma interface desktop que lê os dados diretamente dos arquivos XML dos documentos fiscais, aplica regras de negócio configuráveis e preenche os formulários automaticamente, campo a campo, sem intervenção humana.

---

## Funcionalidades

- **Extração de dados de XML** — leitura e parsing de documentos fiscais eletrônicos
- **Preenchimento automatizado de formulários** — simulação de teclado e mouse para interagir com o sistema alvo
- **Regras de negócio configuráveis** — toda a lógica variável fica em arquivos JSON editáveis, sem necessidade de alterar o código
- **Monitor de arquivos em background** — detecta novos PDFs gerados e os renomeia automaticamente com base no conteúdo
- **Reconhecimento de tela por template** — localiza elementos da interface do sistema alvo via comparação de imagens em tempo real
- **Alertas inteligentes** — identifica tipos de operação problemáticos e notifica o usuário via áudio e diálogo
- **Verificação automática de versão** — consulta o GitHub Releases e notifica quando há atualização disponível
- **Controle de velocidade** — slider para ajustar o ritmo da automação conforme a performance do sistema alvo

---

## Stack

| Categoria | Tecnologia |
|-----------|-----------|
| GUI | CustomTkinter, tkinter |
| Automação de tela | PyAutoGUI |
| Visão computacional | OpenCV, Pillow |
| Parsing XML | xml.etree.ElementTree |
| Leitura de PDF | pdfplumber, PDFMiner.six |
| Monitoramento de arquivos | watchdog |
| Síntese de voz | pyttsx3 |
| Integração Windows | pywin32 |
| HTTP / API | requests |
| Build / distribuição | PyInstaller |

---

## Arquitetura

```
rodopar_interface_customtk/
├── main.py                 # GUI principal (3 abas de operação)
├── utils.py                # Image matching, teclado, áudio, utilitários
├── pdf_monitor.py          # Thread de monitoramento de pasta
├── version_checker.py      # Verificação de versão via GitHub API
│
├── xml_process/            # Pipeline de extração + preenchimento de formulários
│   ├── XML.py              # Parser e validador de documentos XML
│   ├── cte_xml.py          # Modo completo
│   ├── cte_xml_carga.py    # Modo composição de carga
│   └── cte_xml_geral.py    # Modo simplificado
│
├── ost_dadosfixos/         # Módulos de preenchimento por tipo de terminal
│   └── ost_*.py            # (6 módulos — 2 empresas × 3 modos)
│
├── config/                 # Regras de negócio em JSON (editáveis sem tocar no código)
│   ├── mensagem_rotas.json
│   ├── pagador_frete.json
│   ├── terminal_entrega.json
│   ├── tipo_faturamento.json
│   ├── produtos.json
│   ├── peso_nota.json
│   └── valor_nota.json
│
└── imagens/                # Templates PNG para reconhecimento de tela (100+)
```

---

## Como a automação de tela funciona

O sistema não depende de uma API ou integração direta com o software alvo — ele interage com a interface gráfica da mesma forma que um humano faria:

1. Captura a tela em tempo real
2. Compara regiões com templates PNG pré-salvos usando OpenCV
3. Ao localizar o elemento com confiança acima do limiar definido, simula o clique
4. Digita o valor extraído do XML com timing configurável

Essa abordagem torna a solução aplicável a qualquer sistema que não ofereça API, sem necessidade de acesso ao código-fonte do software alvo.

---

## Destaques técnicos

- **Configuração orientada a dados** — adicionar uma nova rota ou regra de negócio não exige alteração de código, apenas uma linha no JSON correspondente
- **Thread separada para monitoramento** — o monitor de PDFs roda em daemon thread sem bloquear a interface
- **Deduplicação por hash** — MD5 para garantir que arquivos já processados não sejam renomeados novamente
- **Distribuição sem dependências** — empacotado com PyInstaller; o operador recebe um `.exe` e não precisa instalar Python
- **Múltiplos modos de operação** — a mesma base de código suporta 3 workflows diferentes (completo, geral, composição de carga) com módulos intercambiáveis

---

## Resultado

Processo que levava vários minutos por documento passou a ser executado em segundos, com menor taxa de erro e sem demandar atenção contínua do operador durante o preenchimento.
