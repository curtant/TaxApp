<template>
  <div>
    <form @submit.prevent="submitForm" v-html="formHtml"></form>
    <div v-if="isLoading" class="d-flex justify-content-center mt-5">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
    <div v-if="successMessage" class="alert alert-success mt-3">{{ successMessage }}</div>
    <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  name: 'TaxpayerInfo',
  setup() {
    const formHtml = ref('');
    const isLoading = ref(true);
    const successMessage = ref('');
    const errorMessage = ref('');

    const fetchForm = async () => {
      isLoading.value = true;
      errorMessage.value = '';
      try {
        const response = await fetch('/api/anagrafica/form/');
        if (!response.ok) throw new Error('Errore nel caricamento del form');
        const data = await response.json();
        formHtml.value = data.html_form;
      } catch (error) {
        errorMessage.value = error.message;
      } finally {
        isLoading.value = false;
      }
    };

    const submitForm = async (event) => {
        const form = event.target;
        const formData = new FormData(form);
        
        successMessage.value = '';
        errorMessage.value = '';

        try {
            const response = await fetch('/api/anagrafica/form/', {
                method: 'POST',
                body: formData,
                headers: {
                    // Non serve 'Content-Type', il browser lo imposta automaticamente con FormData
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                },
            });

            if (!response.ok) throw new Error('Errore durante il salvataggio');
            
            const data = await response.json();
            formHtml.value = data.html_form; // Ricarica il form con i dati aggiornati o eventuali errori
            successMessage.value = "Dati salvati con successo!";

        } catch(error) {
            errorMessage.value = error.message;
        }
    };

    onMounted(fetchForm);

    return {
      formHtml,
      isLoading,
      successMessage,
      errorMessage,
      submitForm,
    };
  },
};
</script>
