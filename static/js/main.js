document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const progressBar = document.getElementById('progressBar');
    const progressBarInner = progressBar.querySelector('.progress-bar');
    const previewArea = document.getElementById('previewArea');
    const markdownContent = document.getElementById('markdownContent');
    const downloadBtn = document.getElementById('downloadBtn');
    const copyBtn = document.getElementById('copyBtn');
    const alertArea = document.getElementById('alertArea');
    const themeToggle = document.getElementById('themeToggle');
    const featureSection = document.getElementById('featureSection');

    // Initialize theme
    initializeTheme();

    // Theme toggle functionality
    themeToggle.addEventListener('click', toggleTheme);

    // Drag and drop events
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

    // File drop
    dropZone.addEventListener('drop', (e) => {
        const file = e.dataTransfer.files[0];
        if (file) {
            handleFile(file);
        }
    });

    // File selection via click
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    // Keyboard accessibility
    dropZone.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            fileInput.click();
        }
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    });

    // Theme functions
    function initializeTheme() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        setTheme(savedTheme);
    }

    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
        localStorage.setItem('theme', newTheme);
    }

    function setTheme(theme) {
        document.documentElement.setAttribute('data-bs-theme', theme);
        const icon = themeToggle.querySelector('i');
        if (theme === 'dark') {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
            themeToggle.setAttribute('aria-label', 'Switch to light mode');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
            themeToggle.setAttribute('aria-label', 'Switch to dark mode');
        }
    }

    // Alert functions
    function showAlert(message, type = 'danger') {
        const alertId = 'alert-' + Date.now();
        const alert = document.createElement('div');
        alert.id = alertId;
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.setAttribute('role', 'alert');

        const content = document.createElement('div');
        content.className = 'd-flex align-items-center';

        const icon = document.createElement('i');
        icon.className = type === 'success'
            ? 'fas fa-check-circle me-2'
            : 'fas fa-exclamation-circle me-2';

        const text = document.createElement('span');
        text.textContent = message;

        const closeButton = document.createElement('button');
        closeButton.type = 'button';
        closeButton.className = 'btn-close';
        closeButton.setAttribute('data-bs-dismiss', 'alert');
        closeButton.setAttribute('aria-label', 'Close');

        content.append(icon, text);
        alert.append(content, closeButton);
        alertArea.replaceChildren(alert);

        // Auto-dismiss after 5 seconds for success alerts
        if (type === 'success') {
            setTimeout(() => {
                const existingAlert = document.getElementById(alertId);
                if (existingAlert) {
                    existingAlert.remove();
                }
            }, 5000);
        }
    }

    // File handling
    function handleFile(file) {
        // Validate file
        if (!file) {
            showAlert('No file selected', 'danger');
            return;
        }

        // Show progress bar
        progressBar.classList.remove('d-none');
        progressBarInner.style.width = '0%';

        const formData = new FormData();
        formData.append('file', file);

        // Hide feature section and clear previous results
        featureSection.classList.add('d-none');
        previewArea.classList.add('d-none');
        alertArea.innerHTML = '';

        // Simulate upload progress
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += Math.random() * 30;
            if (progress > 100) progress = 100;
            progressBarInner.style.width = `${Math.min(progress, 90)}%`;
        }, 200);

        // Fetch conversion
        fetch('/convert', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || `Server error: ${response.status}`);
                });
            }
            return response.json();
        })
        .then(data => {
            clearInterval(progressInterval);
            progressBarInner.style.width = '100%';

            if (data.error) {
                throw new Error(data.error);
            }

            if (!data.success || !data.markdown) {
                throw new Error('Conversion failed: Empty response');
            }

            // Show preview
            markdownContent.textContent = data.markdown;
            previewArea.classList.remove('d-none');

            // Setup download button
            downloadBtn.onclick = () => downloadMarkdown(data.markdown, file.name);

            // Setup copy button
            copyBtn.onclick = () => copyToClipboard(data.markdown);

            showAlert('File converted successfully!', 'success');
        })
        .catch(error => {
            clearInterval(progressInterval);
            showAlert(error.message || 'An error occurred during conversion', 'danger');
            featureSection.classList.remove('d-none');
            previewArea.classList.add('d-none');
        })
        .finally(() => {
            setTimeout(() => {
                progressBar.classList.add('d-none');
                progressBarInner.style.width = '0%';
            }, 1000);
            // Reset file input
            fileInput.value = '';
        });
    }

    // Download markdown
    function downloadMarkdown(content, originalFileName) {
        const baseName = originalFileName.replace(/\.[^/.]+$/, '') || 'converted';
        const blob = new Blob([content], { type: 'text/markdown; charset=utf-8' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${baseName}.md`;
        document.body.appendChild(link);
        link.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(link);
        showAlert('File downloaded successfully!', 'success');
    }

    // Copy to clipboard
    function copyToClipboard(content) {
        if (!navigator.clipboard) {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = content;
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand('copy');
                showAlert('Copied to clipboard!', 'success');
            } catch (err) {
                showAlert('Failed to copy to clipboard', 'danger');
            }
            document.body.removeChild(textArea);
            return;
        }

        navigator.clipboard.writeText(content)
            .then(() => {
                showAlert('Copied to clipboard!', 'success');
            })
            .catch(() => {
                showAlert('Failed to copy to clipboard', 'danger');
            });
    }
});
