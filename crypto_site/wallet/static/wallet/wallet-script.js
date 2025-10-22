const $ = (id) => document.getElementById(id);


Array.from(document.querySelectorAll('.trade-btn')).forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll('.trade-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.trade-panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    $(btn.dataset.target).classList.add('active');
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

window.onload = () => {
  loadTradingView(); 
};