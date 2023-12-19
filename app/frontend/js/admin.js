document.addEventListener('DOMContentLoaded', updateDiscountCounts);



document.querySelector('.insight-btn.expired-discount').addEventListener('click', function() {
  fetch('http://localhost:5555/admin-discount/expired')
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
        row.id = 'discount-row-' + discount.discount_id;
        const discountDataString = JSON.stringify(discount).replace(/"/g, '\\"');
        row.innerHTML = `
            <td>${discount.discount_id}</td>
            <td>${discount.start_date}</td>
            <td>${discount.end_date}</td>
            <td>${discount.discount_type}</td>
            <td><i class='bx info-btn bxs-info-circle' onclick='openPopupInfo("${discountDataString}")'></i></td>
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
  fetch('http://localhost:5555/admin-discount/actual')
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
            <td><i class='bx edit-btn bxs-edit-alt' onclick='openPopupEdit("${discount.discount_id}")'></i></td>
            <td><i class='bx delete-btn bxs-trash-alt' onclick='openDeletePopup(${discount.discount_id})'></i></td>
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
  fetch('http://localhost:5555/admin-discount/future')
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
      row.id = 'discount-row-' + discount.discount_id;
      row.innerHTML = `
          <td>${discount.discount_id}</td>
          <td>${discount.start_date}</td>
          <td>${discount.end_date}</td>
          <td>${discount.discount_type}</td>
          <td><i class='bx edit-btn bxs-edit-alt' onclick='openPopupEdit("${discount.discount_id}")'></i></td>
          <td><i class='bx delete-btn bxs-trash-alt' onclick='openDeletePopup(${discount.discount_id})'></i></td>
      `;
      tableBody.appendChild(row);
    });
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
});


function openPopupEdit(discountId) {
  fetch(`http://localhost:5555/discount/${discountId}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      const discount = data.discount; 
      const popup = document.getElementById("edit-discount-popup");
      popup.setAttribute('data-discount-id', discount.discount_id);
    
      document.getElementById('discount-id').textContent = 'Editează Reducerea ' + (discount.discount_id || '');
      document.getElementById('discount_description').value = discount.discount_description || '';
      document.getElementById('start_date').value = discount.start_date || '';
      document.getElementById('end_date').value = discount.end_date || '';
    
      document.getElementById("edit-discount-popup").style.display = "block";
      document.getElementById("overlay").style.display = "block";
    })
    .catch(error => {
      console.error("Eroare la obținerea datelor discount-ului: ", error);
    });
}




function closePopupEdit() {
  document.getElementById("edit-discount-popup").style.display = "none";
  document.getElementById("overlay").style.display = "none";
}



function saveEditChanges() {
  const popup = document.getElementById("edit-discount-popup");
  const discountId = popup.getAttribute('data-discount-id');

  const discountDescription = document.getElementById('discount_description').value;
  const startDate = document.getElementById('start_date').value;
  const endDate = document.getElementById('end_date').value;

  const discountData = {
      discount_description: discountDescription,
      start_date: startDate,
      end_date: endDate
  };

  const fetchOptions = {
      method: 'PUT',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(discountData)
  };

  fetch(`http://localhost:5555/discount/${discountId}`, fetchOptions)
      .then(response => {
          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
      })
      .then(data => {
          console.log('Success:', data);
          updateTableRow(discountId, discountData);
          closePopupEdit();
      })
      .catch((error) => {
          console.error('Error:', error);
      });
}



function openDeletePopup(discountId) {
  document.getElementById('confirm-delete').setAttribute('data-discount-id', discountId);
  document.getElementById("overlay").style.display = "block";
  document.getElementById('delete-confirmation-popup').style.display = 'block';
}


function closeDeletePopup() {
  document.getElementById('delete-confirmation-popup').style.display = 'none';
  document.getElementById("overlay").style.display = "none";
}



function confirmDelete() {
  var discountId = document.getElementById('confirm-delete').getAttribute('data-discount-id');
  fetch(`http://localhost:5555/discount/${discountId}`, { method: 'DELETE' })
      .then(response => response.json())
      .then(data => {
          console.log(data);
          closeDeletePopup();
          removeDiscountFromTable(discountId);
          updateDiscountCounts();
      })
      .catch(error => console.error('Error:', error));
}











function openPopupInfo(discountDataString) {
  const discount = JSON.parse(discountDataString);

  document.getElementById('info-discount-id').textContent = 'Informații Reducere #' + (discount.discount_id || '');
  document.getElementById('info-discount-description').textContent = discount.discount_description || 'N/A';
  document.getElementById('info-start-date').textContent = discount.start_date || 'N/A';
  document.getElementById('info-end-date').textContent = discount.end_date || 'N/A';
  
  document.getElementById("overlay").style.display = "block";
  document.getElementById("info-discount-popup").style.display = "block";
}

function closePopupInfo() {
  document.getElementById("info-discount-popup").style.display = "none";
  document.getElementById("overlay").style.display = "none";
}






function removeDiscountFromTable(discountId) {
  let rowToDelete = document.getElementById('discount-row-' + discountId);
  if (rowToDelete) {
      rowToDelete.remove();
  }
}




function updateTableRow(discountId, discountData) {
  let row = document.getElementById('discount-row-' + discountId);
  if (row) {
    row.cells[1].textContent = discountData.start_date;
    row.cells[2].textContent = discountData.end_date;
  }
}



function updateDiscountCounts() {
  fetch('http://localhost:5555/admin-discount')
    .then(response => response.json())
    .then(data => {
      document.getElementById('active-discount-count').textContent = `Total: ${data.current_discounts_count}`;
      document.getElementById('expired-discount-count').textContent = `Total: ${data.past_discounts_count}`;
      document.getElementById('future-discount-count').textContent = `Total: ${data.future_discounts_count}`;
    })
    .catch(error => console.error('Error:', error));
}

