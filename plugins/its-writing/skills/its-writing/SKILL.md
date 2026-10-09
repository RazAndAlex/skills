---
name: its-writing
description: "Usa questa skill per QUALSIASI testo in italiano che legge una persona: documentazione, README, descrizioni di PR, messaggi di errore, note di rilascio, etichette di interfaccia, riepiloghi di sessione, commenti. Mai per il codice. Riscrive in italiano tecnico semplice, ispirato all'ITS, per eliminare lo stile artificiale tipico dei testi generati dall'AI. Usa questa skill quando devi rendere un testo meno artificiale, più chiaro o più semplice, applicare uno stile controllato o scrivere documentazione tecnica naturale. Due modalità — rigorosa (procedure/sicurezza) e stile ITS (testi generali)."
---

# its-writing

> Adattata da ste-writing di Ege Çelebi (MIT), versione del 2026-07-24 da
> https://github.com/woosal1337/blog. Licenza: `LICENSE` in questa cartella.

Scrivi in italiano tecnico semplice, ispirato ai principi dell'Italiano Tecnico Semplificato (ITS). Questa regola si applica a documentazione, README, testi di pull request, messaggi di errore, note di rilascio e commenti. Non si applica a codice, identificatori o sintassi dei comandi. Non usarla per testi di marketing, saggi o contenuti che richiedono una voce autoriale — lo stile controllato elimina intenzionalmente la voce.

## Regole

PAROLE
- Usa un solo nome per una cosa. Non chiamare lo stesso elemento con nomi diversi.
- Usa la parola breve e comune: avviare (non dare avvio), usare (non utilizzare o impiegare), aiutare (non facilitare), verificare (non accertare), prima (non preliminarmente), dopo (non successivamente), su (non relativamente a o in merito a), ottenere (non acquisire o reperire), mostrare (non illustrare o evidenziare), anche (non inoltre, peraltro o altresì).
- Assegna un solo significato a ogni parola. "Cadere" significa muoversi verso il basso, non diminuire.
- Non usare aggettivi di marketing: fluido, solido, potente, all'avanguardia, senza sforzo, di livello mondiale, di nuova generazione, rivoluzionario.
- Usa l'italiano standard contemporaneo. Evita regionalismi e anglicismi non necessari.

VERBI
- Usa la forma attiva. "Il parser legge il file", non "il file viene letto dal parser".
- Usa un verbo per un'azione. "Analizza il log", non "esegui un'analisi del log".
- Non accumulare verbi ausiliari o servili. Non scrivere "è importante notare che questo potrebbe contribuire a migliorare". Scrivi "questo migliora X".
- Non usare il gerundio per l'azione principale quando puoi usare un verbo di modo finito.

FRASI
- Scrivi una sola istruzione per frase. Usa massimo 20 parole per un'istruzione e 25 per una descrizione.
- Non omettere elementi necessari per abbreviare il testo. Usa articoli, soggetti e verbi quando rendono la frase più chiara.

PUNTEGGIATURA
- Non usare il punto e virgola. Scrivi due frasi.
- Non usare la lineetta lunga. Chiudi la frase o usa una virgola. La lineetta lunga e' un segnale di testo generato dall'AI, e le parentesi al suo posto sono lo stesso segnale con un altro simbolo.

STRUTTURA
- Tratta un solo argomento per paragrafo e usa massimo sei frasi. Per i passaggi, usa un elenco numerato verticale, un'azione per punto e il modo imperativo. Scrivi la condizione prima del comando.

Scrivi solo il testo richiesto. Non aggiungere introduzioni, riepiloghi o formule di chiusura.

## Modalità

- **rigorosa** — procedure, runbook, testi di sicurezza e messaggi di errore: applica tutte le regole e i due limiti di lunghezza.
- **stile ITS** — testi generali (README, descrizioni di PR, documentazione): applica le regole su frasi, paragrafi, forma attiva e verbi semplici. Allenta il controllo del vocabolario di base per mantenere un testo naturale.

## Controllo finale (esegui prima di restituire il testo)

1. Un'istruzione supera 20 parole o una descrizione supera 25 parole? Dividila.
2. C'e' un punto e virgola o una lineetta lunga? Sostituiscili con un punto o una virgola.
3. Hai omesso un elemento necessario solo per abbreviare la frase? Aggiungilo.
4. C'è una forma passiva con un soggetto noto? Usa la forma attiva.
5. C'è un gerundio principale, una nominalizzazione ("eseguire un'analisi") o una locuzione verbale non necessaria ("dare avvio")? Usa un verbo semplice.
6. Hai chiamato la stessa cosa in due modi? Scegli un solo nome.

Le regole meccaniche precedenti possono essere controllate e rimuovono lo stile artificiale. La piena applicazione dell'ITS richiede giudizio umano, terminologia tecnica corretta e accesso al metodo ufficiale — un controllo automatico non può certificarla. Questa skill corregge la FORMA dello stile artificiale. Non può rendere vero un paragrafo privo di contenuto.

Metodo ufficiale ITS. Non copiarlo integralmente perché è protetto da marchio e copyright: https://www.italianotecnicosemplificato.it/
