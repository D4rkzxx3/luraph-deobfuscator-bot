# Luraph v15 Deobfuscator Discord Bot

Bot Discord completo per deobfuscare e analizzare script Luraph v15.

## Features

✅ **Deobfuscazione Script Luraph v15**
- Devirtualizzazione bytecode VM
- Lifted back to Luau con control flow
- Supporto opzioni: `--no-hooks`, `--max-runs`, `--devirt-rounds`

✅ **Analisi Completa**
- Proto analysis
- Costanti e upvalues
- Closure makers detection
- VM map statico

✅ **Output Dettagliati**
- `.deobf.luau` (trace)
- `.devirt.luau` (devirtualizzato)
- `.protos.json` (metadati)
- `.strings.txt` (stringhe)

✅ **Comandi Discord**
- `/deobf <script>` - Deobfusca uno script
- `/analyze <script>` - Analizza senza devirt
- `/help` - Mostra i comandi disponibili
- `/status` - Status del bot

## Setup

### 1. Clone
```bash
git clone https://github.com/D4rkzxx3/luraph-deobfuscator-bot
cd luraph-deobfuscator-bot
```

### 2. Dipendenze
```bash
pip install -r requirements.txt
```

### 3. Token Discord
```bash
cp .env.example .env
# Modifica .env con il tuo token
```

### 4. Run
```bash
python bot.py
```

## Struttura

```
.
├── bot.py                 # Main bot entry
├── cogs/
│   ├── deobfuscator.py   # Comandi deobfuscazione
│   ├── analyzer.py       # Analisi VM
│   └── utils.py          # Utility functions
├── luraph/
│   ├── __init__.py
│   ├── driver.py         # Pipeline
│   ├── devirt.py         # Devirtualizer
│   ├── vmmap.py          # VM static map
│   ├── optrace.py        # VM research
│   └── probes/           # Research helpers
├── config/
│   ├── options.txt       # Obfuscation options
│   └── settings.json     # Bot settings
└── output/               # Risultati deobfuscazione
```

## Comandi

### `/deobf`
```
/deobf script: <file o testo>
options: --no-hooks --max-runs 100 --devirt-rounds 5
```
Deobfusca uno script Luraph v15 con opzioni personalizzate.

### `/analyze`
```
/analyze script: <file o testo>
```
Analizza lo script senza devirtualizzazione completa.

### `/status`
Mostra lo stato del bot e statistiche.

### `/help`
Mostra tutti i comandi disponibili.

## Luraph v15 Specifiche

- **Detect**: Header `Luraph Obfuscator v15`
- **VM Shape**: `return setmetatable({[n]=bit32.x,...`
- **Devirt**: Lift VM bytecode a Luau reale
- **Fallback**: Behaviour trace se devirt fallisce

## Output Files

| File | Descrizione |
|------|-------------|
| `*.deobf.luau` | Script dopo trace (comportamento) |
| `*.devirt.luau` | Script devirtualizzato (controllo flusso completo) |
| `*.protos.json` | Metadati proto e costanti |
| `*.strings.txt` | Stringhe estratte |
| `*.chunk_<key>.luau` | Chunk loadstring'd |

## Samples

Vedi `/samples/` per script di test con sorgenti a confronto.

## Note Importanti

⚠️ **Environment Fidelity**: Luraph maglia molto di più che Path2D negli stage keys. Qualsiasi divergenza da Roblox reale dà chiave sbagliata.

⚠️ **Boolean Locals**: Luraph droppano lo store di boolean locali quando comparati e poi solo branchati. Un lifting fedele mostra lo stesso.

⚠️ **Stack VM**: Supporto per stack-based VM con register-resident arrays.

## Sviluppo

```bash
# Debug mode
DEVIRT_DEBUG=1 python bot.py

# Con traceback completo
DEVIRT_FULL_ROUNDS=1 DEVIRT_TB=1 python bot.py

# Senza live requests
DEOB_NO_FETCH=1 python bot.py
```

## Supporto

Per problemi:
- Controlla i log in `output/`
- Usa `--debug` per file intermedi
- Vedi CLAUDE.md per dettagli implementazione

## License

MIT
