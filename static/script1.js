document.getElementById('calorieForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    let formData = new FormData(event.target);
    let data = {};
    formData.forEach((value, key) => { data[key] = isNaN(value) ? value : parseFloat(value); });

    fetch('/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        let output = `<h3>Daily Calories Needed: ${result.daily_calories.toFixed(2)} kcal</h3>`;
        output += `<h3>Meal Plan:</h3>`;
        result.meal_plan.forEach((day, index) => {
            output += `<h4>Day ${index + 1}</h4><ul>`;
            for (let meal in day) {
                output += `<li><strong>${meal}:</strong> ${day[meal].item} - ${day[meal].grams}g (${day[meal].calories.toFixed(2)} kcal)</li>`;
            }
            output += `</ul>`;
        });
        document.getElementById('result').innerHTML = output;
    });
});

// Prevent back navigation to login/register after login
if (window.history.replaceState) {
    window.history.pushState(null, "", window.location.href);
    window.onpopstate = function () {
        window.location.href = "/"; // Redirect to index.html
    };
}
