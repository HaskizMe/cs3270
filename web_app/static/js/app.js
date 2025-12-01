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
            const vizLocationSelect = document.getElementById("viz-location");

            data.locations.forEach((location) => {
                // Add to search dropdown
                const option = document.createElement("option");
                option.value = location;
                option.textContent = location;
                locationSelect.appendChild(option);

                // Add to visualization dropdown
                const vizOption = document.createElement("option");
                vizOption.value = location;
                vizOption.textContent = location;
                vizLocationSelect.appendChild(vizOption);
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

// Handle concurrent search (Module 7: Concurrency)
function handleConcurrentSearch(event) {
    event.preventDefault();

    const formData = new FormData(document.getElementById("search-form"));
    currentFilters = {};

    // Build filters object
    for (let [key, value] of formData.entries()) {
        if (value && key !== "limit") {
            // Skip the regular limit, use limit_per_location instead
            currentFilters[key] = value;
        }
    }

    loadWeatherDataConcurrently();
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

// Load weather data using concurrent processing (Module 7)
async function loadWeatherDataConcurrently() {
    const loading = document.getElementById("loading");
    const errorMessage = document.getElementById("error-message");
    const resultsTable = document.getElementById("results-table");

    // Show loading
    loading.style.display = "block";
    errorMessage.style.display = "none";
    resultsTable.innerHTML = "";

    try {
        // Build query string with concurrent-specific parameters
        const params = new URLSearchParams({
            ...currentFilters,
            limit_per_location: 10,
            max_workers: 4,
        });

        const response = await fetch(
            `${API_BASE}/weather/concurrent?${params}`
        );
        const data = await response.json();

        loading.style.display = "none";

        if (data.success) {
            displayResults(data.data);
            displayConcurrentInfo(data.metadata);
            document.getElementById("pagination").style.display = "none"; // No pagination for concurrent
        } else {
            showError("Failed to load data: " + data.error);
        }
    } catch (error) {
        loading.style.display = "none";
        showError("Error loading data: " + error.message);
        console.error("Error:", error);
    }
}

// Display concurrent processing information
function displayConcurrentInfo(metadata) {
    const resultsInfo = document.getElementById("results-info");
    resultsInfo.innerHTML = `
        <div style="background: #e6fffa; padding: 0.75rem; border-radius: 6px; border-left: 4px solid #38b2ac;">
            <strong>Concurrent Processing</strong><br/>
            Processed ${metadata.locations_processed} locations in ${metadata.processing_time}s using ${metadata.max_workers} workers<br/>
            Total records: ${metadata.total_records}
        </div>
    `;
}

// Module 6: Load and display visualizations
async function loadVisualization(chartType) {
    const loading = document.getElementById("viz-loading");
    const container = document.getElementById("viz-container");
    const location = document.getElementById("viz-location").value;

    // Show loading
    loading.style.display = "block";
    container.innerHTML = "";

    try {
        // Build URL based on chart type
        let url = `${API_BASE}/visualize/${chartType}`;
        const params = new URLSearchParams();

        if (location && chartType !== "rainfall") {
            params.append("location", location);
        }

        if (params.toString()) {
            url += `?${params}`;
        }

        const response = await fetch(url);
        const data = await response.json();

        loading.style.display = "none";

        if (data.success) {
            // Display the chart
            container.innerHTML = `
                <div class="viz-result">
                    <img src="data:image/png;base64,${data.image}" alt="${data.chart_type} chart" class="viz-image"/>
                </div>
            `;
        } else {
            container.innerHTML = `
                <div class="error-message">
                    Failed to generate visualization: ${data.error}
                </div>
            `;
        }
    } catch (error) {
        loading.style.display = "none";
        container.innerHTML = `
            <div class="error-message">
                Error loading visualization: ${error.message}
            </div>
        `;
        console.error("Error:", error);
    }
}
