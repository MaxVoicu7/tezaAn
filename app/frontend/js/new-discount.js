document.addEventListener('DOMContentLoaded', function() {
  const selectElement = document.getElementById('discount-type');
  const fieldsContainer = document.getElementById('specific-fields-container');

  selectElement.addEventListener('change', function(event) {
    const value = event.target.value;
    fieldsContainer.innerHTML = ''; // Clear the container
    
    if (value === '1') {
      // Reducere procentuală
      fieldsContainer.innerHTML = `
        <div class="discount-form__group">
          <label for="product-code-percentage" class="discount-form__label">Cod produs:</label>
          <input type="text" id="product-code-percentage" name="product-code-percentage" required class="discount-form__input">
        </div>
        <div class="discount-form__group">
          <label for="percentage-value" class="discount-form__label">Valoarea procentuală a reducerii:</label>
          <input type="number" id="percentage-value" name="percentage-value" required class="discount-form__input">
        </div>
      `;
    } else if (value === '4') {
      // Reducere cantitativă
      fieldsContainer.innerHTML = `
        <div class="discount-form__group">
          <label for="product-code-quantity" class="discount-form__label">Cod produs:</label>
          <input type="text" id="product-code-quantity" name="product-code-quantity" required class="discount-form__input">
        </div>
        <div class="discount-form__group">
          <label for="quantity-required" class="discount-form__label">Cantitate necesară:</label>
          <input type="number" id="quantity-required" name="quantity-required" required class="discount-form__input">
        </div>
        <div class="discount-form__group">
          <label for="quantity-free" class="discount-form__label">Cantitate gratis:</label>
          <input type="number" id="quantity-free" name="quantity-free" required class="discount-form__input">
        </div>
      `;
    } else if (value === '2') {
      // Reducere de valoare fixă
      fieldsContainer.innerHTML = `
        <div class="discount-form__group">
          <label for="product-code-fixed" class="discount-form__label">Cod produs:</label>
          <input type="text" id="product-code-fixed" name="product-code-fixed" required class="discount-form__input">
        </div>
        <div class="discount-form__group">
          <label for="fixed-value" class="discount-form__label">Valoarea reducerii:</label>
          <input type="number" id="fixed-value" name="fixed-value" required class="discount-form__input">
        </div>
      `;
    } else if (value === '3') {
      // Reducere complementară
      fieldsContainer.innerHTML = `
        <div class="discount-form__group">
          <label for="number-of-products" class="discount-form__label">Numărul de produse:</label>
          <input type="number" id="number-of-products" name="number-of-products" required class="discount-form__input">
        </div>
        <div class="discount-form__group" id="complementary-products-container">
          <!-- Aici vor fi adăugate câmpurile pentru codul produsului -->
        </div>
        <div class="discount-form__group">
          <label for="final-price" class="discount-form__label">Preț final:</label>
          <input type="number" id="final-price" name="final-price" required class="discount-form__input">
        </div>
      `;

      const numberOfProductsElement = document.getElementById('number-of-products');
      numberOfProductsElement.addEventListener('change', function(event) {
        const numberOfProducts = event.target.value;
        const productsContainer = document.getElementById('complementary-products-container');
        productsContainer.innerHTML = ''; // Clear the container
        
        for (let i = 0; i < numberOfProducts; i++) {
          const productInputGroup = document.createElement('div');
          productInputGroup.classList.add('discount-form__group');
          productInputGroup.innerHTML = `
            <label for="product-code-${i}" class="discount-form__label">Cod produs ${i+1}:</label>
            <input type="text" id="product-code-${i}" name="product-code-${i}" required class="discount-form__input">
          `;
          productsContainer.appendChild(productInputGroup);
        }
      });
    }
  });

  fetchStores();
});





function fetchStores() {
  fetch('http://localhost:5555/store')
    .then(response => response.json())
    .then(stores => {
      const storesContainer = document.getElementById('stores-fields-container');
      let fieldsetContent = `<fieldset><legend>Informații de Contact</legend>`; // Începe construirea conținutului fieldset
      
      stores.forEach(store => {
        // Adaugă fiecare label și checkbox în variabila fieldsetContent
        fieldsetContent += `
          <label for="store-${store.store_id}">
            <input type="checkbox" id="store-${store.store_id}" name="stores" value="${store.store_id}">
            ${store.store_name} - ${store.address}
          </label><br>`;
      });

      fieldsetContent += `</fieldset>`; // Închide tag-ul fieldset
      storesContainer.innerHTML = fieldsetContent; // Adaugă tot conținutul în storesContainer
    })
    .catch(error => {
      console.error('Error fetching stores:', error);
    });
}
