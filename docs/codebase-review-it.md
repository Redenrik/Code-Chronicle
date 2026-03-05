# Revisione del codebase (in italiano)

## Panoramica architetturale

Code Chronicle è composto da due moduli principali:

- `src/file_explorer_summary.py`: motore CLI che legge una cartella, applica i pattern di esclusione (`.gitignore` + regole interne), genera:
  - un indice ad albero (`00_file-index.txt`)
  - una concatenazione dei file supportati (`scripts-list.txt`)
- `src/gui.py`: interfaccia PyQt5 che espone lo stesso flusso con selezione cartella, checkbox per i due output e cronologia in `chronicle-history/`.

La GUI delega la logica di scansione/generazione al modulo CLI (buona separazione tra logica e presentazione).

## Criticità rilevate

1. **Possibile crash su permessi/FS non leggibile**
   - In `_build_tree_lines`, la chiamata diretta a `os.listdir(path)` non è protetta: su directory senza permessi può sollevare eccezioni e interrompere la generazione dell'indice.

2. **Rischio cicli su symlink nelle directory**
   - La ricorsione in `_build_tree_lines` non gestisce link simbolici a directory che puntano a un antenato, con potenziale loop/infinita espansione.

3. **Scarsa testabilità della GUI e dipendenza dall'ambiente desktop**
   - `open_path` usa `os.startfile/open/xdg-open`; il comportamento dipende dall'ambiente e oggi il progetto non include test automatici per i casi di errore/fallback della GUI.

4. **Copertura test assente**
   - Non c'è una suite `tests/` dedicata alla logica più delicata (match pattern `.gitignore`, esclusione directory-only, ordinamento deterministico output).

## Attività proposte

> Stato: le attività proposte in questa revisione sono state implementate nel codice (robustezza albero file, prevenzione loop symlink, allineamento terminologia/documentazione `.gitignore`, test automatici).

### 1) Attività per correggere un refuso
- **Titolo**: Uniformare la terminologia “script summary” vs “scripts summary”/“scripts-list”.
- **Contesto**: nel progetto convivono stringhe UI e nomi file con varianti lessicali simili.
- **Task**:
  1. Cercare testi utente in GUI e README.
  2. Scegliere un lessico unico (es. “Scripts summary”).
  3. Aggiornare etichette e documentazione senza cambiare i nomi file generati (retrocompatibilità).
- **DoD**: tutte le stringhe rivolte all'utente sono coerenti e verificate con uno script di ricerca testuale.

### 2) Attività per correggere un bug
- **Titolo**: Rendere robusta la generazione indice su directory non accessibili.
- **Task**:
  1. Aggiungere gestione di `PermissionError`/`OSError` in `_build_tree_lines`.
  2. Saltare le cartelle non leggibili annotandole nell'output (es. `⚠ permission denied`).
  3. Aggiungere test unitario con mock di `os.listdir` che solleva `PermissionError`.
- **DoD**: il comando CLI non crasha e completa il file indice anche in presenza di directory non leggibili.

### 3) Attività per correggere un commento o una discrepanza di documentazione
- **Titolo**: Documentare esplicitamente i limiti `.gitignore` (anchor e negazioni) con esempi.
- **Contesto**: README cita solo che le negazioni (`!`) non sono supportate; mancano esempi su pattern ancorati/non ancorati.
- **Task**:
  1. Aggiornare README con una sezione “Compatibilità `.gitignore`”.
  2. Inserire tabella “supportato / non supportato” con esempi.
  3. Allineare i commenti nel codice a quanto scritto in README.
- **DoD**: un utente capisce prima di eseguire lo strumento quali pattern funzionano davvero.

### 4) Attività per migliorare un test
- **Titolo**: Introdurre una suite pytest minima sul motore di esclusione file.
- **Task**:
  1. Creare `tests/test_ignore_patterns.py`.
  2. Coprire casi: pattern directory-only (`build/`), wildcard (`*.log`), pattern basename (`node_modules`), path annidati.
  3. Aggiungere test di regressione per ordinamento deterministico in `get_file_paths`.
- **DoD**: almeno 8 test verdi, inclusi edge case e regressioni note.
