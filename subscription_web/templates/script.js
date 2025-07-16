document.getElementById('dataForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    // Gather form data
    const formData = {
        name: document.getElementById('name').value,
        number: document.getElementById('number').value,
        company: document.getElementById('company').value,
        rate: document.getElementById('rate').value,
    };

    // Send data to the backend
    try {
        const response = await fetch('http://localhost:5000/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData),
        });

        const result = await response.json();
        alert(result.message);
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to submit data');
    }
    const response = await fetch('http://localhost:5000/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
    });
    
});
