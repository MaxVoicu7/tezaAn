let navbar = document.querySelector('.header .navbar');

document.querySelector('#menu-btn').onclick = () => {
  navbar.classList.toggle('active');
}



fetch('http://localhost:5555/category')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    const selectElement = document.getElementById('category-select');

    data.forEach(category => {
      const option = document.createElement('option');
      option.value = category.id;
      option.textContent = category.name;
      selectElement.appendChild(option);
    });
  })
  .catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
  });



fetch('http://localhost:5555/discount')
  .then(response => {
    // Verifică dacă răspunsul este ok (status 200)
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json(); // Converteste răspunsul în JSON
  })
  .then(data => {
    // Aici ai datele tale, le poți prelucra după nevoie
    console.log('Discounts:', data); // Afișează datele în consolă

    // Dacă vrei să faci ceva în plus cu datele, poți adăuga cod aici
  })
  .catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
  });
