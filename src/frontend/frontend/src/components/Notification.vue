<template>
	<div class="notification" v-if="isVisible" :class="notificationClass">
		{{ message }}
	</div>
</template>

<script>
export default {
	props: {
		message: String,
		type: String, // "success" or "error"
	},
	data() {
		return {
			isVisible: false,
		}
	},
	computed: {
		notificationClass() {
			return {
				success: this.type === "success",
				error: this.type === "error",
			}
		},
	},
	watch: {
		isVisible(newValue) {
			if (newValue) {
				setTimeout(() => {
					this.isVisible = false
				}, 3000) // Hide the notification after 3 seconds
			}
		},
	},
}
</script>

<style scoped>
.notification {
	position: fixed;
	top: 10px;
	right: 10px;
	padding: 10px;
	border-radius: 5px;
	color: #fff;
	z-index: 1000;
	transition: opacity 0.3s;
}

.success {
	background-color: #4caf50; /* Green */
}

.error {
	background-color: #f44336; /* Red */
}
</style>
