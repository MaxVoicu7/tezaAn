document.addEventListener('DOMContentLoaded', function() {
  fetch('http://localhost:5555/admin-discount')
  .then(response => response.json())
  .then(data => {
    // Actualizează numărul de reduceri în elementele respective
    document.getElementById('active-discount-count').textContent = `Total: ${data.current_discounts_count}`;
    document.getElementById('expired-discount-count').textContent = `Total: ${data.past_discounts_count}`;
    document.getElementById('future-discount-count').textContent = `Total: ${data.future_discounts_count}`;
  })
  .catch(error => {
    console.error('Error:', error);
  });
});



document.querySelector('.insight-btn.expired-discount').addEventListener('click', function() {
  fetch('http://localhost:5555/admin-expired-discount')
  .then(response => response.json())
  .then(data => {
    const textContainer = document.querySelector('.discount-status-title');
    const tableContainer = document.querySelector('.discount-table-container');

    if (data.length == 0) {
      textContainer.innerHTML = 'Reducerile anterioare nu sunt disponibile';
      tableContainer.innerHTML = '';
    }
    else {
      textContainer.innerHTML = 'Reduceri anterioare';
      tableContainer.innerHTML = `
        <table class="discount-table">
            <thead>
                <tr>
                    <th>Discount ID</th>
                    <th>Început</th>
                    <th>Sfârșit</th>
                    <th>Tip reducere</th>
                    <th>Informație</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
      `;

      const tableBody = tableContainer.querySelector('tbody');

      data.forEach(discount => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${discount.discount_id}</td>
            <td>${discount.start_date}</td>
            <td>${discount.end_date}</td>
            <td>${discount.discount_type}</td>
            <td><i class='bx info-btn bxs-info-circle'></i></td>
        `;
        tableBody.appendChild(row);
      });
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
});



document.querySelector('.insight-btn.active-discount').addEventListener('click', function() {
  fetch('http://localhost:5555/admin-actual-discount')
  .then(response => response.json())
  .then(data => {
    const textContainer = document.querySelector('.discount-status-title');
    const tableContainer = document.querySelector('.discount-table-container');

    if (data.length == 0) {
      textContainer.innerHTML = 'Nu sunt reduceri active la moment';
      tableContainer.innerHTML = '';
    }
    else {
      textContainer.innerHTML = 'Reduceri ce sunt disponibile acum';
      tableContainer.innerHTML = `
        <table class="discount-table">
            <thead>
                <tr>
                    <th>Discount ID</th>
                    <th>Început</th>
                    <th>Sfârșit</th>
                    <th>Tip reducere</th>
                    <th>Modifică</th>
                    <th>Șterge</th>
                </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
      `;

      const tableBody = tableContainer.querySelector('tbody');

      data.forEach(discount => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${discount.discount_id}</td>
            <td>${discount.start_date}</td>
            <td>${discount.end_date}</td>
            <td>${discount.discount_type}</td>
            <td><i class='bx edit-btn bxs-edit-alt' ></i></td>
            <td><i class='bx delete-btn bxs-trash-alt'></i></td>
        `;
        tableBody.appendChild(row);
      });
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
});



document.querySelector('.insight-btn.future-discount').addEventListener('click', function() {
  fetch('http://localhost:5555/admin-future-discount')
  .then(response => response.json())
  .then(data => {
    const textContainer = document.querySelector('.discount-status-title');
    const tableContainer = document.querySelector('.discount-table-container');

    if (data.length == 0) {
      textContainer.innerHTML = 'Nu sunt planificate reduceri pentru viitor';
      tableContainer.innerHTML = '';
    }
    else {
      textContainer.innerHTML = 'Reduceri ce vor fi disponibile în curând';
    tableContainer.innerHTML = `
      <table class="discount-table">
          <thead>
              <tr>
                  <th>Discount ID</th>
                  <th>Început</th>
                  <th>Sfârșit</th>
                  <th>Tip reducere</th>
                  <th>Modifică</th>
                  <th>Șterge</th>
              </tr>
          </thead>
          <tbody>
          </tbody>
      </table>
    `;

    const tableBody = tableContainer.querySelector('tbody');

    data.forEach(discount => {
      const row = document.createElement('tr');
      row.innerHTML = `
          <td>${discount.discount_id}</td>
          <td>${discount.start_date}</td>
          <td>${discount.end_date}</td>
          <td>${discount.discount_type}</td>
          <td><i class='bx edit-btn bxs-edit-alt' ></i></td>
          <td><i class='bx delete-btn bxs-trash-alt'></i></td>
      `;
      tableBody.appendChild(row);
    });
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
});