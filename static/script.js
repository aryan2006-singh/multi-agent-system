const messagesEl = document.getElementById("messages");
const formEl = document.getElementById("chat-form");
const inputEl = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");
const statusPill = document.getElementById("status-pill");

function addMessage(text, role, agentsUsed) {
  const bubble = document.createElement("div");
  bubble.className = `msg ${role}`;
  bubble.textContent = text;

  if (agentsUsed && agentsUsed.length) {
    const tag = document.createElement("span");
    tag.className = "agents-tag";
    tag.textContent = `handled by: ${agentsUsed.join(", ")}`;
    bubble.appendChild(tag);
  }

  messagesEl.appendChild(bubble);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function checkHealth() {
  try {
    const res = await fetch("/api/health");
    const data = await res.json();
    if (data.llm_configured) {
      statusPill.textContent = "online";
      statusPill.className = "status-pill ok";
    } else {
      statusPill.textContent = "no API key set";
      statusPill.className = "status-pill bad";
    }
  } catch (err) {
    statusPill.textContent = "offline";
    statusPill.className = "status-pill bad";
  }
}

async function sendMessage(message) {
  addMessage(message, "user");
  inputEl.value = "";
  sendBtn.disabled = true;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    if (!res.ok) {
      throw new Error(`Server returned ${res.status}`);
    }
    const data = await res.json();
    addMessage(data.reply, "bot", data.agents_used);
  } catch (err) {
    addMessage("Couldn't reach the server. Please try again.", "bot");
  } finally {
    sendBtn.disabled = false;
    inputEl.focus();
  }
}

formEl.addEventListener("submit", (event) => {
  event.preventDefault();
  const message = inputEl.value.trim();
  if (message) {
    sendMessage(message);
  }
});

checkHealth();
addMessage(
  "Hi! Ask me about billing, technical issues, products, or anything else.",
  "bot"
);
