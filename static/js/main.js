document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const progressBar = document.getElementById('progressBar');
    const progressBarInner = progressBar.querySelector('.progress-bar');
    const previewArea = document.getElementById('previewArea');
    const markdownContent = document.getElementById('markdownContent');
    const downloadBtn = document.getElementById('downloadBtn');
    const alertArea = document.getElementById('alertArea');

    // Handle drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => {
            dropZone.classList.remove('dragover');
        });
    });

    // Handle file drop
    dropZone.addEventListener('drop', (e) => {
        const file = e.dataTransfer.files[0];
        handleFile(file);
    });

    // Handle file selection via click
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        handleFile(file);
    });

    function showAlert(message, type = 'danger') {
        alertArea.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
    }

    function handleFile(file) {
        // Show progress bar
        progressBar.classList.remove('d-none');
        progressBarInner.style.width = '0%';
        
        const formData = new FormData();
        formData.append('file', file);

        // Simulate upload progress
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += 10;
            if (progress <= 90) {
                progressBarInner.style.width = `${progress}%`;
            }
        }, 200);

        fetch('/convert', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            clearInterval(progressInterval);
            progressBarInner.style.width = '100%';
            
            if (data.error) {
                throw new Error(data.error);
            }

            // Show preview
            markdownContent.textContent = data.markdown;
            previewArea.classList.remove('d-none');

            // Setup download button
            downloadBtn.onclick = () => {
                const blob = new Blob([data.markdown], { type: 'text/markdown' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'converted.md';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
            };

            showAlert('File converted successfully!', 'success');
        })
        .catch(error => {
            showAlert(error.message);
        })
        .finally(() => {
            setTimeout(() => {
                progressBar.classList.add('d-none');
            }, 1000);
        });
    }
});
