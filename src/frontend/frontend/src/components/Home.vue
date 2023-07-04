<template>
  <div>
    <p>{{ msg }}</p>
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
