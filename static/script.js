const words = ["RED", "BLUE", "GREEN", "YELLOW"];
const colors = ["red", "blue", "green", "yellow"];

let startTime;
let currentWord, currentColor;
const maxTrials = 20; 

// Reset trialCount when the test starts
if (!sessionStorage.getItem("trialCount") || sessionStorage.getItem("trialCount") >= maxTrials) {
    sessionStorage.setItem("trialCount", 0);
}

let trialCount = parseInt(sessionStorage.getItem("trialCount"));

//Occurs in every trial
function nextTrial() {
    if (trialCount >= maxTrials) {
        showCompletionMessage();
        return;
    }

    //Setting random words and colours
    currentWord = words[Math.floor(Math.random() * words.length)];
    currentColor = colors[Math.floor(Math.random() * colors.length)];
    document.getElementById("word").innerText = currentWord;
    document.getElementById("word").style.color = currentColor;
    startTime = Date.now();
}

function handleResponse(userResponse) {
    if (trialCount >= maxTrials) {
        showCompletionMessage();
        return;
    }

    let reactionTime = Date.now() - startTime;

    //Submitting data to database
    fetch("/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            word: currentWord,
            color: currentColor,
            response: userResponse,
            reaction_time: reactionTime,
            is_correct: userResponse === currentColor    
        })
    }).then(response => response.json())
      .catch(error => console.error("Error:", error));

    trialCount++;
    sessionStorage.setItem("trialCount", trialCount);

    if (trialCount < maxTrials) {
        nextTrial();
    } else {
        showCompletionMessage();
    }
}

//When 20 trials are completed
function showCompletionMessage() {
    document.getElementById("word").style.display = "none";
    document.getElementById("buttons").style.display = "none";

    const completionMessage = document.createElement("h2");
    completionMessage.innerText = "Test completed! Thank you.";
    document.body.appendChild(completionMessage);
}

window.onload = nextTrial;



