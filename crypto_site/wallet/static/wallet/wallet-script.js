window.onload = () => {
  const $ = (id) => document.getElementById(id);
  const operationInput = $("operation");

  Array.from(document.querySelectorAll('.trade-btn')).forEach(btn => {
    btn.onclick = () => {
      document.querySelectorAll('.trade-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.trade-panel').forEach(p => p.classList.remove('active'));
      btn.classList.add('active');
      $(btn.dataset.target).classList.add('active');
      operationInput.value = btn.dataset.target;
    };
  });

  function loadTradingView(symbol = "BTCUSDT") {
    new TradingView.widget({
      container_id: "tradingview-widget",
      autosize: true,
      symbol: `BINANCE:${symbol}`,
      interval: "1",
      timezone: "Etc/UTC",
      theme: "dark",
      style: "1",
      locale: "en",
      enable_publishing: false,
      hide_top_toolbar: true,
      allow_symbol_change: true,
      details: true,
      withdateranges: true,
      studies: ["MACD@tv-basicstudies"],
    });
  }

  function setupAmountCheck(inputId, buttonId) {
    const input = $(inputId);
    const button = $(buttonId);
    const check = () => {
      const value = parseFloat(input.value);
      if (!value || value <= 0) {
        button.disabled = true;
        button.style.opacity = "0.5"; 
        button.style.cursor = "not-allowed";
      } else {
        button.disabled = false;
        button.style.opacity = "1";
        button.style.cursor = "pointer";
      }
    };
    input.addEventListener("input", check);
    check();
  }

  setupAmountCheck("buy-amount", "buy-btn");
  setupAmountCheck("sell-amount", "sell-btn");
  setupAmountCheck("convert-amount", "convert-btn");
  setupAmountCheck("send-amount", "send-btn");

  document.querySelector(".send-form").addEventListener("submit", (e) => {
  const email = document.getElementById("send-email").value;
  const crypto = document.getElementById("send-crypto").value;
  const amount = document.getElementById("send-amount").value;

  if (!confirm(`გგსურს ${amount} ${crypto} გადაუგზავნო ${email}?`)) {
    e.preventDefault();
  }
});


  loadTradingView();
};
