// Text to animate
const text = "Welcome to Highcharts Hub!";
const titleElement = document.getElementById("animated-title");

// Typing effect function
let index = 0;
function typeText() {
    if (index < text.length) {
        titleElement.textContent += text.charAt(index);
        index++;
        setTimeout(typeText, 100); // Adjust typing speed here
    }
}

// Start animation when the page loads
window.onload = typeText;
