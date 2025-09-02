# **TaxApp: Un Progetto Didattico per l'Integrazione di Django e Vue.js**

Benvenuto in TaxApp, un'applicazione web creata per esplorare le diverse strategie di integrazione tra un potente backend come Django e un moderno framework frontend come Vue.js. 
L'obiettivo di questo progetto non è creare un'applicazione funzionale per la dichiarazione dei redditi, ma servire come caso studio pratico sui diversi approcci architetturali possibili ed accellerare il proceso di apprendimento nel farlo.
Dunque sarà passibile di molti errori e refactoring.

### **Approccio adottato i Paradigmi di Integrazione**

Durante lo sviluppo, sono stati deliberatamente utilizzati modelli diversi di integrazione per dimostrarne i rispettivi punti di forza:

**1\. Form Pre-renderizzati da Django (Approccio Ibrido)**

* **Dove?** Nel modulo "Informazioni relative al contribuente".  
* **Come funziona?** Django, tramite i suoi ModelForm, genera l'HTML completo del form, con tutti i campi, le etichette, le classi CSS e i token di sicurezza (CSRF). Vue si occupa di richiedere questo blocco di HTML tramite un'API e di inserirlo dinamicamente nella pagina.  
* **Perché questa scelta?** È l'approccio ideale per form complessi. Permette di sfruttare tutta la potenza di Django per la validazione dei dati, la gestione degli errori e la sicurezza, senza dover duplicare questa logica complessa in JavaScript. È veloce da sviluppare e molto robusto.

**2\. API JSON Pura (Approccio SPA Tradizionale)**

* **Dove?** Nella "Dashboard di Riepilogo" con i grafici.  
* **Come funziona?** Django espone un endpoint API che restituisce i dati in formato JSON puro. Vue riceve questi dati e si occupa interamente della loro visualizzazione, costruendo i grafici e la tabella dei consigli da zero utilizzando Chart.js.  
* **Perché questa scelta?** È la soluzione adottata per componenti altamente interattivi e dinamici. Decoppia completamente il frontend dal backend, permettendo di lavorare al frontend di lavorare sulla UI, a patto di rispettare il "contratto" dei dati definito dall'API.

### **Stack Tecnologico**

* **Backend**: Python 3.13+, Django 5.2+  
* **Frontend**: Node.js 20+, Vue.js 3 (SFC & Composition API), Vite, Chart.js  
* **Styling**: Bootstrap 5  
* **Database**: SQLite 
* **Integrazione**: django-vite e django-cors-headers

### **Funzionalità Attuali**

* **Autenticazione**: Sistema completo di registrazione, login e logout gestito da Django.  
* **Dashboard Interattiva**: Un'interfaccia Single Page Application (SPA) costruita con Vue.js che funge da centro di controllo per l'utente.  
* **Compilazione Anagrafica**: Un form dettagliato e segmentato per l'inserimento e la modifica dei dati anagrafici del contribuente.  
* **Dashboard di Riepilogo**: Una vista analitica con grafici interattivi (a barre e a ciambella) che visualizzano una simulazione dei dati reddituali, delle imposte e dei rimborsi.  
* **Logica di Simulazione**: I dati visualizzati sono generati dinamicamente da una logica di backend che simula il calcolo dell'IRPEF basato sugli scaglioni ufficiali.

### **Struttura del Progetto**

La codebase è divisa in due macro-aree: backend per tutto il codice Django e frontend per il codice Vue.js.
```
.  
├── backend/                
│   ├── anagrafica/           \# App Django per i dati anagrafici  
│   │   ├── forms.py          \# Form Django per la validazione dei dati  
│   │   └── templates/        
│   │       └── anagrafica/  
│   │           └── \_contribuente\_form.html \# Template del form renderizzato da Django  
│   ├── declaration\_app/      \# App Django principale (autenticazione, viste contenitore)  
│   │   └── templates/  
│   │       ├── dashboard.html \# Template "guscio" che ospita l'app Vue  
│   │       └── registration/  
│   │           ├── login.html  
│   │           └── register.html  
│   ├── djcore/               \# Cartella per la configurazione del progetto Django (settings.py, urls.py)  
│   └── riepilogo/            \# App Django per la dashboard di riepilogo  
│       └── logic.py          \# Logica per simulare/calcolare i dati fiscali  
├── frontend/                 
│   ├── src/  
│   │   ├── App.vue           \# Componente Vue principale, gestisce il layout e la navigazione  
│   │   ├── components/       
│   │   │   ├── Navbar.vue  
│   │   │   ├── RiepilogoDashboard.vue \# Componente per la dashboard con grafici  
│   │   │   ├── Sidebar.vue  
│   │   │   └── TaxpayerInfo.vue     \# Componente che mostra il form anagrafico  
│   │   └── main.js           \# Entry point dell'applicazione Vue  
│   └── vite.config.js      
└── README.md
```