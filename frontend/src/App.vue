<template>
  <div>
    <!-- Ascolta l'evento 'navigate' dalla Navbar e chiama il metodo setActiveView -->
    <Navbar 
      :user-info="userInfo" 
      :logout-url="logoutUrl" 
      @navigate="setActiveView" 
    />
    
    <div class="d-flex main-container">
      <!-- La Sidebar emette lo stesso evento 'navigate', rendendo il codice riutilizzabile -->
      <Sidebar :navigation="navigation" @navigate="setActiveView" />

      <main class="main-content">
        <div class="container-fluid">
          
          <!-- Mostra il componente corretto in base al valore di activeView -->
          <TaxpayerInfo v-if="activeView === 'contribuente'" />
          <RiepilogoDashboard v-if="activeView === 'riepilogo'" />

          <!-- Placeholder per altre viste non ancora implementate -->
          <div v-if="!['contribuente', 'riepilogo'].includes(activeView)">
             <div class="alert alert-info">
                <h2>Sezione in Sviluppo</h2>
                <p>La vista per '{{ activeView }}' sarà implementata prossimamente.</p>
             </div>
          </div>

        </div>
      </main>
    </div>
  </div>
</template>

<script>
// 1. Importa tutti i componenti necessari
import Sidebar from './components/Sidebar.vue';
import TaxpayerInfo from './components/TaxpayerInfo.vue';
import Navbar from './components/Navbar.vue';
import RiepilogoDashboard from './components/RiepilogoDashboard.vue';

export default {
  name: 'App',
  // 2. Registra i componenti
  components: {
    Sidebar,
    TaxpayerInfo,
    Navbar,
    RiepilogoDashboard,
  },
  data() {
    return {
      activeView: 'riepilogo', // La dashboard di riepilogo ora è la vista di default
      userInfo: { firstName: '', lastName: '' },
      logoutUrl: '#',
      navigation: [ // Struttura di navigazione per la Sidebar
        {
          name: "Informazioni Preliminari",
          children: [
            { id: 'contribuente', name: "Informazioni relative al contribuente", enabled: true },
            { id: 'familiari', name: "Familiari a carico", enabled: false },
            { id: 'sostituto', name: "Dati del sostituto d'imposta", enabled: false },
            { id: 'firma', name: "Firma della dichiarazione", enabled: false }
          ]
        },
        {
          name: "Redditi (Quadri da A a D)",
          children: [
            { id: 'quadro_a', name: "Quadro A - Redditi dei terreni", enabled: false },
            { id: 'quadro_b', name: "Quadro B - Redditi dei fabbricati e altri dati", enabled: false },
            { id: 'quadro_c', name: "Quadro C - Redditi di lavoro dipendente ed assimilati", enabled: true },
            { id: 'quadro_d', name: "Quadro D - Altri redditi", enabled: false }
          ]
        },
        {
          name: "Oneri e spese (Quadro E)",
          children: [
             { id: 'quadro_e1_e14', name: "Quadro E - I: (da E1 a E14)", enabled: true },
             { id: 'quadro_e21_e36', name: "Quadro E - II: (da E21 a E36)", enabled: false },
            {
              name: "Quadro E - III:",
              children: [
                { id: 'quadro_e41_e43', name: "A - (da E41 a E43)", enabled: false },
                { id: 'quadro_e51_e53', name: "B - (da E51 a E53)", enabled: false },
                { id: 'quadro_e56_e59', name: "C - (da E56 a E59)", enabled: false }
              ]
            },
            {
              name: "Quadro E - IV - V - VI:",
              children: [
                { id: 'quadro_e61_e62', name: " IV - (da E61 a E62)", enabled: false },
                { id: 'quadro_e71_e72', name: " V  - (da E71 a E72)", enabled: false },
                { id: 'quadro_e81_e83', name: " VI - (da E81 a E83)", enabled: false }
              ]
            }
          ]
        },
        {
          name: "Informazioni Conclusive",
          children: [
            { id: 'quadro_f', name: "Quadro F - Acconti, ritenute, eccedenze e altri dati", enabled: false },
            { id: 'quadro_g', name: "Quadro G - Crediti d'imposta", enabled: false },
            { id: 'quadro_i', name: "Quadro I - Imposte da compensare", enabled: false },
            { id: 'quadro_k', name: "Quadro K - Comunicazione dell'amministratore di condominio", enabled: false },
            { id: 'quadro_l', name: "Quadro L - Ulteriori dati", enabled: false }
          ]
        }
      ]
    };
  },
  created() {
    const vueDataElement = document.getElementById('vue-data');
    if (vueDataElement) {
      const data = JSON.parse(vueDataElement.textContent);
      this.userInfo = data.userInfo || { firstName: 'Utente', lastName: '' };
      this.logoutUrl = data.logoutUrl || '#';
    }
  },
  methods: {
    // 3. Questo singolo metodo gestisce la navigazione sia dalla Sidebar che dalla Navbar
    setActiveView(viewId) {
      this.activeView = viewId;
    }
  }
};
</script>

<style>
/* Gli stili globali rimangono invariati */
body {
  font-family: 'Inter', sans-serif;
  background-color: #f8f9fa;
}
.main-container {
  padding-top: 66px;
}
.main-content {
  margin-left: 280px;
  padding: 2rem;
  width: calc(100% - 280px);
}
</style>
