// Weather Data Explorer - Frontend JavaScript

const API_BASE = "/api";
let currentOffset = 0;
let currentFilters = {};
let totalRecords = 0;
let currentLimit = 25;

// Initialize app on page load
document.addEventListener("DOMContentLoaded", () => {
    loadLocations();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    const searchForm = document.getElementById("search-form");
    searchForm.addEventListener("submit", handleSearch);
    searchForm.addEventListener("reset", handleReset);
}

// Load locations for dropdown
async function loadLocations() {
    try {
        const response = await fetch(`${API_BASE}/locations`);
        const data = await response.json();

        if (data.success) {
            const locationSelect = document.getElementById("location");
            data.locations.forEach((location) => {
                const option = document.createElement("option");
                option.value = location;
                option.textContent = location;
                locationSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error("Error loading locations:", error);
    }
}

// Handle search form submission
function handleSearch(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    currentFilters = {};

    // Build filters object
    for (let [key, value] of formData.entries()) {
        if (value) {
            currentFilters[key] = value;
        }
    }

    currentLimit = parseInt(currentFilters.limit || 25);
    currentOffset = 0;

    loadWeatherData();
}

// Handle form reset
function handleReset() {
    currentFilters = {};
    currentOffset = 0;
    currentLimit = 25;

    // Clear results
    document.getElementById("results-table").innerHTML =
        '<p class="no-results">Use the search form above to find weather data.</p>';
    document.getElementById("pagination").style.display = "none";
    document.getElementById("results-info").textContent = "";
}

// Load weather data from API
async function loadWeatherData() {
    const loading = document.getElementById("loading");
    const errorMessage = document.getElementById("error-message");
    const resultsTable = document.getElementById("results-table");

    // Show loading
    loading.style.display = "block";
    errorMessage.style.display = "none";
    resultsTable.innerHTML = "";

    try {
        // Build query string
        const params = new URLSearchParams({
            ...currentFilters,
            offset: currentOffset,
        });

        const response = await fetch(`${API_BASE}/weather?${params}`);
        const data = await response.json();

        loading.style.display = "none";

        if (data.success) {
            totalRecords = data.total;
            displayResults(data.data);
            updatePagination(data);
            updateResultsInfo(data);
        } else {
            showError("Failed to load data: " + data.error);
        }
    } catch (error) {
        loading.style.display = "none";
        showError("Error loading data: " + error.message);
        console.error("Error:", error);
    }
}

// Display results in table
function displayResults(data) {
    const resultsTable = document.getElementById("results-table");

    if (data.length === 0) {
        resultsTable.innerHTML =
            '<p class="no-results">No results found. Try adjusting your filters.</p>';
        return;
    }

    const table = document.createElement("table");
    table.innerHTML = `
        <thead>
            <tr>
                <th>Location</th>
                <th>Min Temp (°C)</th>
                <th>Max Temp (°C)</th>
                <th>Rainfall (mm)</th>
                <th>Humidity 9am (%)</th>
                <th>Humidity 3pm (%)</th>
                <th>Rain Today</th>
            </tr>
        </thead>
        <tbody>
            ${data
                .map(
                    (record) => `
                <tr>
                    <td>${record.location || "N/A"}</td>
                    <td>${
                        record.min_temp !== null ? record.min_temp : "N/A"
                    }</td>
                    <td>${
                        record.max_temp !== null ? record.max_temp : "N/A"
                    }</td>
                    <td>${
                        record.rainfall !== null ? record.rainfall : "N/A"
                    }</td>
                    <td>${
                        record.humidity_9am !== null
                            ? record.humidity_9am
                            : "N/A"
                    }</td>
                    <td>${
                        record.humidity_3pm !== null
                            ? record.humidity_3pm
                            : "N/A"
                    }</td>
                    <td>${record.rain_today || "N/A"}</td>
                </tr>
            `
                )
                .join("")}
        </tbody>
    `;

    resultsTable.innerHTML = "";
    resultsTable.appendChild(table);
}

// Update pagination controls
function updatePagination(data) {
    const pagination = document.getElementById("pagination");
    const totalPages = Math.ceil(data.total / currentLimit);
    const currentPage = Math.floor(currentOffset / currentLimit) + 1;

    if (totalPages <= 1) {
        pagination.style.display = "none";
        return;
    }

    pagination.style.display = "flex";
    pagination.innerHTML = `
        <button ${currentPage === 1 ? "disabled" : ""} onclick="goToPage(${
        currentPage - 1
    })">
            Previous
        </button>
        <span style="padding: 0.5rem 1rem; color: #4a5568;">
            Page ${currentPage} of ${totalPages}
        </span>
        <button ${
            currentPage === totalPages ? "disabled" : ""
        } onclick="goToPage(${currentPage + 1})">
            Next
        </button>
    `;
}

// Update results info
function updateResultsInfo(data) {
    const resultsInfo = document.getElementById("results-info");
    const start = currentOffset + 1;
    const end = Math.min(currentOffset + data.count, data.total);
    resultsInfo.textContent = `Showing ${start}-${end} of ${data.total.toLocaleString()} results`;
}

// Navigate to page
function goToPage(page) {
    currentOffset = (page - 1) * currentLimit;
    loadWeatherData();
}

// Show error message
function showError(message) {
    const errorMessage = document.getElementById("error-message");
    errorMessage.textContent = message;
    errorMessage.style.display = "block";
}
