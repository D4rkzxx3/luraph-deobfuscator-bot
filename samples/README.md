# Luraph v15 Samples

Script di test con sorgenti per validazione deobfuscazione.

## 001_vm_like_dispatch

**Sorgente**: `001_vm_like_dispatch.lua`  
**Obfuscato**: `001_vm_like_dispatch-obfuscated.lua` (options sconosciute)

### Caratteristiche
- Pure math operations (add, subtract, multiply)
- Assertions per validazione
- Stack machine VM
- 5 funzioni lifted completamente
- Stessa struttura del sorgente

### Output Atteso
```
Trace: Only Luraph probes, pure math + assert
Devirt: Stack machine lifted to Luau
Result: Returns 34
```

### Note
- Nomi variabili differenti (tbl/tbl2/n per program/stack/sp)
- Dispatch via VM-object methods (K:A(...))
- Hardcode Globals per script globals (R[a] = assert)
