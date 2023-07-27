<template>
  <!-- Primary Navigation Bar -->
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

	<!-- Secondary Navigation Bar -->
    <nav class="navbar bg-secondary" data-bs-theme="dark">
      <div class="container-fluid navbar-expand">
        <div class="nav nav-underline">
          <router-link to="/cve" class="nav-link">CVE Scan</router-link>
          <router-link to="/service" class="nav-link active"
            >Service Scan</router-link
          >
          <router-link to="/ip" class="nav-link">IP Scan</router-link>
          <router-link to="/port" class="nav-link">Port Scan</router-link>
          <router-link to="/dos" class="nav-link">DoS Attack</router-link>
          <router-link to="/ddos" class="nav-link">DDoS Attack</router-link>
        </div>
      </div>
    </nav>

	<!-- Page Title -->
    <h1>Service Scan</h1>

	<form @submit="onSubmit">
      <!-- Target network input text field -->
      <div class="mb-3">
        <label for="targetNetworkInput" class="form-label"
          >Target Network</label
        >
        <input
          type="text"
          class="form-control"
          id="targetNetworkInput"
          placeholder="IP address"
          v-model="serviceScanForm.ipAddress"
        />
      </div>

	  <!-- Scan type dropdown menu -->
      <label for="scanTypeInput" class="form-label">Scan Type</label>
      <select
        class="form-select"
        id="scanTypeInput"
        aria-label="Default select example"
        v-model="serviceScanForm.scanType"
      >
        <option disabled value="">Select Scan Type</option>
        <option value="sV">TCP</option>
      </select>

	  <!-- Run button -->
      <div class="run-button">
        <button type="submit" class="btn btn-primary">Run</button>
        <!-- <button type="submit" class="btn btn-primary float-end">Run</button> -->
      </div>
    </form>

	<!-- Scan Result -->
    <label for="resultOutput" class="form-label">Scan Result</label>
    <div class="card">
      <div class="card-body">{{ result }}</div>
    </div>
    
  </div>
</template>

<script></script>

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
