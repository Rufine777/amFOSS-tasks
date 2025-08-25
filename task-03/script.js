const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let drawing = false;
let points = [];
let centerX = canvas.width / 2;
let centerY = canvas.height / 2;

// Draw center dot
function drawCenterDot() {
    ctx.fillStyle = 'red';
    ctx.beginPath();
    ctx.arc(centerX, centerY, 5, 0, Math.PI * 2);
    ctx.fill();
}

// Score calculation
function calculateScore() {
    if (points.length < 5) return 0;
    let totalDist = 0;
    let count = 0;
    points.forEach(p => {
        let dx = p.x - centerX;
        let dy = p.y - centerY;
        let dist = Math.sqrt(dx * dx + dy * dy);
        totalDist += dist;
        count++;
    });
    let avgDist = totalDist / count;
    let variance = 0;
    points.forEach(p => {
        let dx = p.x - centerX;
        let dy = p.y - centerY;
        let dist = Math.sqrt(dx * dx + dy * dy);
        variance += Math.abs(dist - avgDist);
    });
    variance /= count;
    let score = Math.max(0, 100 - variance);
    return Math.round(score);
}

// Save and display scores
function updateScores(score) {
    let scores = JSON.parse(sessionStorage.getItem('scores')) || [];
    scores.unshift(score);
    if (scores.length > 5) scores.pop();
    sessionStorage.setItem('scores', JSON.stringify(scores));
    document.getElementById('scores').innerHTML = scores.join('%<br>') + '%';
}

function startDrawingGame() {
    document.getElementById('start-btn').style.display = 'none';
    document.getElementById('start-sound').play();
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawCenterDot();
    points = [];
    drawing = false;

    canvas.onmousedown = (e) => {
        drawing = true;
        points = [];
        ctx.beginPath();
        ctx.moveTo(e.clientX, e.clientY);
    };
    canvas.onmousemove = (e) => {
        if (drawing) {
            ctx.lineTo(e.clientX, e.clientY);
            ctx.strokeStyle = 'white';
            ctx.lineWidth = 2;
            ctx.stroke();
            points.push({ x: e.clientX, y: e.clientY });
        }
    };
    canvas.onmouseup = () => {
        drawing = false;
        let score = calculateScore();
        updateScores(score);
        document.getElementById('end-sound').play();
        document.getElementById('start-btn').style.display = 'block';
    };
}

drawCenterDot();
updateScores(0);

document.getElementById('start-btn').addEventListener('click', startDrawingGame);

window.onresize = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    centerX = canvas.width / 2;
    centerY = canvas.height / 2;
    drawCenterDot();
};
