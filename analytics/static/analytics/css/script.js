// Analytics Page Animations
document.addEventListener("DOMContentLoaded", function() {
    // Animate the bar charts fill on load
    const fills = document.querySelectorAll(".chart-bar-fill");
    fills.forEach(fill => {
        const targetWidth = fill.getAttribute("data-width");
        setTimeout(() => {
            fill.style.width = targetWidth + "%";
        }, 150);
    });
});
