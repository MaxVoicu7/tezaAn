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
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    const discountsSection = document.querySelector('.discounts');

    discountsSection.innerHTML = '';
    data.forEach(discount => {
      const discountElement = createDiscountElement(discount);
      discountsSection.appendChild(discountElement);
    });
  })
  .catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
  });



  function createDiscountElement(discount) {
    // Crează elementul div pentru discount
    const discountDiv = document.createElement('div');
    discountDiv.classList.add('discount');
  
    // Secțiunea de prezentare a discount-ului
    const presentationDiv = document.createElement('div');
    presentationDiv.classList.add('discount__presentation');
  
    const labelSpan = document.createElement('span');
    labelSpan.classList.add('discount__label');
    labelSpan.textContent = discount.products.join(', ');  // Listă de produse
  
    const infoP = document.createElement('p');
    infoP.classList.add('discount__info');
    infoP.textContent = discount.discount_value;

    const descriptionP = document.createElement('p');
    descriptionP.classList.add('discount__description');
    descriptionP.textContent = discount.description;
  
    presentationDiv.appendChild(labelSpan);
    presentationDiv.appendChild(infoP);
    presentationDiv.appendChild(descriptionP);
  
    // Secțiunea de preț
    const priceDiv = document.createElement('div');
    priceDiv.classList.add('discount__price');
  
    const pricesDiv = document.createElement('div');
    pricesDiv.classList.add('prices');
  
    const oldPriceP = document.createElement('p');
    oldPriceP.classList.add('old-price');
    oldPriceP.textContent = discount.initial_price;
  
    const newPriceP = document.createElement('p');
    newPriceP.classList.add('new-price');
    newPriceP.textContent = discount.final_price;
  
    pricesDiv.appendChild(oldPriceP);
    pricesDiv.appendChild(newPriceP);
  
    const buttonDiv = document.createElement('div');
    buttonDiv.classList.add('discount__button');
  
    const button = document.createElement('button');
    button.classList.add('btn');
    button.textContent = 'Mai mult';
  
    buttonDiv.appendChild(button);

    button.onclick = function() {
      openPopupDetail(discount);
    };
  
    priceDiv.appendChild(pricesDiv);
    priceDiv.appendChild(buttonDiv);
  
    // Adaugă secțiunile la elementul principal de discount
    discountDiv.appendChild(presentationDiv);
    discountDiv.appendChild(priceDiv);
  
    return discountDiv;
  }
  


  document.getElementById('filter-submit').addEventListener('click', function() {
    // Obține valorile selectate de utilizator
    const selectedCategory = document.getElementById('category-select').value;
    const startPrice = document.getElementById('start-value').value;
    const endPrice = document.getElementById('end-value').value;

    const requestData = {
      category: selectedCategory,
      priceRange: {
        start: startPrice,
        end: endPrice
      }
    };


    
    fetch('http://localhost:5555/discount-info', {
      method: 'POST',  // sau 'GET', în funcție de cum este configurat backend-ul tău
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
      const discountsSection = document.querySelector('.discounts');
  
      discountsSection.innerHTML = '';
      data.forEach(discount => {
        const discountElement = createDiscountElement(discount);
        discountsSection.appendChild(discountElement);
      });
    })
    .catch(error => {
      console.error('There has been a problem with your fetch operation:', error);
    });


  });
  




  function openPopupDetail(discount) {
    document.getElementById('popup-title').textContent = `Detalii Reducere #${discount.id}`;
    document.getElementById('popup-description').textContent = discount.description;
    document.getElementById('popup-initial-price').textContent = discount.initial_price;
    document.getElementById('popup-final-price').textContent = discount.final_price;
    document.getElementById('popup-start-date').textContent = discount.start_date;
    document.getElementById('popup-end-date').textContent = discount.end_date;

    // Șterge orice magazine listate anterior
    const storesContainer = document.getElementById('popup-stores');
    while (storesContainer.firstChild) {
        storesContainer.removeChild(storesContainer.firstChild);
    }

    // Adaugă un titlu pentru secțiunea magazinelor
    const storesTitle = document.createElement('h3');
    storesTitle.textContent = 'Disponibil în magazinele';
    storesContainer.appendChild(storesTitle);

    console.log(discount.stores);

    // Creează și adaugă lista de magazine
    discount.stores.forEach((store) => {
        const storeDiv = document.createElement('div');
        storeDiv.classList.add('store-info');

        const storeName = document.createElement('h4');
        storeName.textContent = store.name;

        const storeAddress = document.createElement('p');
        storeAddress.textContent = `Adresa: ${store.address}`;

        const storeHours = document.createElement('p');
        storeHours.textContent = `Orar: ${store.working_hours}`;

        storeDiv.appendChild(storeName);
        storeDiv.appendChild(storeAddress);
        storeDiv.appendChild(storeHours);

        storesContainer.appendChild(storeDiv);
    });

    // Afișează pop-up-ul
    document.getElementById('discount-detail-popup').style.display = 'flex';
}


function closePopupDetail() {
    document.getElementById('discount-detail-popup').style.display = 'none';
}