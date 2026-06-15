// State variables
let students = [];
let currentSort = { field: '', reverse: false };
let studentToDelete = null;
let currentTab = 'records'; // 'records' or 'analytics'

// Initial Load
document.addEventListener("DOMContentLoaded", () => {
    fetchStudents();
    fetchStats();
});

// Tab Switching
function switchTab(tab) {
    if (currentTab === tab) return;
    currentTab = tab;

    // Toggle active state on buttons
    document.getElementById('tab-records').classList.toggle('active', tab === 'records');
    document.getElementById('tab-analytics').classList.toggle('active', tab === 'analytics');

    // Toggle visible state on view panels
    document.getElementById('records-view').classList.toggle('hidden', tab !== 'records');
    document.getElementById('analytics-view').classList.toggle('hidden', tab !== 'analytics');

    // Show/hide search bar in header (it's only used for filtering records)
    document.getElementById('header-search-wrapper').classList.toggle('hidden', tab !== 'records');

    if (tab === 'analytics') {
        fetchStats(); // Refresh stats/charts
    } else {
        fetchStudents(); // Refresh records list
    }
}

// Toast System
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let iconClass = 'fa-circle-info';
    if (type === 'success') iconClass = 'fa-circle-check';
    if (type === 'error') iconClass = 'fa-circle-xmark';
    
    toast.innerHTML = `
        <i class="fa-solid ${iconClass}"></i>
        <span>${message}</span>
    `;
    
    container.appendChild(toast);
    
    // Auto-remove after 4 seconds
    setTimeout(() => {
        toast.style.animation = 'toastSlideIn 0.3s cubic-bezier(0.68, -0.55, 0.27, 1.55) reverse';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Fetch Students from API
async function fetchStudents() {
    let url = '/api/students';
    const params = [];
    if (currentSort.field) {
        params.push(`sort=${currentSort.field}`);
        params.push(`reverse=${currentSort.reverse}`);
    }
    if (params.length > 0) {
        url += `?${params.join('&')}`;
    }

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error("Failed to fetch students");
        students = await response.json();
        renderStudentsTable(students);
    } catch (err) {
        console.error(err);
        showToast("Error retrieving student records.", "error");
    }
}

// Fetch Stats and Render Analytics
async function fetchStats() {
    try {
        const response = await fetch('/api/stats');
        if (!response.ok) throw new Error("Failed to fetch stats");
        const stats = await response.json();
        
        // Update general dashboard counts
        document.getElementById('stat-total').innerText = stats.total_students;
        document.getElementById('stat-average').innerText = stats.average_marks.toFixed(1);
        const courseCount = Object.keys(stats.course_distribution).length;
        document.getElementById('stat-courses').innerText = courseCount;
        
        // Render detailed analytics dashboard views
        renderAnalyticsView(stats);
    } catch (err) {
        console.error(err);
    }
}

// Render Analytics Layout
function renderAnalyticsView(stats) {
    const total = stats.total_students;
    
    // Summary Cards
    document.getElementById('analytics-total').innerText = total;
    document.getElementById('analytics-average').innerText = stats.average_marks.toFixed(1);
    
    let passRate = 0.0;
    if (total > 0 && stats.pass_fail_distribution) {
        const passed = stats.pass_fail_distribution.Pass || 0;
        passRate = (passed / total) * 100;
    }
    document.getElementById('analytics-pass-rate').innerText = `${passRate.toFixed(1)}%`;

    // Grade Distribution HTML Chart
    const gradeContainer = document.getElementById('grade-chart-container');
    gradeContainer.innerHTML = '';
    
    if (total === 0) {
        gradeContainer.innerHTML = '<div class="empty-state"><p>No grade records to analyze.</p></div>';
    } else {
        const maxCount = Math.max(...Object.values(stats.grade_distribution), 1);
        Object.entries(stats.grade_distribution).forEach(([grade, count]) => {
            const widthPct = (count / maxCount) * 100;
            const row = document.createElement('div');
            row.className = 'chart-bar-row';
            row.innerHTML = `
                <span class="chart-bar-label">${grade}</span>
                <div class="chart-bar-track">
                    <div class="chart-bar-fill fill-${grade.toLowerCase()}" style="width: ${widthPct}%"></div>
                </div>
                <span class="chart-bar-value">${count} (${Math.round((count / total) * 100)}%)</span>
            `;
            gradeContainer.appendChild(row);
        });
    }

    // Pass vs Fail Progress Fill
    const passCount = stats.pass_fail_distribution ? (stats.pass_fail_distribution.Pass || 0) : 0;
    const failCount = stats.pass_fail_distribution ? (stats.pass_fail_distribution.Fail || 0) : 0;
    
    document.getElementById('pass-count').innerText = passCount;
    document.getElementById('fail-count').innerText = failCount;
    
    const passPct = total > 0 ? (passCount / total) * 100 : 0.0;
    const failPct = total > 0 ? (failCount / total) * 100 : 0.0;
    
    document.getElementById('pass-bar-fill').style.width = `${passPct}%`;
    document.getElementById('fail-bar-fill').style.width = `${failPct}%`;
    document.getElementById('pass-percentage').innerText = `${Math.round(passPct)}%`;

    // Course Performance Breakdown Table
    const courseBody = document.getElementById('course-analytics-tbody');
    courseBody.innerHTML = '';
    
    if (total === 0 || !stats.course_details || stats.course_details.length === 0) {
        courseBody.innerHTML = '<tr><td colspan="5" class="text-center" style="text-align: center; color: var(--text-secondary);">No course records available.</td></tr>';
    } else {
        stats.course_details.forEach(course => {
            const tr = document.createElement('tr');
            
            // Color tag for course pass percentage status
            let rateClass = 'text-green';
            if (course.pass_rate < 50.0) rateClass = 'text-red';
            
            tr.innerHTML = `
                <td><strong>${course.course_name}</strong></td>
                <td>${course.student_count}</td>
                <td>${course.average_marks.toFixed(1)}</td>
                <td>${course.pass_count}</td>
                <td><span class="${rateClass} font-bold">${course.pass_rate.toFixed(1)}%</span></td>
            `;
            courseBody.appendChild(tr);
        });
    }
}

// Render Table Rows
function renderStudentsTable(data) {
    const tbody = document.getElementById('students-tbody');
    const msg = document.getElementById('no-records-msg');
    tbody.innerHTML = '';
    
    if (data.length === 0) {
        msg.classList.remove('hidden');
        return;
    } else {
        msg.classList.add('hidden');
    }
    
    data.forEach(s => {
        // Marks Badge Styling
        let badgeClass = 'marks-mid';
        if (s.marks >= 80) badgeClass = 'marks-high';
        else if (s.marks < 40) badgeClass = 'marks-low';
        
        // Truncate description for neat rendering
        const desc = s.description.length > 25 ? `${s.description.substring(0, 22)}...` : s.description;

        const tr = document.createElement('tr');
        tr.id = `row-${s.student_id}`;
        tr.innerHTML = `
            <td><strong>${s.student_id}</strong></td>
            <td>${s.name}</td>
            <td>${s.age}</td>
            <td>${s.gender}</td>
            <td>${s.course}</td>
            <td><span class="marks-badge ${badgeClass}">${s.marks.toFixed(1)}</span></td>
            <td><span class="grade-badge font-bold">${s.grade}</span></td>
            <td><span class="status-badge ${s.status.toLowerCase()}">${s.status}</span></td>
            <td>${s.email}</td>
            <td title="${s.description}">${desc}</td>
            <td class="actions-col">
                <div class="actions-cell">
                    <button class="btn-icon edit" onclick="openEditModal('${s.student_id}')" title="Edit Student">
                        <i class="fa-solid fa-pen"></i>
                    </button>
                    <button class="btn-icon delete" onclick="openDeleteModal('${s.student_id}', '${s.name.replace(/'/g, "\\'")}')" title="Delete Student">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Real-time client-side search filtering
function filterStudents() {
    const query = document.getElementById('search-input').value.toLowerCase().trim();
    if (!query) {
        renderStudentsTable(students);
        return;
    }
    
    const filtered = students.filter(s => 
        s.student_id.toLowerCase().includes(query) || 
        s.name.toLowerCase().includes(query) ||
        s.course.toLowerCase().includes(query) ||
        s.email.toLowerCase().includes(query) ||
        s.description.toLowerCase().includes(query)
    );
    renderStudentsTable(filtered);
}

// Sort Action Toggler
function toggleSort(field) {
    if (currentSort.field === field) {
        currentSort.reverse = !currentSort.reverse;
    } else {
        currentSort.field = field;
        currentSort.reverse = field === 'marks'; // default descending for marks, ascending for name
    }
    
    // Update sort button active states
    document.getElementById('sort-name-btn').classList.toggle('active', field === 'name');
    document.getElementById('sort-marks-btn').classList.toggle('active', field === 'marks');
    
    // Update icon directions
    const nameIcon = document.querySelector('#sort-name-btn i');
    const marksIcon = document.querySelector('#sort-marks-btn i');
    
    if (field === 'name') {
        nameIcon.className = currentSort.reverse ? "fa-solid fa-sort-down" : "fa-solid fa-sort-up";
        marksIcon.className = "fa-solid fa-sort";
    } else {
        marksIcon.className = currentSort.reverse ? "fa-solid fa-sort-down" : "fa-solid fa-sort-up";
        nameIcon.className = "fa-solid fa-sort";
    }
    
    fetchStudents();
}

// Modal functions
function openAddModal() {
    resetForm();
    document.getElementById('modal-title').innerText = "Add Student";
    document.getElementById('form-action').value = "add";
    document.getElementById('student_id').disabled = false;
    document.getElementById('student-modal').classList.remove('hidden');
}

function openEditModal(studentId) {
    resetForm();
    const student = students.find(s => s.student_id === studentId);
    if (!student) return;
    
    document.getElementById('modal-title').innerText = "Edit Student Details";
    document.getElementById('form-action').value = "edit";
    
    // Populate form
    document.getElementById('student_id').value = student.student_id;
    document.getElementById('student_id').disabled = true; // Cannot edit ID
    document.getElementById('name').value = student.name;
    document.getElementById('age').value = student.age;
    document.getElementById('gender').value = student.gender;
    document.getElementById('course').value = student.course;
    document.getElementById('marks').value = student.marks;
    document.getElementById('email').value = student.email;
    document.getElementById('description').value = student.description;
    
    document.getElementById('student-modal').classList.remove('hidden');
}

function closeStudentModal() {
    document.getElementById('student-modal').classList.add('hidden');
}

function resetForm() {
    document.getElementById('student-form').reset();
    clearErrors();
}

function clearErrors() {
    const errorElements = document.querySelectorAll('.error-msg');
    errorElements.forEach(el => el.innerText = '');
    
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => input.style.borderColor = '');
}

// Form validations on client-side
function validateForm() {
    clearErrors();
    let isValid = true;
    
    const studentId = document.getElementById('student_id').value.trim();
    const name = document.getElementById('name').value.trim();
    const age = parseInt(document.getElementById('age').value);
    const gender = document.getElementById('gender').value;
    const course = document.getElementById('course').value.trim();
    const marks = parseFloat(document.getElementById('marks').value);
    const email = document.getElementById('email').value.trim();
    const description = document.getElementById('description').value.trim();
    
    if (!studentId) {
        showFieldError('student_id', "Student ID is required.");
        isValid = false;
    }
    
    if (!name) {
        showFieldError('name', "Name is required.");
        isValid = false;
    }
    
    if (isNaN(age) || age <= 0) {
        showFieldError('age', "Age must be greater than 0.");
        isValid = false;
    }
    
    if (!gender) {
        showFieldError('gender', "Gender selection is required.");
        isValid = false;
    }
    
    if (!course) {
        showFieldError('course', "Course is required.");
        isValid = false;
    }
    
    if (isNaN(marks) || marks < 0 || marks > 100) {
        showFieldError('marks', "Marks must be between 0 and 100.");
        isValid = false;
    }
    
    // Basic email validation regex
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!email || !emailRegex.test(email)) {
        showFieldError('email', "Invalid email format.");
        isValid = false;
    }

    if (!description) {
        showFieldError('description', "Description cannot be empty.");
        isValid = false;
    } else if (description.length > 200) {
        showFieldError('description', "Description cannot exceed 200 characters.");
        isValid = false;
    }
    
    return isValid;
}

function showFieldError(fieldId, message) {
    const errorEl = document.getElementById(`err-${fieldId}`);
    if (errorEl) errorEl.innerText = message;
    
    const inputEl = document.getElementById(fieldId);
    if (inputEl) inputEl.style.borderColor = 'var(--accent-red)';
}

// Save Student (Insert/Update)
async function saveStudent(event) {
    event.preventDefault();
    if (!validateForm()) return;
    
    const action = document.getElementById('form-action').value;
    const studentId = document.getElementById('student_id').value.trim();
    
    const payload = {
        student_id: studentId,
        name: document.getElementById('name').value.trim(),
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        course: document.getElementById('course').value.trim(),
        marks: parseFloat(document.getElementById('marks').value),
        email: document.getElementById('email').value.trim(),
        description: document.getElementById('description').value.trim()
    };
    
    let url = '/api/students';
    let method = 'POST';
    
    if (action === 'edit') {
        url = `/api/students/${encodeURIComponent(studentId)}`;
        method = 'PUT';
    }
    
    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            // Check if backend returned a validation error
            if (data.error) {
                if (data.error.includes("ID") || data.error.includes("exists")) {
                    showFieldError('student_id', data.error);
                } else if (data.error.includes("email") || data.error.includes("Email")) {
                    showFieldError('email', data.error);
                } else {
                    showToast(data.error, "error");
                }
            } else {
                throw new Error("Server error during save");
            }
            return;
        }
        
        showToast(
            action === 'add' ? "Student record added successfully!" : "Student details updated successfully!", 
            "success"
        );
        closeStudentModal();
        fetchStudents();
        fetchStats();
        
    } catch (err) {
        console.error(err);
        showToast("An unexpected error occurred while saving.", "error");
    }
}

// Delete Dialog
function openDeleteModal(studentId, studentName) {
    studentToDelete = studentId;
    document.getElementById('delete-student-name').innerText = studentName;
    document.getElementById('delete-student-id').innerText = studentId;
    document.getElementById('delete-modal').classList.remove('hidden');
}

// Close Delete Modal
function closeDeleteModal() {
    document.getElementById('delete-modal').classList.add('hidden');
    studentToDelete = null;
}

// Confirm Delete
async function confirmDelete() {
    if (!studentToDelete) return;
    
    try {
        const response = await fetch(`/api/students/${encodeURIComponent(studentToDelete)}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Failed to delete student");
        }
        
        showToast("Student record deleted successfully.", "success");
        closeDeleteModal();
        fetchStudents();
        fetchStats();
    } catch (err) {
        console.error(err);
        showToast(err.message || "Error deleting student.", "error");
    }
}
