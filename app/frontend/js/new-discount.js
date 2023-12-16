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




document.querySelector(".discount-form__body").addEventListener("submit", function(event) {
  let selectedValue = document.getElementById("discount-type").value;
  if(selectedValue < 1 || selectedValue > 4) {
      event.preventDefault();
      alert('selecteaza un tip de reducere');
      return;
  }

  let checkboxes = document.querySelectorAll("#stores-fields-container input[type='checkbox']");
  let isChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);

  if(!isChecked) {
      event.preventDefault();
      alert('Selectează cel puțin un magazin');
      return;
  }

      // Validarea datelor de început și sfârșit
      let startDate = new Date(document.getElementById("start-date").value);
      let endDate = new Date(document.getElementById("end-date").value);
      let today = new Date();
      today.setHours(0, 0, 0, 0); // Resetează ora, minutele, secundele și milisecundele
  
      if(startDate < today) {
          event.preventDefault();
          alert('Ziua de început a reducerii trebuie să fie cel puțin egală cu ziua de azi');
          return;
      }
  
      if(endDate <= today) {
          event.preventDefault();
          alert('Ziua de sfârșit a reducerii trebuie să fie mai mare decât ziua de azi');
          return;
      }
  
      if(endDate <= startDate) {
          event.preventDefault();
          alert('Ziua de sfârșit a reducerii trebuie să fie după ziua de început');
          return;
      }

  
    let formData = {
        discount_description: document.getElementById("description").value,
        start_date: document.getElementById("start-date").value,
        end_date: document.getElementById("end-date").value,
        discount_type: document.getElementById("discount-type").value,
    };

    if (formData.discount_type === "1") {
      formData.discount_percentage = document.getElementById("percentage-value").value;
      formData.product_code = document.getElementById("product-code-percentage").value;
    }
    else if (formData.discount_type === "2") {
      formData.product_code = document.getElementById("product-code-fixed").value;
      formData.discount_fixed_value = document.getElementById("fixed-value").value;
    }
    else if (formData.discount_type === "3") {
      let numberOfProducts = parseInt(document.getElementById("number-of-products").value, 10);
      let productCodes = [];

      for (let i = 0; i < numberOfProducts; i++) {
            let productCode = document.getElementById(`product-code-${i}`).value; // Presupunem că ai ID-uri dinamice pentru fiecare câmp de cod al produsului
            if (productCode) {
                productCodes.push(productCode);
            }
        }

        let finalPrice = document.getElementById("final-price").value;
        formData.product_codes = productCodes;
        formData.final_price = finalPrice;
    }
    else if (formData.discount_type === "4") {
      formData.product_code = document.getElementById("product-code-quantity").value;
      formData.free_quantity = document.getElementById("quantity-free").value;
      formData.required_quantity = document.getElementById("quantity-required").value;
    }

    let storeCheckboxes = document.querySelectorAll("#stores-fields-container input[type='checkbox']:checked");
    let selectedStoreIds = Array.from(storeCheckboxes).map(checkbox => checkbox.value);
    formData.stores = selectedStoreIds;

    // Opțional: Loghează formData pentru a verifica datele
    console.log(formData);

    fetch('http://localhost:5555/admin-discount', {
        method: 'POST', // Metoda HTTP pentru trimitere
        headers: {
            'Content-Type': 'application/json', // Specifică faptul că trimitem date în format JSON
        },
        body: JSON.stringify(formData) // Convertim obiectul formData în JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Procesează răspunsul JSON
    })
    .then(data => {
        console.log('Success:', data);
        // Aici poți adăuga logica pentru succes (ex: redirecționare, afișare mesaj de succes etc.)
    })
    .catch((error) => {
        console.error('Error:', error);
        // Aici poți gestiona erorile (ex: afișare mesaj de eroare)
    });

    event.preventDefault();
});