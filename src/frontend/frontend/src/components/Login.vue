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
	name: "Login",
	data() {
		return {
			userField: {
				username: "",
				password: "",
			},
			isAuthenticated: false,
		}
	},
	methods: {
		async getResponse() {
			try {
				const path = "http://localhost:5000/login"
				axios.post(path, payload).then((res) => {
					console.log(res.data)
					this.msg = res.data
				})

				// Check Response from Backend
				if (res.status == 200) {
					// Redirect to Home upon successful login
					this.$router.push("/home")
				} else {
					// Display error message otherwise
					this.err = "Invalid username or password"
				}
			} catch (err) {
				console.log(err)
				// Catch any unrelated errors
				this.error = "An error was encountered during login"
			}
		},
	},
	created() {},
}
</script>

<style scoped>
.login-page {
	display: flex;
	justify-content: center;
	align-items: center;
	height: 100vh;
}

.background {
	position: absolute;
	width: 100%;
	height: 100%;
	background-color: rgba(255, 255, 255, 0.8); /* White background */
	backdrop-filter: blur(10px); /* Apply Blur effect */
	z-index: -1; /* Place the effect behind container */
}

.login-container {
	background: rgba(255, 255, 255, 0.8); /* White background with transparency */
	border-radius: 8px;
	padding: 20px;
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
	text-align: center;
}
</style>
