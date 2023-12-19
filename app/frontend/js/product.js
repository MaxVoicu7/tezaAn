fetch('http://localhost:5555/product')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(products => {
    const tableBody = document.getElementById('product-table-body');
    tableBody.innerHTML = ''; 

    products.forEach(product => {
      const row = tableBody.insertRow();
      row.innerHTML = `
        <td>${product.product_id}</td>
        <td>${product.product_name}</td>
        <td>${product.category_name}</td>
        <td>${product.manufacturer_name}</td>
        <td>${product.product_volume}</td>
        <td>${product.product_price}</td>
        <td>${product.unique_code}</td>
      `;
    });
  })
  .catch(error => {
    console.error('Error:', error);
  });





  document.getElementById('add-product-btn').addEventListener('click', function() {
    window.location.href = './../frontend/add_product.html'; 
  });