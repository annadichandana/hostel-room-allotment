function showSection(sectionId) {
    const sections = document.querySelectorAll('main section');
    sections.forEach(sec => {
        sec.classList.add('hidden');
    });
    document.getElementById(sectionId).classList.remove('hidden');
}

// Optional: Prevent form reload
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('studentForm');
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        alert("Student added successfully!");
        form.reset();
    });
});
function lick(){
    window.location.href = "/dashboard/";  
}

