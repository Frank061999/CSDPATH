// Declare a variable to store a hashmap
let myHashMap;

// Wait for the DOM content to be loaded before executing any JavaScript
document.addEventListener('DOMContentLoaded', function () {
  fetchData();
});

// Function to fetch data from a given API endpoint
function fetchData() {
  // Fetch data from the specified API endpoint
  fetch('https://dnihzli5l8.execute-api.us-west-1.amazonaws.com/default/generateClassInfoJSON')
    .then(response => {
      // Check if the response is ok; if not, throw an error
      if (!response.ok) {
        throw new Error('Failed to fetch data');
      }
      // Parse the response as JSON
      return response.json();
    })
    .then(data => {
      // Initialize the hashmap
      myHashMap = {};
      // Iterate through the received data (JSON) and populate the hashmap
      for (let key in data) { 
        if (data.hasOwnProperty(key)) { 
          // Trim key and values to remove leading/trailing whitespace 
          let trimmedKey = key.trim();
          let trimmedClassName = data[key].className.trim();
          let trimmedPreqs = data[key].preqs.map(value => value.trim());
          let trimmedUnblock = data[key].unblock.map(value => value.trim());
          // Assign trimmed values to the hashmap
          myHashMap[trimmedKey] = {
            className: trimmedClassName,
            preqs: trimmedPreqs,
            unblock: trimmedUnblock
          };
        }
      }
      // Call functions to populate HTML, color classes, and add hover functionality  
      populateHTML();
      colorClasses();
      hoverWindow();
    })
    .catch(error => console.error('Error fetching data:', error)); // Catch and log any errors during fetch
}



// method that fill the Html cells 
function populateHTML() {
  for (let key in myHashMap) {// Loop through each key in the hashmap
    if (myHashMap.hasOwnProperty(key)) { // Check if the current key belongs to myHashMap
      let divs = document.querySelectorAll('[id="' + key + '"]');// Get all HTML (div) elements with id matching the key and store it in an array 
      let className = myHashMap[key].className; // Get the class name from the hashmap
      divs.forEach(function (div) { // Set the inner HTML of each div to the class name
        div.innerHTML = className;
      });
    }
  }
}


// method that color the html cells 
function colorClasses() {
  for (let key in myHashMap) {// Loop through each key in the hashmap
    if (myHashMap.hasOwnProperty(key)) {// Check if the current key belongs to myHashMap
      let startingCells = document.querySelectorAll('[id="' + key + '"]'); // Get all HTML (div) elements with id matching the key and store it in an array 
      let isReady = myHashMap[key].preqs.length === 0; // Check if the class is ready (no prerequisites)

      startingCells.forEach(function (cell) { // Loop through found elements 
        cell.classList.add(isReady ? 'readyColor' : 'waitingColor'); // Add color based on isReady 
      });
    }
  }
}


// method that create hover window for the cells  
function hoverWindow() {
  const hoverWindow = document.createElement('div'); // Create a new div element
  hoverWindow.id = 'hover-window'; // Set the id of the div to 'hover-window'
  hoverWindow.style.display = 'none'; // Set initial display style to 'none' (hidden)
  document.body.appendChild(hoverWindow); // Append the div to the body of the document 
  for (let key in myHashMap) { // Loop through each key in the hashmap
    if (myHashMap.hasOwnProperty(key)) { // Check if the current key belongs to myHashMap
      let divs = document.querySelectorAll('[id="' + key + '"]'); // Find HTML elements with matching IDs
      let allPreqs = myHashMap[key].preqs; // Get the prerequisites for the current class
  
      divs.forEach(function (div) { // Loop through found elements
        if (myHashMap[key].preqs.length == 0) { // Check if the class has no prerequisites
          return; // Do nothing for classes with no prerequisites
        }
  
        div.addEventListener('mouseover', function (event) { // Add mouseover event listener to each div
          var targetId = event.target.id; // Get the ID of the hovered element
          let theCell = document.getElementById(targetId); // Get the hovered cell
          if (theCell.classList.contains('waitingColor')) { // Check if the cell is waiting to be unlocked
            const rect = div.getBoundingClientRect(); // Get the position of the hovered div
            const mouseX = rect.left + window.scrollX; // Calculate X coordinate of mouse pointer
            const mouseY = rect.bottom + window.scrollY; // Calculate Y coordinate of mouse pointer
  
            let classesLeft = "Required to unlock this class: "; // Initialize message about remaining prerequisites
            for(let index = 0; index < allPreqs.length; index++){ // Loop through prerequisites
              let checkCell = document.getElementById(allPreqs[index]); // Get the prerequisite cell
              if (!checkCell.classList.contains('finishedColor')) { // Check if the prerequisite is not finished
                classesLeft = classesLeft + allPreqs[index] + ", "; // Add the prerequisite to the message
              }
            }
            hoverWindow.textContent = classesLeft; // Set the message in the hover window
            hoverWindow.style.top = mouseY + 'px'; // Position the hover window vertically
            hoverWindow.style.left = mouseX + 'px'; // Position the hover window horizontally
            hoverWindow.style.display = 'block'; // Display the hover window
          }
        });
  
        div.addEventListener('mouseout', function () { // Add mouseout event listener to each div
          hoverWindow.style.display = 'none'; // Hide the hover window when mouse leaves the div
        });
      });
    }
  }
}



document.addEventListener('click', function (event) { // Add event listener for click on document
  var targetId = event.target.id; // Get the ID of the clicked element 
  let theCell = document.getElementById(targetId); // Get the clicked cell

 
  if (theCell.classList.contains('waitingColor')) { // Check if the clicked cell is waiting
    // Do nothing
  } else if (theCell.classList.contains('readyColor')) { // If clicked cell is ready
    // Color it as done.
    let cells = document.querySelectorAll('[id="' + targetId + '"]'); // Find all cells with the same ID
    cells.forEach(function (cell) { // Iterate over found cells
      cell.classList.remove('readyColor') // Remove ready color class
      cell.classList.add('finishedColor'); // Add finished color class
    });

    // Loop to iterate through the unblock classes
    for (let index = 0; index < myHashMap[targetId].unblock.length; index++) { // Loop through unblock classes
      let classCode = myHashMap[targetId].unblock[index]; // Get unblock class code
      let isReady = true;
      for (let preqsIndex = 0; isReady && preqsIndex < myHashMap[classCode].preqs.length; preqsIndex++) {
        let preqsCode = myHashMap[classCode].preqs[preqsIndex]; // Get prerequisite code
        let checkCell = document.getElementById(preqsCode); // Get prerequisite cell
        if (!checkCell.classList.contains('finishedColor')) { // If prerequisite is not finished
          isReady = false; // Mark class as not ready
        }
      }
      if (isReady) { // If class is ready
        let theCells = document.querySelectorAll('[id="' + classCode + '"]'); // Find all cells with the same ID
        theCells.forEach(function (cell) { // Iterate over found cells
          cell.classList.remove('waitingColor'); // Remove waiting color class
          cell.classList.add('readyColor'); // Add ready color class
        });
      }
    }
  } else if (theCell.classList.contains('finishedColor')) { // If clicked cell is finished

    let cells = document.querySelectorAll('[id="' + targetId + '"]'); // Find all cells with the same ID
    cells.forEach(function (cell) { // Iterate over found cells
      cell.classList.remove('finishedColor'); // Remove finished color class
      cell.classList.add('readyColor'); // Add ready color class
    });

    // Loop to iterate through the unblock classes and reset them to waiting
    for (let index = 0; index < myHashMap[targetId].unblock.length; index++) { // Loop through unblock classes
      let classCode = myHashMap[targetId].unblock[index]; // Get unblock class code
      blockClassesR(classCode); // Call function to reset unblock classes
    }
  }
});
function blockClassesR(classID) {
  let checkCell = document.getElementById(classID); // Get the element with the specified classID
  if (checkCell.classList.contains('waitingColor')) { // Check if the class is already waiting
    return; // If so, exit the function
  } else {
    // make it gray, iterate through the unblock classes and check if those classes are gray
    let theCells = document.querySelectorAll('[id="' + classID + '"]'); // Find all elements with the specified classID
    theCells.forEach(function (cell) { // Loop through found elements
      cell.classList.remove('readyColor'); // Remove 'readyColor' class
      cell.classList.remove('finishedColor'); // Remove 'finishedColor' class
      cell.classList.add('waitingColor'); // Add 'waitingColor' class
    });
    // Loop though the unblock to block all dependent classes. 
    for (let index = 0; index < myHashMap[classID].unblock.length; index++) { // Loop through the unblock classes
      let dependentClass = myHashMap[classID].unblock[index]; // Get the current dependent class
      blockClassesR(dependentClass); // Recursively call blockClassesR for the dependent class
    }
  }
}