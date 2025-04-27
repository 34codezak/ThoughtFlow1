document.addEventListener('DOMContentLoaded', () => {
    // Check if sorting links exist
    const sortLinks = document.querySelectorAll('.sort-link');
    if (sortLinks.length === 0) return; // Exit if no links found

    // Highlight previously selected link
    const activeSort = localStorage.getItem('activeSort');
    if (activeSort) {
        const activeLink = document.querySelector(a[href="${activeSort}"]);
        if (activeLink) {
            activeLink.style.color = '#f3d19e';
        }
    }

    // Add click listener to each link
    sortLinks.forEach(link => {
        link.addEventListener('click', function () {
            // Save clicked link in localStorage
            localStorage.setItem('activeSort', this.getAttribute('href'));

            // Reset styles for all links
            sortLinks.forEach(l => {
                l.style.color = '';
                l.style.textDecoration = '';
            });

            // Apply styles to the clicked link
            this.style.color = '#f3d19e';
            this.style.textDecoration = 'underline';

            // Remove underline after 3 seconds
            setTimeout(() => {
                this.style.textDecoration = '';
            }, 3000);
        });
    });
});