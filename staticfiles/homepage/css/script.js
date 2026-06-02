// Homepage Interactive Scripts
document.addEventListener("DOMContentLoaded", function() {
    console.log("ShopNova Homepage Loaded Successfully.");
    
    // Add visual highlights to selected budget categories on click
    const checkboxes = document.querySelectorAll(".checkbox-label input");
    checkboxes.forEach(chk => {
        chk.addEventListener("change", function() {
            if (this.checked) {
                this.parentElement.style.color = "var(--accent-orange)";
            } else {
                this.parentElement.style.color = "#fff";
            }
        });
        // Initial state
        if (chk.checked) {
            chk.parentElement.style.color = "var(--accent-orange)";
        }
    });
});
