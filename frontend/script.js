// const API_URL = "http://35.185.125.85:5000/employee/";

const API_URL = "http://192.168.49.2:31660/employee/";

// Fetch employee data and populate the table
async function fetchEmployees() {
  try {
    const response = await fetch(API_URL);
    
    // Check if the response is okay
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const employees = await response.json();
    const tableBody = document.getElementById("employee-table-body");
    tableBody.innerHTML = "";

    employees.forEach(employee => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${employee.emp_id}</td>
        <td>${employee.emp_name}</td>
        <td>${employee.position}</td>
        <td>${employee.department}</td>
        <td>${employee.email}</td>
        <td>
          <button class="btn btn-warning" onclick="editEmployee(${employee.emp_id})">Edit</button>
          <button class="btn btn-danger" onclick="deleteEmployee(${employee.emp_id})">Delete</button>
        </td>
      `;
      tableBody.appendChild(row);
    });
  } catch (error) {
    console.error("Error fetching employees:", error);
    alert(`Failed to fetch employees: ${error.message}`);
  }
}

// Edit Employee Function
async function editEmployee(empId) {
  try {
    const response = await fetch(`${API_URL}${empId}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const employee = await response.json();
    
    // Populate form with employee data
    document.getElementById("emp-id").value = employee.emp_id;
    document.getElementById("emp-name-input").value = employee.emp_name;
    document.getElementById("position-input").value = employee.position;
    document.getElementById("department-input").value = employee.department;
    document.getElementById("email-input").value = employee.email;

    // Toggle form visibility
    document.getElementById("edit-form").classList.remove("hidden");
    document.getElementById("employee-details").classList.add("hidden");
  } catch (error) {
    console.error("Error fetching employee for editing:", error);
    alert(`Failed to fetch employee for editing: ${error.message}`);
  }
}

// Delete Employee Function
async function deleteEmployee(empId) {
  if (confirm("Are you sure you want to delete this employee?")) {
    try {
      const response = await fetch(`${API_URL}${empId}`, { 
        method: "DELETE" 
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      alert("Employee deleted successfully!");
      fetchEmployees();
    } catch (error) {
      console.error("Error deleting employee:", error);
      alert(`Failed to delete employee: ${error.message}`);
    }
  }
}

// Handle form submission for saving/updating employee
document.getElementById("employee-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  // Collect form data
  const empId = document.getElementById("emp-id").value;
  const empName = document.getElementById("emp-name-input").value;
  const position = document.getElementById("position-input").value;
  const department = document.getElementById("department-input").value;
  const email = document.getElementById("email-input").value;

  // Prepare employee data object
  const employeeData = { 
    emp_name: empName, 
    position: position, 
    department: department, 
    email: email 
  };

  try {
    let response;
    if (empId) {
      // Update existing employee
      response = await fetch(`${API_URL}${empId}`, {
        method: "PUT",
        headers: { 
          "Content-Type": "application/json" 
        },
        body: JSON.stringify(employeeData),
      });
    } else {
      // Add new employee
      response = await fetch(API_URL, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json" 
        },
        body: JSON.stringify(employeeData),
      });
    }

    // Check response status
    if (!response.ok) {
      const errorBody = await response.text();
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorBody}`);
    }

    alert("Employee saved successfully!");
    fetchEmployees();
    
    // Reset and hide form
    document.getElementById("employee-form").reset();
    document.getElementById("edit-form").classList.add("hidden");
    document.getElementById("employee-details").classList.remove("hidden");
  } catch (error) {
    console.error("Error saving employee:", error);
    alert(`Failed to save employee: ${error.message}`);
  }
});

// Add Employee Button Handler
document.getElementById("add-btn").addEventListener("click", () => {
  document.getElementById("edit-form").classList.remove("hidden");
  document.getElementById("employee-details").classList.add("hidden");
  document.getElementById("employee-form").reset();
  document.getElementById("emp-id").value = "";
});

// Cancel Edit Button Handler
document.getElementById("cancel-edit-btn").addEventListener("click", () => {
  document.getElementById("edit-form").classList.add("hidden");
  document.getElementById("employee-details").classList.remove("hidden");
});

// Load employees when the page is loaded
document.addEventListener("DOMContentLoaded", fetchEmployees);