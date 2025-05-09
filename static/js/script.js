// JavaScript for the Image Processing App

document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const form = document.getElementById('upload-form');
    const filterSelect = document.getElementById('filter_type');
    const loadingElement = document.getElementById('loading');
    const resultsElement = document.getElementById('results');
    const originalImage = document.getElementById('original-image');
    const processedImage = document.getElementById('processed-image');
    const filterApplied = document.getElementById('filter-applied');
    const downloadBtn = document.getElementById('download-btn');
    const newImageBtn = document.getElementById('new-image-btn');
    
    // Show parameter controls based on selected filter
    filterSelect.addEventListener('change', function() {
        // Hide all parameter groups first
        document.querySelectorAll('.param-group').forEach(group => {
            group.style.display = 'none';
        });
        
        // Show relevant parameter group
        const filter = this.value;
        
        if (filter === 'brightness') {
            document.getElementById('brightness_params').style.display = 'block';
        } else if (filter === 'contrast') {
            document.getElementById('contrast_params').style.display = 'block';
        } else if (filter === 'gaussian_blur') {
            document.getElementById('gaussian_blur_params').style.display = 'block';
        } else if (filter === 'threshold') {
            document.getElementById('threshold_params').style.display = 'block';
        } else if (filter === 'pixelate') {
            document.getElementById('pixelate_params').style.display = 'block';
        }
    });
    
    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(form);
        const fileInput = document.getElementById('file');
        
        // Validate file input
        if (fileInput.files.length === 0) {
            alert('Please select an image file.');
            return;
        }
        
        // Show loading indicator
        form.style.display = 'none';
        loadingElement.style.display = 'flex';
        resultsElement.style.display = 'none';
        
        try {
            // Send form data to the server
            const response = await fetch('/process/', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Update the result images
            originalImage.src = data.original_image;
            processedImage.src = data.processed_image;
            
            // Update filter name
            filterApplied.textContent = data.filter_applied;
            
            // Show results
            loadingElement.style.display = 'none';
            resultsElement.style.display = 'block';
            
            // Setup download button
            downloadBtn.onclick = function() {
                const link = document.createElement('a');
                link.href = data.processed_image;
                link.download = `processed_${data.original_filename}`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            };
            
        } catch (error) {
            console.error('Error:', error);
            alert('Error processing the image. Please try again.');
            loadingElement.style.display = 'none';
            form.style.display = 'block';
        }
    });
    
    // Reset to upload new image
    newImageBtn.addEventListener('click', function() {
        form.reset();
        form.style.display = 'block';
        resultsElement.style.display = 'none';
        
        // Hide all parameter groups
        document.querySelectorAll('.param-group').forEach(group => {
            group.style.display = 'none';
        });
    });
    
    // Preview uploaded image
    document.getElementById('file').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = new Image();
                img.onload = function() {
                    // You can add preview functionality here if desired
                };
                img.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });
});