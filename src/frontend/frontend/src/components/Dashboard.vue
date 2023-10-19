<template>
	<div>
		<!-- Primary Navigation Bar -->
		<nav
			id="primaryNav"
			class="navbar bg-dark border-bottom border-bottom-dark"
			data-bs-theme="dark"
		>
			<div class="container-fluid">
				<router-link class="navbar-brand" to="/home"
					><img id="cm-logo" src="../assets/cm_logo_color_200.png" alt="" />SDN
					Intrusion & Penetration System</router-link
				>
				<div class="d-flex">
					<a class="navbar-brand ms-auto" href="/manual">
						<i class="bi bi-info-circle"></i>
					</a>
					<a class="navbar-brand ms-auto" href="#">
						<i class="bi bi-gear"></i>
					</a>
					<router-link class="navbar-brand ms-auto" to="/login">
						<i class="bi bi-box-arrow-right"></i> Logout
					</router-link>
				</div>
			</div>
		</nav>

		<!-- Secondary Navigation Bar -->
		<nav class="navbar bg-secondary" data-bs-theme="dark">
			<div class="container-fluid navbar-expand">
				<ul class="nav nav-underline">
					<router-link to="/cve" class="nav-link">CVE Scan</router-link>
					<router-link to="/service" class="nav-link">Service Scan</router-link>
					<router-link to="/ip" class="nav-link">IP Scan</router-link>
					<router-link to="/port" class="nav-link">Port Scan</router-link>
					<router-link to="/dos" class="nav-link">DoS Attack</router-link>
					<router-link to="/ddos" class="nav-link">DDoS Attack</router-link>
				</ul>
				<ul class="nav nav-underline ms-auto">
					<router-link to="/dashboard" class="nav-link active"
						>Dashboard</router-link
					>
				</ul>
			</div>
		</nav>

		<div id="content" class="container">
			<label for="historyLog" class="form-label">History Log</label>
			<div id="historyOutputBox" class="card card-body">
				<!-- Loading indicator -->
				<div v-if="isLoading" class="text-center mt-3">
					<div class="spinner-border" role="status">
						<span class="visually-hidden">Loading...</span>
					</div>
					<p>Loading...</p>
				</div>

				<table id="historyLogTable" class="table table-hover">
					<thead>
						<tr>
							<th scope="col">Type</th>
							<th scope="col">Date</th>
							<th scope="col">Time</th>
							<th scope="col">Target</th>
						</tr>
					</thead>
					<tbody>
						<tr
							v-for="activity in paginatedHistoryLog"
							:key="activity._id"
							@click="redirectToDetailPage(activity._id)"
						>
							<td>{{ activity.activity }}</td>
							<td>{{ activity.date }}</td>
							<td>{{ activity.time }}</td>
							<td v-if="activity.activity != 'IP SCAN MULTIPLE'">
								{{ activity.target }}
							</td>
							<td v-if="activity.activity === 'IP SCAN MULTIPLE'">
								<ul>
									<li v-for="(ip, index) in activity.target" :key="index">
										{{ ip }}
									</li>
								</ul>
							</td>
						</tr>
					</tbody>
				</table>
			</div>
			<p class="right-align">{{ paginationInfo }}</p>

			<!-- Pagination controls -->
			<nav aria-label="Page navigation example">
				<ul class="pagination justify-content-end">
					<li class="page-item" :class="{ disabled: currentPage === 1 }">
						<a
							class="page-link"
							href="#"
							@click="prevPage"
							aria-label="Previous"
						>
							<span aria-hidden="true">&laquo;</span>
						</a>
					</li>

					<li
						class="page-item"
						v-for="page in displayedPages"
						:key="page"
						:class="{ active: currentPage === page }"
					>
						<a class="page-link" href="#" @click="setCurrentPage(page)">{{
							page
						}}</a>
					</li>

					<li
						class="page-item"
						:class="{ disabled: currentPage === totalPages }"
					>
						<a class="page-link" href="#" @click="nextPage" aria-label="Next">
							<span aria-hidden="true">&raquo;</span>
						</a>
					</li>
				</ul>
			</nav>
		</div>
	</div>
</template>

<script>
import axios from "axios"
export default {
	name: "Dashboard",
	data() {
		return {
			isLoading: false,
			historyLog: [],
			itemsPerPage: 10, // Number of items per page
			currentPage: 1,
			pagesToShow: 10,
		}
	},
	computed: {
		// Use a computed property to dynamically calculate the displayed pages
		displayedPages() {
			const startPage = Math.max(
				1,
				this.currentPage - Math.floor(this.pagesToShow / 2)
			)
			const endPage = Math.min(
				this.totalPages,
				startPage + this.pagesToShow - 1
			)

			return Array.from(
				{ length: endPage - startPage + 1 },
				(_, i) => startPage + i
			)
		},
		// Calculate the total number of pages
		totalPages() {
			return Math.ceil(this.historyLog.length / this.itemsPerPage)
		},
		// Calculate the array of page numbers for display
		pages() {
			const pages = []
			for (let i = 1; i <= this.totalPages; i++) {
				pages.push(i)
			}
			return pages
		},
		// Calculate the current page's data
		paginatedHistoryLog() {
			const startIndex = (this.currentPage - 1) * this.itemsPerPage
			const endIndex = startIndex + this.itemsPerPage
			return this.historyLog.slice(startIndex, endIndex)
		},
		// Calculate the "showing X-Y of Z result(s)" message
		paginationInfo() {
			const startIndex = (this.currentPage - 1) * this.itemsPerPage + 1
			const endIndex = Math.min(
				startIndex + this.itemsPerPage - 1,
				this.historyLog.length
			)
			const totalResults = this.historyLog.length

			return `Showing ${startIndex}-${endIndex} of ${totalResults} result(s)`
		},
	},
	methods: {
		getHistory() {
			const path = "http://127.0.0.1:5000/dashboard/history"
			this.isLoading = true
			axios
				.get(path)
				.then((res) => {
					console.log(res)
					this.historyLog = res.data
				})
				.catch((err) => {
					console.log(err)
				})
				.finally(() => {
					this.isLoading = false
				})
		},
		redirectToDetailPage(id) {
			// Use the `router-link` component to navigate to the detail page
			this.$router.push({ name: "historyDetail", params: { id } })
		},
		// Change to the previous page
		prevPage() {
			if (this.currentPage > 1) {
				this.currentPage--
			}
		},
		// Change to the next page
		nextPage() {
			if (this.currentPage < this.totalPages) {
				this.currentPage++
			}
		},
		// Set the current page
		setCurrentPage(page) {
			this.currentPage = page
		},
	},
	mounted() {
		this.getHistory()
	},
}
</script>

<style scoped>
.navbar {
	height: 50px;
}
h1 {
	display: block;
}
.card-body {
	white-space: pre-wrap;
}
#historyOutputBox {
	margin-bottom: 5px;
}
#content {
	padding-top: 50px;
}
ul {
	list-style-type: none; /* Remove bullets */
	padding: 0; /* Remove padding */
}
.right-align {
	text-align: right;
}
#cm-logo {
	max-width: 100%;
	max-height: 100%;
	width: auto;
	height: auto;
	object-fit: cover;
	padding-right: 10px;
}
</style>
