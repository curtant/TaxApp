<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white border-bottom fixed-top py-2">
    <div class="container-fluid">
      <a class="navbar-brand fw-bold" href="#">TaxApp MVP</a>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link" href="#" @click.prevent="emitNavigate('riepilogo')">Dashboard di Riepilogo</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click.prevent="emitNavigate('contribuente')">Dichiarazione</a>
          </li>
        </ul>
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              {{ userInfo.firstName }} {{ userInfo.lastName }}
            </a>
            <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
              <li><a class="dropdown-item" href="#" @click.prevent="handleLogout">Logout</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  props: {
    userInfo: { type: Object, required: true },
    logoutUrl: { type: String, required: true },
  },
  methods: {
    emitNavigate(viewId) {
      this.$emit('navigate', viewId);
    },
    getCSRFToken() {
      const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1];
      return cookieValue;
    },
    async handleLogout() {
      const csrfToken = this.getCSRFToken();
      try {
        const response = await fetch(this.logoutUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          credentials: 'include',
        });
        if (response.ok) {
          window.location.href = '/login/'; // reindirizza al login
        } else {
          console.error('Logout fallito');
        }
      } catch (error) {
        console.error('Errore durante il logout:', error);
      }
    }
  }
};
</script>
