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
          <router-link to="/service" class="nav-link">Service Scan</router-link>
          <router-link to="/ip" class="nav-link">IP Scan</router-link>
          <router-link to="/port" class="nav-link active"
            >Port Scan</router-link
          >
          <router-link to="/dos" class="nav-link">DoS Attack</router-link>
          <router-link to="/ddos" class="nav-link">DDoS Attack</router-link>
        </div>
      </div>
    </nav>

    <div class="container">
      <div id="topRow" class="row">
        <div class="col">
          <!-- Page Title -->
          <h1>Port Scan</h1>

          <form @submit="onSubmit">
            <!-- Target network input text field -->
            <div class="mb-3 w-75">
              <label for="targetNetworkInput" class="form-label"
                >Target Network</label
              >
              <input
                type="text"
                class="form-control"
                id="targetNetworkInput"
                placeholder="IP address"
                v-model="portScanForm.ipAddress"
              />
            </div>

            <!-- Scan type dropdown menu -->
            <label for="scanTypeInput" class="form-label">Scan Type</label>
            <select
              class="form-select w-75"
              id="scanTypeInput"
              aria-label="Default select example"
              v-model="portScanForm.scanType"
            >
              <option disabled value="">Select Scan Type</option>
              <option value="sV">TCP</option>
              <option value="sU">UDP</option>
            </select>

            <!-- Run button -->
            <div class="run-button">
              <button type="submit" class="btn btn-primary">Run</button>
              <!-- <button type="submit" class="btn btn-primary float-end">Run</button> -->
            </div>
          </form>
        </div>
        <div class="col">
          <!-- Event Log -->
          <div class="row">
            <div class="col-md-4">
              <label for="eventLog" class="form-label">Event Log</label>
            </div>
            <div class="col-md-8">
              <div
                v-show="display"
                class="progress"
                role="progressbar"
                style="height: 10px"
              >
                <div
                  class="progress-bar progress-bar-striped progress-bar-animated"
                  style="width: 100%"
                ></div>
              </div>
            </div>
          </div>
          <div id="eventCard" class="card">
            <div id="eventLogBox" class="card-body">{{ eventLog }}</div>
          </div>
        </div>
      </div>
      <div id="bottomRow" class="row">
        <div class="col">
          <!-- Scan Result old -->
          <label for="resultOutput" class="form-label">Scan Result</label>
          <div id="resultOutputBox" class="card">
            <div class="card-body">{{ result }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"
export default {
  name: "PortScan",
  data() {
    return {
      portScanForm: {
        ipAddress: "",
        scanType: "",
      },
      result: "",
      eventLog: "",
      display: false,
    }
  },
  methods: {
    // POST Function
    scanPorts(payload) {
      const path = "http://localhost:5000/portScan/"
      this.eventLog += `Scan started on network ${this.portScanForm.ipAddress}\n`
      this.display = true
      axios
        .post(path, payload)
        .then((res) => {
          console.log(res.data)
          this.result = res.data
          this.eventLog += "Scan completed successfully\n"
        })
        .catch((err) => {
          console.log(err)
        })
        .finally(() => {
          // this.scanning = false
        })
    },
    initForm() {
      this.portScanForm.ipAddress = ""
      this.portScanForm.scanType = ""
    },
    initStatus() {
      this.eventLog = ""
      this.result = ""
    },
    onSubmit(e) {
      e.preventDefault()
      const payload = {
        ipAddress: this.portScanForm.ipAddress,
        scanType: this.portScanForm.scanType,
      }
      console.log(payload)
      this.scanPorts(payload)
      this.initForm()
    },
  },
  created() {},
}
</script>

<style>
.navbar {
  height: 50px;
}
h1 {
  display: block;
}
form {
  padding-top: 30px;
  margin-left: 50px;
}
.btn-primary {
  min-width: 100px;
  max-width: 100px;
}
.run-button {
  padding-top: 53px;
  padding-right: 20px;
  text-align: right;
}
.card {
  min-height: 100px;
}
#topRow {
  padding-top: 50px;
}
#bottomRow {
  padding-top: 50px;
}
#eventCard {
  min-height: 300px;
  max-height: 300px;
}
.card-body {
  white-space: pre-wrap;
}
#resultOutputBox {
  margin-bottom: 50px;
}
.progress-bar {
}
.progress {
  visibility: hidden;
}
</style>
