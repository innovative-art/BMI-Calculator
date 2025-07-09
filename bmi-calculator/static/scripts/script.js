document.addEventListener('DOMContentLoaded', () => {
    const bmiForm = document.getElementById('bmiForm');
    const resultDiv = document.getElementById('result');

    bmiForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const height = document.getElementById('height').value.trim();
        const weight = document.getElementById('weight').value.trim();

        if (!height || !weight || isNaN(height) || isNaN(weight)) {
            resultDiv.innerHTML = "<p style='color: red;'>Please enter valid height and weight values.</p>";
            return;
        }

        try {
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ height, weight })
            });

            if (!response.ok) throw new Error("Failed to fetch BMI data.");

            const data = await response.json();
            renderResult(data);
        } catch (error) {
            resultDiv.innerHTML = `<p style='color: red;'>Error: ${error.message}</p>`;
        }
    });

    function renderResult(data) {
        let resultHTML = `
            <h2>BMI: ${data.bmi}</h2>
            <p>Status: ${data.status}</p>
            <p>Diet: ${data.diet}</p>
            <p>Ideal Weight Range: ${data.ideal_weight_range}</p>
            <h3>Recommended Foods:</h3>
        `;

        for (const category in data.foods) {
            resultHTML += `<div class="food-category">
                <h4>${category}</h4>
                <div class="food-list">`;

            data.foods[category].forEach(food => {
                resultHTML += `
                    <div class="food-item">
                        <img src="${food.image}" alt="${food.name}">
                        <span>${food.name}</span>
                    </div>`;
            });

            resultHTML += `</div></div>`;
        }

        resultDiv.innerHTML = resultHTML;
    }
});
