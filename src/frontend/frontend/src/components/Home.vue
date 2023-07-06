<template>
  <div>
    <nav
      class="navbar bg-dark border-bottom border-bottom-dark"
      data-bs-theme="dark"
    >
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/home"
          >SDN Intrusion & Penetration System</router-link
        >
        <a class="navbar-brand ms-auto" href="#">
          <i class="bi bi-gear"></i>
        </a>
        <a class="navbar-brand mS-auto" href="#">
          <i class="bi bi-person"></i>
        </a>
      </div>
    </nav>

    <nav class="navbar bg-secondary" data-bs-theme="dark">
      <div class="container-fluid navbar-expand">
        <div class="nav nav-underline">
          <router-link to="/cve" class="nav-link">CVE Scan</router-link>
          <router-link to="/service" class="nav-link">Service Scan</router-link>
          <router-link to="/ip" class="nav-link">IP Scan</router-link>
          <router-link to="/port" class="nav-link">Port Scan</router-link>
          <router-link to="/dos" class="nav-link">DoS Attack</router-link>
          <router-link to="/ddos" class="nav-link">DDoS Attack</router-link>
          <!-- <router-link to="/dashboard" class="nav-link">Daskboard</router-link> -->
        </div>
      </div>
    </nav>

    <p>This is the Home Page</p>
    <!-- <button type="button" class="btn btn-primary">{{ msg }}</button> -->
  </div>
</template>

<script>
// import axios from "axios"
// export default {
//   name: "Home",
//   data() {
//     return {
//       msg: "",
//     }
//   },
//   methods: {
//     getResponse() {
//       const path = "http://localhost:5000/home"
//       axios
//         .get(path)
//         .then((res) => {
//           console.log(res.data)
//           this.msg = res.data
//         })
//         .catch((err) => {
//           console.log(err)
//         })
//     },
//   },
//   created() {
//     this.getResponse()
//   },
// }
</script>

<style>
.navbar {
  height: 50px;
}
p {
  display: block;
  padding-top: 10px;
  margin-left: 15px;
}
</style>
