const form = document.getElementById('predictionForm');
const submitBtn = document.getElementById('submitBtn');
const randomBtn = document.getElementById('randomBtn');
const resultCard = document.getElementById('resultCard');
const inputCard = document.querySelector('.input-card');

randomBtn.addEventListener('click', async () => {
    randomBtn.textContent = 'Loading...';
    try {
        const response = await fetch('http://127.0.0.1:5000/random_sample');
        const data = await response.json();
        
        // Populate text fields
        document.getElementById('title').value = data.title || '';
        document.getElementById('company_profile').value = data.company_profile || '';
        document.getElementById('description').value = data.description || '';
        document.getElementById('requirements').value = data.requirements || '';
        document.getElementById('benefits').value = data.benefits || '';
        
        // Populate dropdowns
        document.getElementById('employment_type').value = data.employment_type || 'Full-time';
        document.getElementById('required_experience').value = data.required_experience || 'Entry level';
        document.getElementById('required_education').value = data.required_education || 'Unspecified';
        document.getElementById('industry').value = data.industry || 'Other';
        
        // Populate checkboxes
        document.getElementById('telecommuting').checked = data.telecommuting == 1;
        document.getElementById('has_company_logo').checked = data.has_company_logo == 1;
        document.getElementById('has_questions').checked = data.has_questions == 1;
        
    } catch (error) {
        console.error('Error fetching random sample:', error);
        alert('Could not fetch random sample. Is the backend running?');
    } finally {
        randomBtn.textContent = 'Load Random Sample';
    }
});

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;

    const formData = {
        title: document.getElementById('title').value,
        company_profile: document.getElementById('company_profile').value,
        description: document.getElementById('description').value,
        requirements: document.getElementById('requirements').value,
        benefits: document.getElementById('benefits').value,
        employment_type: document.getElementById('employment_type').value,
        required_experience: document.getElementById('required_experience').value,
        required_education: document.getElementById('required_education').value,
        industry: document.getElementById('industry').value,
        telecommuting: document.getElementById('telecommuting').checked ? 1 : 0,
        has_company_logo: document.getElementById('has_company_logo').checked ? 1 : 0,
        has_questions: document.getElementById('has_questions').checked ? 1 : 0
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        displayResult(data);
    } catch (error) {
        console.error('Error:', error);
        alert('Could not connect to the backend server. Please make sure app.py is running.');
    } finally {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
    }
});

function displayResult(data) {
    const badge = document.getElementById('resultBadge');
    const gaugeFill = document.getElementById('gaugeFill');
    const confidenceText = document.getElementById('confidenceText');
    const message = document.getElementById('resultMessage');

    if (data.is_fraudulent) {
        badge.textContent = 'Fraudulent';
        badge.className = 'badge danger';
        message.textContent = 'This posting exhibits high-risk patterns. Our ensemble model identified multiple scam indicators across text and metadata.';
        gaugeFill.style.borderColor = '#ef4444';
    } else {
        badge.textContent = 'Legitimate';
        badge.className = 'badge safe';
        message.textContent = 'Our system analyzed the job details and determined this posting to be legitimate with high probability.';
        gaugeFill.style.borderColor = '#10b981';
    }

    const confidence = Math.round(data.confidence * 100);
    confidenceText.textContent = `${confidence}%`;
    const rotation = (confidence / 100) * 360;
    gaugeFill.style.transform = `rotate(${rotation}deg)`;

    inputCard.style.display = 'none';
    resultCard.style.display = 'block';
    resultCard.classList.add('fadeInUp');
}

function resetForm() {
    form.reset();
    resultCard.style.display = 'none';
    inputCard.style.display = 'block';
    inputCard.classList.add('fadeInUp');
}
