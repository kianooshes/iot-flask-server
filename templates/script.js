// Initialize the map centered on Iran
const map = L.map('map').setView([35.6892, 51.3890], 6);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Store markers and their references
let markers = [];
let currentMarker = null;

// Function to toggle sidebar
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const toggleButton = document.querySelector('.toggle-sidebar');
    const openButton = document.querySelector('.open-sidebar-btn');
    const icon = toggleButton.querySelector('i');
    
    sidebar.classList.toggle('hidden');
    openButton.classList.toggle('hidden');
    
    // Change the icon direction
    if (sidebar.classList.contains('hidden')) {
        icon.classList.remove('fa-chevron-down');
        icon.classList.add('fa-chevron-up');
    } else {
        icon.classList.remove('fa-chevron-up');
        icon.classList.add('fa-chevron-down');
    }
    
    // Adjust map size when sidebar is toggled
    setTimeout(() => {
        map.invalidateSize();
    }, 300);
}

// Function to add marker
function addMarker() {
    const lat = parseFloat(document.getElementById('latitude').value);
    const lon = parseFloat(document.getElementById('longitude').value);

    // Validate coordinates
    if (isNaN(lat) || isNaN(lon)) {
        alert('Please enter valid coordinates');
        return;
    }

    if (lat < -90 || lat > 90 || lon < -180 || lon > 180) {
        alert('Invalid coordinates. Latitude must be between -90 and 90, and longitude between -180 and 180');
        return;
    }

    // Create new marker
    const marker = L.marker([lat, lon]).addTo(map);
    
    // Add popup with coordinates
    marker.bindPopup(`Latitude: ${lat}<br>Longitude: ${lon}`).openPopup();
    
    // Add marker to the list
    addMarkerToList(marker, lat, lon);
    
    // Center map on the new marker with animation
    map.flyTo([lat, lon], 13, {
        duration: 1.5,
        easeLinearity: 0.25
    });
}

// Function to add marker to the list
function addMarkerToList(marker, lat, lon) {
    const markerList = document.getElementById('markerList');
    const markerItem = document.createElement('div');
    markerItem.className = 'marker-item';
    markerItem.innerHTML = `
        <div>Marker ${markers.length + 1}</div>
        <div>Lat: ${lat.toFixed(6)}, Lon: ${lon.toFixed(6)}</div>
        <button class="delete-btn" onclick="deleteMarker(${markers.length})">Delete</button>
    `;

    // Add click event to select marker
    markerItem.addEventListener('click', () => {
        selectMarker(markers.length);
    });

    markerList.appendChild(markerItem);
    markers.push({ marker, element: markerItem });
}

// Function to select a marker
function selectMarker(index) {
    if (currentMarker !== null) {
        markers[currentMarker].element.classList.remove('active');
    }

    const markerData = markers[index];
    markerData.element.classList.add('active');
    markerData.marker.openPopup();
    
    // Smoothly fly to the marker location
    map.flyTo(markerData.marker.getLatLng(), 13, {
        duration: 1.5,
        easeLinearity: 0.25
    });
    
    currentMarker = index;
}

// Function to delete a marker
function deleteMarker(index) {
    const markerData = markers[index];
    map.removeLayer(markerData.marker);
    markerData.element.remove();
    markers.splice(index, 1);
    
    // Update the list items after deletion
    markers.forEach((marker, i) => {
        marker.element.querySelector('div:first-child').textContent = `Marker ${i + 1}`;
    });

    if (currentMarker === index) {
        currentMarker = null;
    } else if (currentMarker > index) {
        currentMarker--;
    }
} 