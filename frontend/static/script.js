document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('docGenForm');
    const statusDiv = document.getElementById('status');
    const outputPre = document.getElementById('output');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        statusDiv.textContent = 'Generating documentation...';
        outputPre.textContent = '';

        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            const result = await response.json();

            if (response.ok) {
                statusDiv.textContent = 'Documentation generated successfully!';
                outputPre.textContent = JSON.stringify(result, null, 2);
            } else {
                statusDiv.textContent = `Error: ${result.detail || 'Unknown error'}`;
                outputPre.textContent = JSON.stringify(result, null, 2);
            }
        } catch (error) {
            statusDiv.textContent = `Network error: ${error.message}`;
            console.error('Error:', error);
        }
    });
});
