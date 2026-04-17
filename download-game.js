document.addEventListener('DOMContentLoaded', function() {
    const downloadBtn = document.getElementById('downloadBtn');
    
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function(e) {
            console.log('Game download initiated');
            
            const originalText = downloadBtn.innerHTML;
            downloadBtn.innerHTML = 'PREPARING DOWNLOAD...';
            downloadBtn.style.opacity = '0.7';
            
            setTimeout(() => {
                downloadBtn.innerHTML = originalText;
                downloadBtn.style.opacity = '1';
            }, 2000);
        });
    }
});