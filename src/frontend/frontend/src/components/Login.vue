<template>
	<div class="login-page">
		<!-- Blurred background -->
		<div class="background"></div>

		<!-- Pop out container -->
		<div class="login-container">
			<h2>Login</h2>
			<form @submit.prevent="login">
				<div class="form-group">
					<label for="username">Username</label>
					<input type="text" id="username" v-model="username" required />
				</div>
				<div class="form-group">
					<label for="password">Password</label>
					<input type="password" id="password" v-model="password" required />
				</div>
			</form>
		</div>
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
	height: 50px;
}
p {
	display: block;
	padding-top: 10px;
	margin-left: 15px;
}
</style>
