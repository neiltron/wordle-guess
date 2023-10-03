import './styles/main.scss'

document.getElementById('submit').addEventListener('click', async (e) => {
    e.preventDefault();

    const userInput = document.getElementById('userInput').value
    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: userInput
        })
        const data = await response.json()
        const outputEl = document.getElementById('output');

        outputEl.innerHTML = '';

        data['top_probable_first_guesses'].forEach(el => {
            outputEl.innerHTML += `<li>${el[0]}: ${el[1]}</li>`
        })
    } catch (error) {
        console.error('Error fetching predictions:', error)
    }
})