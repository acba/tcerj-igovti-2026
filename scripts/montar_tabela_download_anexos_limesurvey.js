// A ser executado na página de listagem das respostas do survey
// Ex:
// https://www.tcerj.tc.br/limesurvey-novo/index.php/admin/responses/sa/browse/surveyid/796352

(async function () {
  // 0. Carrega biblioteca para gerar XLSX
  if (!window.XLSX) {
    await new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src =
        "https://cdn.sheetjs.com/xlsx-0.20.3/package/dist/xlsx.full.min.js";
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  // 1. Seleciona a tabela
  const table = document.querySelector("table.table-striped.table");

  if (!table) {
    console.error("Tabela não encontrada.");
    return;
  }

  // Descobre automaticamente o surveyid
  const surveyId =
    new URLSearchParams(location.search).get("surveyid") ||
    location.pathname.match(/surveyid\/(\d+)/)?.[1] ||
    table.querySelector('a[href*="surveyid/"]')
      ?.href.match(/surveyid\/(\d+)/)?.[1] ||
    "desconhecido";

  // 2. Extrai cabeçalhos
  const headers = Array.from(
    table.querySelectorAll(":scope > thead > tr > th")
  ).map(th => th.innerText.trim());

  const idIdx = headers.findIndex(h =>
    h.toLowerCase() === "id" ||
    h.toLowerCase().includes("id da resposta")
  );

  const fnIdx = headers.findIndex(h =>
    h.toLowerCase().includes("first name")
  );

  const dateIdx = headers.findIndex(h =>
    h.toLowerCase().includes("last action")
  );

  const completeIdx = headers.findIndex(h =>
    h.toLowerCase().includes("completed")
  );

  // 3. Processa apenas os TR do TBODY externo
  const rows = Array.from(
    table.querySelectorAll(":scope > tbody > tr")
  );

  const dados = rows
    .map(row => {
      const cells = row.cells;

      if (cells.length < 2) {
        return null;
      }

      const id =
        idIdx !== -1 && cells[idIdx]
          ? cells[idIdx].innerText.trim()
          : "";

      if (!id) {
        return null;
      }

      const firstname =
        fnIdx !== -1 && cells[fnIdx]
          ? cells[fnIdx].innerText.trim()
          : "N/A";

      const date =
        dateIdx !== -1 && cells[dateIdx]
          ? cells[dateIdx].innerText.trim()
          : "N/A";

      const completed =
        completeIdx !== -1 &&
        cells[completeIdx]?.querySelector("span.fa-check")
          ? "sim"
          : "nao";

      // Botão de download dos anexos
      const downloadButton = row.querySelector(
        'a[href*="/actionDownloadfiles/"]'
      );

      // Botão do PDF das respostas
      const pdfButton = row.querySelector(
        'a[href*="/viewquexmlpdf/"]'
      );

      return {
        id,
        orgao: firstname,
        datestamp: date,
        completed,
        url: (!downloadButton) ? "" : downloadButton.href,
        url_pdf_respostas: pdfButton ? pdfButton.href : ""
      };
    })
    .filter(Boolean);

  // 4. Gera XLSX
  const worksheet = XLSX.utils.json_to_sheet(dados);

  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "respostas");

  XLSX.writeFile(
    workbook,
    `relacao_respostas_${surveyId}.xlsx`
  );

  console.log(
    `✅ Planilha gerada com ${dados.length} respostas que possuem anexos.`
  );
})();