printers = {
  "HR3v3": {
    "address": "10.37.35.247:5000",
    "series": "HR",
    "version": "3.3"
  }
}

table = document.querySelector('table');
header = document.querySelector('header');

function populateTable(jsonObj) {
    
    var count = 0;
    
    for(const object in jsonObj) {
        count++;
    }
    
    text = document.createElement('p');
    text.textContent = count + " printer(s) were found.";
    header.appendChild(text);

    for(const object in jsonObj) {
    
        row = document.createElement('tr');
        col1 = document.createElement('td');
        col2 = document.createElement('td');
        col3 = document.createElement('td');
        col4 = document.createElement('td');
        
        temp = jsonObj[object];
          
        col1.textContent = object
        col2.textContent = temp.address;
        col3.textContent = temp.series;
        col4.textContent = temp.version;
        
        row.appendChild(col1);
        row.appendChild(col2);
        row.appendChild(col3);
        row.appendChild(col4);
        table.appendChild(row);
    }
}
populateTable(printers);
