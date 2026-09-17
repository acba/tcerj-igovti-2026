# Deploy da Fiscalização 18/2026

Esta pasta contém o gerador do pacote final a ser enviado ao sistema do TCE-RJ. A saída reproduz a lista de anexos do relatório consolidado:

- relatório consolidado em DOCX e PDF;
- AN01 a AN11, com os nomes definidos no relatório;
- AN12 a AN124, um ZIP reservado para cada uma das 113 organizações avaliadas;
- manifestos JSON e CSV com tamanho, SHA-256, situação e arquivos faltantes;
- `FALTANTES.md`, para conferência antes do protocolo.

Nenhum ZIP de saída pode ultrapassar 100.000.000 bytes. Quando um anexo excede esse limite, o gerador distribui seu conteúdo entre arquivos ZIP válidos denominados `ANXX – ORGANIZACAO-parte1.zip`, `ANXX – ORGANIZACAO-parte2.zip` e assim por diante. Todas as partes devem ser enviadas e consideradas em conjunto.

Cada ZIP individual contém exclusivamente:

1. TSID01, TSID02 e TSID03 enviados à organização;
2. PDF das respostas ao questionário iGovTI e evidências anexadas;
3. PDF dos comentários do gestor e evidências anexadas, quando houve manifestação;
4. relatório individual final em PDF.

Arquivos obrigatórios não localizados recebem um `ARQUIVO_FALTANTE.txt` dentro do ZIP. A ausência de manifestação do gestor é registrada como `NAO_HOUVE_MANIFESTACAO.txt` e não é tratada como falha do deploy.

## Organização esperada dos TSIDs

Armazene os documentos sob `99-Gestao/02-TSIDs`, identificando a sigla e o TSID no caminho. A forma recomendada é:

```text
99-Gestao/02-TSIDs/
└── AGENERSA/
    ├── TSID01/
    ├── TSID02/
    └── TSID03/
```

O script também reconhece arquivos planos quando o nome contém simultaneamente a sigla e `TSID01`, `TSID02` ou `TSID03`.

Quando os documentos forem recebidos nos três arquivos ZIP originais, organize-os antes do deploy:

```bash
scripts/.venv/bin/python 05-Deploy/organizar_comunicacoes.py
```

O importador extrai os ofícios, materializa os três conjuntos de TSID por destinatário, replica os anexos comuns e aplica o TSID01 estadual ou municipal. O conjunto TSID03 inclui o expediente, o questionário personalizado de comentários e o relatório individual preliminar enviados. Os ZIPs recebidos e os manifestos ficam preservados em `99-Gestao/03-Fontes_Originais_Comunicacoes`.

O importador recusa sobrescrever um arquivo divergente. Destinatários que não integram os 113 anexos individuais permanecem no manifesto e nos ZIPs originais.

## Execução

O destino deve estar vazio ou não existir:

```bash
scripts/.venv/bin/python 05-Deploy/gerar_deploy.py \
  --output-dir 05-Deploy/gerados
```

Para validar sem materializar produtos no repositório, use um destino temporário:

```bash
scripts/.venv/bin/python 05-Deploy/gerar_deploy.py \
  --output-dir /tmp/tcerj-igovti-2026/deploy
```

Antes do protocolo, confira `FALTANTES.md`, a sequência de AN01 a AN124, todas as eventuais partes e os hashes do `manifesto-deploy.csv`.
