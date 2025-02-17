document.getElementById('calorieForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    // Show loading state
    const button = event.target.querySelector('button');
    const originalText = button.innerHTML;
    button.innerHTML = `
        <div class="button-content">
            <svg class="animate-spin" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
            <span>Calculating...</span>
        </div>
        <div class="button-glow"></div>
    `;
    
    let formData = new FormData(event.target);
    let data = {};
    formData.forEach((value, key) => { 
        data[key] = isNaN(value) ? value : parseFloat(value); 
    });

    fetch('/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        // Reset button state
        button.innerHTML = originalText;

        // Clear previous results with fade out
        const resultElement = document.getElementById('result');
        resultElement.style.opacity = '0';
        
        setTimeout(() => {
            // Build new result HTML
            let output = `
                <h3>Daily Calorie Target: ${result.daily_calories.toFixed(0)} kcal</h3>
                <div class="meal-plan">
            `;
            
            result.meal_plan.forEach((day, index) => {
                output += `
                    <h4>Day ${index + 1}</h4>
                    <ul>
                `;
                
                for (let meal in day) {
                    output += `
                        <li>
                            <strong>${meal}:</strong> 
                            ${day[meal].item} - ${day[meal].grams}g 
                            <span class="calories">(${day[meal].calories.toFixed(0)} kcal)</span>
                        </li>
                    `;
                }
                
                output += `</ul>`;
            });
            
            output += `</div>`;
            
            // Show new results with fade in
            resultElement.innerHTML = output;
            resultElement.style.opacity = '1';
            
            // Scroll to results on mobile
            if (window.innerWidth <= 1200) {
                resultElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }, 300);
    })
    .catch(error => {
        console.error('Error:', error);
        button.innerHTML = originalText;
        alert('An error occurred while generating your meal plan. Please try again.');
    });
});

// Add animation to form inputs
document.querySelectorAll('input, select').forEach(element => {
    element.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
    });
    
    element.addEventListener('blur', function() {
        this.parentElement.classList.remove('focused');
    });
});
