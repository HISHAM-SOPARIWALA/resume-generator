class DataManager {
    constructor() {
        this.isLoading = false;
        this.cache = {};
    }
    
    // Load data with optional caching
    loadData(endpoint, useCache = true) {
        return new Promise((resolve, reject) => {
            // Check if data is in cache
            if (useCache && this.cache[endpoint]) {
                console.log('Using cached data for:', endpoint);
                resolve(this.cache[endpoint]);
                return;
            }
            
            this.isLoading = true;
            
            // Make AJAX request
            $.ajax({
                url: endpoint,
                type: 'GET',
                dataType: 'json',
                success: (data) => {
                    this.isLoading = false;
                    
                    // Cache the response
                    if (useCache) {
                        this.cache[endpoint] = data;
                    }
                    
                    resolve(data);
                },
                error: (xhr, status, error) => {
                    this.isLoading = false;
                    console.error('Error fetching data:', error);
                    reject(error);
                }
            });
        });
    }
    
    // Clear cache for a specific endpoint or all endpoints
    clearCache(endpoint = null) {
        if (endpoint) {
            delete this.cache[endpoint];
        } else {
            this.cache = {};
        }
    }
    
    // Post data to the server
    postData(endpoint, data) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: endpoint,
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),
                dataType: 'json',
                success: (response) => {
                    // Clear cache as data may have changed
                    this.clearCache();
                    resolve(response);
                },
                error: (xhr, status, error) => {
                    console.error('Error posting data:', error);
                    reject(error);
                }
            });
        });
    }
    
    // Example method to render items in a container
    renderItems(items, containerId) {
        const container = $(`#${containerId}`);
        container.empty();
        
        if (!items || items.length === 0) {
            container.html('<p>No items available.</p>');
            return;
        }
        
        items.forEach(item => {
            const itemElement = $('<div class="item"></div>');
            itemElement.html(`
                <h3>${item.name}</h3>
                <p>${item.description}</p>
                <button class="item-action" data-id="${item.id}">View Details</button>
            `);
            container.append(itemElement);
        });
        
        // Add event listeners for buttons
        $('.item-action').click(function() {
            const itemId = $(this).data('id');
            console.log('Action clicked for item:', itemId);
            // Implement your action here
        });
    }
}