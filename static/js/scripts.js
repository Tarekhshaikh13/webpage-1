
function refreshPage() {
    location.reload();
}

document.addEventListener("DOMContentLoaded", function() {
    // Get all input and textarea elements
    const inputs = document.querySelectorAll('input, textarea');
    
    inputs.forEach(input => {
        // Add input event listener
        input.addEventListener('input', function() {
            if (input.validity.valid) {
                input.style.borderColor = "lightblue";
            } else {
                input.style.borderColor = "red";
            }
        });
    });
});



async function handleFormSubmit(event) {
    event.preventDefault();
    let formData = new FormData(event.target);

    try {
        let response = await fetch('/', {
            method: 'POST',
            body: formData
        });

        // Assuming a successful submission will return a 200 status
        if (response.status === 200) {
            lockFormData();
            document.getElementById("messageDisplay").innerText = "Form submitted successfully!";
        } else {
            document.getElementById("messageDisplay").innerText = "Error submitting the form.";
        }
    } catch (error) {
        console.error("There was an error sending the form.", error);
        document.getElementById("messageDisplay").innerText = "Error submitting the form.";
    }
}

function lockFormData() {
    const formElements = document.querySelectorAll('input, textarea');
    formElements.forEach(element => {
        if (element.getAttribute('type') !== 'submit') {
            element.setAttribute('readonly', true);
        }
    });
    const saveButton = document.getElementById("saveBtn");
    saveButton.disabled = true; 
    saveButton.style.backgroundColor = "#e0e0e0"; // Light gray background
    saveButton.style.color = "#333";

    nxtButton = document.getElementById("nxtBtn");
}




