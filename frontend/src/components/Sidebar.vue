<template>
  <nav class="sidebar">
    <h2 class="mb-4">Dichiarazione 730</h2>
    <ul class="nav flex-column">
      <li v-for="(item, index) in navigation" :key="index" class="nav-item">
        <!-- ... (il template della sidebar rimane identico a prima) ... -->
         <a v-if="!item.children"
           :href="item.enabled ? '#' : null"
           class="nav-link d-flex align-items-center"
           :class="{ 'disabled': !item.enabled, 'active': item.id === activeItemId }"
           @click.prevent="navigate(item)">
            {{ item.name }}
            <svg v-if="!item.enabled" class="lock-icon bi bi-lock-fill" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"  viewBox="0 0 16 16">
              <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2m3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2"/>
            </svg>
        </a>
        <div v-else>
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="collapse" :data-bs-target="'#collapse' + index">
                {{ item.name }}
            </a>
            <div class="collapse show" :id="'collapse' + index">
                <ul class="nav flex-column ms-3">
                    <li v-for="(child, childIndex) in item.children" :key="childIndex" class="nav-item">
                       <a v-if="!child.children"
                           :href="child.enabled ? '#' : null"
                           class="nav-link d-flex align-items-center"
                           :class="{ 'disabled': !child.enabled, 'active': child.id === activeItemId }"
                           @click.prevent="navigate(child)">
                            {{ child.name }}
                            <svg v-if="!child.enabled" class="lock-icon bi bi-lock-fill" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"  viewBox="0 0 16 16">
                               <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2m3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2"/>
                            </svg>
                        </a>
                        <div v-else>
                             <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="collapse" :data-bs-target="'#collapse' + index + '-' + childIndex">
                                {{ child.name }}
                            </a>
                            <div class="collapse" :id="'collapse' + index + '-' + childIndex">
                                <ul class="nav flex-column ms-3">
                                    <li v-for="(grandchild, grandchildIndex) in child.children" :key="grandchildIndex" class="nav-item">
                                        <a :href="grandchild.enabled ? '#' : null"
                                           class="nav-link d-flex align-items-center"
                                           :class="{ 'disabled': !grandchild.enabled, 'active': grandchild.id === activeItemId }"
                                           @click.prevent="navigate(grandchild)">
                                            {{ grandchild.name }}
                                            <svg v-if="!grandchild.enabled" class="lock-icon bi bi-lock-fill" xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"  viewBox="0 0 16 16">
                                              <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2m3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2"/>
                                            </svg>
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'Sidebar',
  props: ['navigation'],
  data() {
    return {
      activeItemId: 'contribuente'
    };
  },
  methods: {
    navigate(item) {
      if (item.enabled) {
        this.activeItemId = item.id;
        this.$emit('navigate', item.id);
      }
    }
  }
};
</script>

<style scoped>
/* Stili specifici per la sidebar, aggiornati per il nuovo layout */
.sidebar {
  width: 280px;
  background-color: #ffffff;
  border-right: 1px solid #dee2e6;
  padding: 1rem;
  height: calc(100vh - 66px); /* Altezza meno la navbar */
  position: fixed;
  top: 66px; /* Posizionata sotto la navbar */
  left: 0;
  overflow-y: auto;
}
.lock-icon {
  margin-left: auto;
  color: #6c757d;
}
.nav-link {
    color: #495057;
}
.nav-link.disabled {
  pointer-events: none;
  color: #adb5bd;
}
.nav-link.active {
  font-weight: bold;
  color: #0d6efd;
}
.nav-link.dropdown-toggle {
    font-weight: 500;
}
</style>
