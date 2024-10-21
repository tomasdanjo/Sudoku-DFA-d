function validate_all_inputs() {
    // get all input elements
    clear_highlights();
    const inputs = document.querySelectorAll('input[type="text"]');
    inputs.forEach((input) => {
        validate_input(input);
    });
}

function clear_highlights() {
    document.querySelectorAll('td').forEach(td => {
        // Remove classes from the <td>
        td.classList.remove('bg-red-200', 'row-highlight', 'col-highlight', 'region-highlight');

        // Also select the input element inside the <td> and remove highlight classes
        const input = td.querySelector('input');
        if (input) {
            input.classList.remove('bg-red-300', 'bg-red-400'); // Remove the highlight classes for inputs
        }
    });
}


function validate_input(input) {
    // Allow only digits 1-9
    input.value = input.value.replace(/[^1-9]/g, '');

    // Get the row and column indices from the input attributes
    const row = input.getAttribute('data-row');
    const col = input.getAttribute('data-col');
    console.log(`Row: ${row}, Column: ${col}, Value: ${input.value}`);


    // Row Validation

    row_val = get_row_values(row);
    col_val = get_col_values(col);
    region_val = get_region_values(row, col);

    // console.log(row_val.length);

    console.log("Row Val: " + (row_val));
    console.log("Col Val: " + (col_val));
    console.log("Region Val: " + (region_val));

    console.log("Row State: " + get_state(row_val));
    console.log("Col State: " + get_state(col_val));
    console.log("Region State: " + get_state(region_val));



    if (get_state(row_val) == 0) {
        highlight_row(row);
    }

    // Column Validation
    if (get_state(col_val) == 0) {
        highlight_column(col);
    }


    if (get_state(region_val) == 0) {
        highlight_region(row, col);
    }
}


function get_state(arr) {

    let i = 0, state = 10; // initial state
    seen = new Set(); // Initialize a Set to track seen values


    while (i < arr.length) {
        const input = arr[i]; // Get the current input
        if (input == 0) {
            i++;
            continue;
        }

        // state = table[state][input]; // This line is commented out
        if (seen.has(input)) {
            state = 0; // If input is already seen, set state to 0 (reject state)
        } else {
            seen.add(input); // If not seen, add to the Set
            state = input;
        }

        if (state == 0) break; // Exit loop if state is 0
        i++; // Move to the next input
    }
    return state; // Return the final state

}


function highlight_row(row) {
    // Select all <td> elements in the specified row
    const tds = document.querySelectorAll(`tr:nth-child(${parseInt(row) + 1}) td`);

    tds.forEach(td => {
        // Add classes to the <td>
        td.classList.add('bg-red-200', 'row-highlight');

        // Also select the input element inside the <td> and add classes to it
        const input = td.querySelector('input');
        if (input) {
            // Check if the input is readonly
            if (input.hasAttribute('readonly')) {
                input.classList.add('bg-red-300'); // Color for readonly inputs
            } else {
                input.classList.add('bg-red-400'); // Color for editable inputs
            }
        }
    });
}

function highlight_column(col) {
    document.querySelectorAll(`tr`).forEach(row => {
        const td = row.querySelectorAll('td')[parseInt(col)];
        td.classList.add('bg-red-200', 'col-highlight');

        const input = td.querySelector('input');
        if (input) {
            // Check if the input is readonly
            if (input.hasAttribute('readonly')) {
                input.classList.add('bg-red-300'); // Color for readonly inputs
            } else {
                input.classList.add('bg-red-400'); // Color for editable inputs
            }
        }
    });
}


function highlight_region(row, col) {
    const startRow = Math.floor(row / 3) * 3;
    const startCol = Math.floor(col / 3) * 3;

    for (let r = startRow; r < startRow + 3; r++) {
        for (let c = startCol; c < startCol + 3; c++) {
            const td = document.querySelector(`tr:nth-child(${r + 1})`).querySelectorAll('td')[c];
            td.classList.add('bg-red-200', 'region-highlight');

            const input = td.querySelector('input');
            if (input) {
                // Check if the input is readonly
                if (input.hasAttribute('readonly')) {
                    input.classList.add('bg-red-300'); // Color for readonly inputs
                } else {
                    input.classList.add('bg-red-400'); // Color for editable inputs
                }
            }
        }
    }
}




function get_row_values(row) {
    // Selects all <td> elements in the specified row
    const rowCells = document.querySelectorAll(`tr:nth-child(${parseInt(row) + 1}) td`);
    // console.log(rowCells);  // Log the row cells for debugging

    const rowValues = [];

    rowCells.forEach(td => {
        if (td.querySelector('input')) {
            rowValues.push(td.querySelector('input').value || '0');
        } else {
            rowValues.push(td.textContent);
        }
    });


    return rowValues;
}

function get_col_values(col) {
    const rows = document.querySelectorAll('tr'); // Select all rows
    const colValues = []; // Initialize an array to hold column values

    rows.forEach((row) => {
        const cell = row.querySelector(`td:nth-child(${parseInt(col) + 1})`); // Select the specific cell in the current row

        if (cell) {
            if (cell.querySelector('input')) {
                // If the cell contains an input, push its value to the array
                colValues.push(cell.querySelector('input').value || '0');
            } else {
                // Otherwise, push the text content of the cell
                colValues.push(cell.textContent);
            }
        }
    });


    return colValues; // Return the array of column values
}

function get_region_values(row, col) {
    // Calculate the top-left corner of the 3x3 region based on the current row and column
    const startRow = Math.floor(row / 3) * 3;
    const startCol = Math.floor(col / 3) * 3;

    const regionValues = [];

    // Loop through each cell in the 3x3 region
    for (let r = startRow; r < startRow + 3; r++) {
        for (let c = startCol; c < startCol + 3; c++) {
            const cell = document.querySelector(`tr:nth-child(${r + 1}) td:nth-child(${c + 1})`);

            if (cell) {
                if (cell.querySelector('input')) {
                    // If the cell has an input, get the value or '0' if empty
                    regionValues.push(cell.querySelector('input').value || '0');
                } else {
                    // Otherwise, get the text content of the cell
                    regionValues.push(cell.textContent);
                }
            }
        }
    }

    // console.log(regionValues); // For debugging purposes
    return regionValues; // Return the array of region values
}

document.addEventListener("DOMContentLoaded", function(){
    validate_all_inputs();
    console.log("JavaScript loaded and ready!");
});
