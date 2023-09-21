<template>
	<div class="login-page">
		<!-- Blurred background -->
		<div class="background"></div>

		<!-- Pop out container -->
		<div class="login-container">
			<h2>Login</h2>
			<form @submit.prevent="onSubmit">
				<div class="form-group">
					<label for="username">Username</label>
					<input
						type="text"
						id="username"
						v-model="userField.username"
						required
					/>
				</div>
				<div class="form-group">
					<label for="password">Password</label>
					<input
						type="password"
						id="password"
						v-model="userField.password"
						required
					/>
				</div>
				<button type="submit">Login</button>
			</form>
		</div>

		<!-- Success and Error Messages -->
		<Notification :message="notificationMessage" />
		<Notification :type="notificationType" />
	</div>
</template>

<script>
import axios from "axios"
import Notification from "./Notification.vue"

export default {
	name: "Login",
	components: {
		Notification,
	},
	data() {
		return {
			userField: {
				username: "",
				password: "",
			},
			notificationMessage: "",
			notificationType: "",
		}
	},
	methods: {
		getResponse(payload) {
			const path = "http://localhost:5000/login/"
			axios
				.post(path, payload)
				.then((res) => {
					console.log(res.data)
					this.msg = res.data

					// Check Response from Backend
					if (res.status == 200) {
						// Success message upon login
						this.notificationMessage = "Login Successful!"
						this.notificationType = "success"
						// Redirect to Home upon successful login
						this.$router.push("/home")
					} else {
						// Display error message otherwise
						this.errorMessage = "Invalid username or password"
						this.notificationType = "error"
					}
				})
				.catch((error) => {
					if (error.response.status === 401) {
						// Handle 401 Unauthorized error
						this.errorMessage = "Unauthorized: Invalid username or password"
						this.notificationType = "error"
					} else {
						// Catch any unrelated errors
						console.error("An error occurred:", error)
						this.errorMessage = "An error was encountered during login"
						this.notificationType = "error"
					}
				})
		},
		initForm() {
			this.userField.username = ""
			this.userField.password = ""
		},
		onSubmit(e) {
			e.preventDefault()
			const payload = {
				username: this.userField.username,
				password: this.userField.password,
			}
			console.log(payload)
			this.getResponse(payload)
			this.initForm()
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
	background-color: rgba(192, 192, 192, 0.8); /* White background */
	backdrop-filter: blur(10px); /* Apply Blur effect */
	z-index: -1; /* Place the effect behind container */
}

.login-container {
	background: rgba(255, 255, 255, 0.8); /* White background with transparency */
	border-radius: 8px;
	padding: 30px;
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
	text-align: center;
	width: 400px;
}

.form-group {
	display: flex;
	flex-direction: column;
	align-items: flex-start;
}

label {
	font-weight: bold;
	margin-bottom: 5px;
}

input {
	padding: 8px;
	border: 1px solid #ccc;
	border-radius: 4px;
	margin-bottom: 10px;
}

button {
	padding: 10px;
	background-color: #007bff;
	color: white;
	border: none;
	border-radius: 4px;
	cursor: pointer;
	margin-top: 10px;
	margin-right: 50px;
	width: 100px;
}

button:hover {
	background-color: #0056b3;
}
</style>
