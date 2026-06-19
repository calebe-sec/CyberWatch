/* scripts.js — CyberWatch Dashboard */

async function carregarReports() {
    const loading = document.getElementById("loading");
    const empty   = document.getElementById("empty");
    const grid    = document.getElementById("reports");

    try {
        const response = await fetch("/reports");

        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const reports = await response.json();

        loading.classList.add("hidden");

        if (!reports || reports.length === 0) {
            empty.classList.remove("hidden");
            return;
        }

        reports.forEach(report => {
            const card = document.createElement("div");
            card.className = "report-card";

            const kb = (report.tamanho / 1024).toFixed(1);

            card.innerHTML = `
                <div class="card-name">${escapeHtml(report.name)}</div>
                <div class="card-meta">
                    <span>${escapeHtml(report.path ?? report.name)}</span>
                </div>
                <div class="card-meta" style="margin-top:4px">
                    <span class="card-badge">JSON</span>
                    <span>${kb} KB</span>
                </div>
                <button class="card-btn" onclick="abrirReport('${escapeHtml(report.path ?? report.name)}', '${escapeHtml(report.name)}')">
                    Ver relatório →
                </button>
            `;

            grid.appendChild(card);
        });

    } catch (err) {
        loading.textContent = `Erro ao carregar relatórios: ${err.message}`;
    }
}

async function abrirReport(filepath, nome) {
    const modal   = document.getElementById("modal");
    const title   = document.getElementById("modalTitle");
    const content = document.getElementById("modalContent");

    title.textContent   = nome;
    content.textContent = "Carregando…";
    modal.classList.remove("hidden");

    try {
        const response = await fetch(`/reports/${filepath}`);
        const data = await response.json();

        content.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        content.textContent = `Erro ao carregar: ${err.message}`;
    }
}

function fecharModal() {
    document.getElementById("modal").classList.add("hidden");
}

document.addEventListener("click", function (e) {
    const modal = document.getElementById("modal");
    if (e.target === modal) fecharModal();
});

document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") fecharModal();
});

function escapeHtml(str) {
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
}

carregarReports();