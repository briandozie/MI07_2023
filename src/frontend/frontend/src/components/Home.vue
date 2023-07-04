<template>
  <div>
    <nav
      class="navbar bg-dark border-bottom border-bottom-dark"
      data-bs-theme="dark"
    >
      <div class="container-fluid">
        <a class="navbar-brand" href="#">SDN Intrusion & Penetration System</a>
        <a class="navbar-brand ms-auto" href="#">
          <i class="bi bi-gear"></i>
        </a>
        <a class="navbar-brand mS-auto" href="#">
          <i class="bi bi-person"></i>
        </a>
      </div>
    </nav>

    <nav class="navbar bg-secondary" data-bs-theme="dark">
      <div class="container-fluid">
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNavAltMarkup"
          aria-controls="navbarNavAltMarkup"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav">
            <a class="nav-link active" aria-current="page" href="#">Home</a>
            <a class="nav-link" href="#">Features</a>
            <a class="nav-link" href="#">Pricing</a>
            <a class="nav-link disabled">Disabled</a>
          </div>
        </div>
      </div>
    </nav>
    <!-- <button type="button" class="btn btn-primary">{{ msg }}</button> -->
  </div>
</template>

<script>
import axios from "axios"
export default {
  name: "Home",
  data() {
    return {
      msg: "",
    }
  },
  methods: {
    getResponse() {
      const path = "http://localhost:5000/home"
      axios
        .get(path)
        .then((res) => {
          console.log(res.data)
          this.msg = res.data
        })
        .catch((err) => {
          console.log(err)
        })
    },
  },
  created() {
    this.getResponse()
  },
}
</script>

<style>
.navbar {
  height: 60px;
}
</style>
