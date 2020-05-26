table = document.querySelector('table');
header = document.querySelector('header');

function populateTable(jsonObj) {
    
    var count = 0;
    
    for(const object in jsonObj) {
        count++;
    }
    
    //create header
    text = document.createElement('p');
    text.textContent = count + " printer(s) were found.";
    header.appendChild(text);
    
    //create table headders
    headerRow = document.createElement('tr');
    header1 = document.createElement('th');
    header2 = document.createElement('th');
    header3 = document.createElement('th');
    header4 = document.createElement('th');
    header5 = document.createElement('th');
    header6 = document.createElement('th');
    
    header1.textContent = "Status"
    header2.textContent = "Host";
    header3.textContent = "IP Address";
    header4.textContent = "Port";
    header5.textContent = "Series";
    header6.textContent = "Version";
    
    headerRow.appendChild(header1);
    headerRow.appendChild(header2);
    headerRow.appendChild(header3);
    headerRow.appendChild(header4);
    headerRow.appendChild(header5);
    headerRow.appendChild(header6);
    table.appendChild(headerRow);
    

    for(const object in jsonObj) {
        //create table columns
        row = document.createElement('tr');
        col1 = document.createElement('td');
        col2 = document.createElement('td');
        col3 = document.createElement('td');
        col4 = document.createElement('td');
        col5 = document.createElement('td');
        col6 = document.createElement('td');
        
        //get printer info
        temp = jsonObj[object];
        
        //create hyperlink
        a = document.createElement('a');
        link = document.createTextNode(temp.address);
        a.appendChild(link);
        a.title = temp.address;
        a.href = "http://" + temp.address + ":" + temp.port;
          
        //set printer status and icon
        var icon = document.createElement('span');
        if(temp.stat == 0){
            col1.textContent = "Offline";
            icon.style = "font-size: 16px; color: Red; float:right;";
            icon.textContent = '\u2612';
        }
        else if (temp.stat == 1){
            col1.textContent = "Server Offline";
            icon.style = "font-size: 18px; color: Orange; float:right;";
            icon.textContent = '\u2610';
        }
        else if (temp.stat == 2){
            col1.textContent = "Online";
            icon.style = "font-size: 16px; color: Green; float:right;";
            icon.textContent = '\u2611';
        }
        else{
            col1.textContent = "Loading";
            icon.style = "font-size: 16px; float:right;";
            icon.textContent = '\u2610';
        }
        col1.appendChild(icon);
        
        col2.textContent = object;
        col3.appendChild(a);
        col4.textContent = temp.port;
        col5.textContent = temp.series;
        col6.textContent = temp.version;
        
        row.appendChild(col1);
        row.appendChild(col2);
        row.appendChild(col3);
        row.appendChild(col4);
        row.appendChild(col5);
        row.appendChild(col6);
        table.appendChild(row);
    }
}
populateTable(printers);
