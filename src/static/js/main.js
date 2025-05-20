// Main JavaScript file for Pokemon Database Web App

document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Confirm delete operations
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Handle search form submission
    const searchForms = document.querySelectorAll('.search-form');
    searchForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Remove empty fields from the form before submission
            const inputs = form.querySelectorAll('input, select');
            inputs.forEach(input => {
                if (input.value === '' || input.value === null) {
                    input.disabled = true;
                }
            });
        });
    });

    // Reset search form
    const resetButtons = document.querySelectorAll('.reset-search');
    resetButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const form = this.closest('form');
            const inputs = form.querySelectorAll('input, select');
            inputs.forEach(input => {
                input.value = '';
            });
            form.submit();
        });
    });

    // Ability selection for Pokemon
    const abilitySelects = document.querySelectorAll('.ability-select');
    abilitySelects.forEach(select => {
        select.addEventListener('change', function() {
            const selectedOptions = Array.from(this.selectedOptions).map(option => option.text);
            const selectedDisplay = this.closest('.form-group').querySelector('.selected-abilities');
            if (selectedDisplay) {
                selectedDisplay.textContent = selectedOptions.join(', ');
            }
        });
    });

    // Stat bars for Pokemon
    const statBars = document.querySelectorAll('.stat-bar');
    statBars.forEach(bar => {
        const value = parseInt(bar.getAttribute('data-value'));
        const maxValue = parseInt(bar.getAttribute('data-max-value') || '255');
        const percentage = (value / maxValue) * 100;
        bar.style.width = `${percentage}%`;
    });
});
