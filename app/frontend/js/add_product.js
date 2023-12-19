window.addEventListener('load', () => {
  populateDropdown('manufacturer-select', 'http://localhost:5555/manufacturer');
  populateDropdown('category-select', 'http://localhost:5555/category');
});



function populateDropdown(dropdownId, url) {
  fetch(url)
    .then(response => response.json())
    .then(data => {
      const select = document.getElementById(dropdownId);
      data.forEach(item => {
        const option = new Option(item.name, item.id);
        select.add(option);
      });
    })
    .catch(error => console.error('Error:', error));
}



document.getElementById('add-product-form').addEventListener('submit', function(event) {
  event.preventDefault();

  const productName = document.getElementById('product-name').value.trim();
  const productVolume = document.getElementById('product-volume').value.trim();
  const manufacturerId = document.getElementById('manufacturer-select').value.trim();
  const uniqueCode = document.getElementById('unique-code').value.trim();
  const productPrice = document.getElementById('product-price').value.trim();
  const categoryId = document.getElementById('category-select').value.trim();

  const fields = [
    { value: productName, name: 'Nume' },
    { value: productVolume, name: 'Volum' },
    { value: manufacturerId, name: 'Producător' },
    { value: uniqueCode, name: 'Cod Unic' },
    { value: productPrice, name: 'Preț' },
    { value: categoryId, name: 'Categorie' }
  ];

  for (const field of fields) {
    if (!field.value) {
      alert(`Te rog să completezi câmpul "${field.name}".`);
      return;
    }
  }

  const productData = {
    name: productName,
    volume: productVolume,
    manufacturer_id: manufacturerId,
    unique_code: uniqueCode,
    price: productPrice,
    category_id: categoryId
  };

  console.log(productData)

  fetch('http://localhost:5555/product', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(productData)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Răspunsul rețelei nu a fost ok.');
    }
    return response.json();
  })
  .then(data => {
    alert('Produs adăugat cu succes!');
    window.location.href = './../frontend/product.html';
  })
  .catch(error => {
    alert('A apărut o eroare la adăugarea produsului.');
    console.error('Error:', error);
  });
});