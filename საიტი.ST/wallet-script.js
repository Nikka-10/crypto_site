const $ = (id) => document.getElementById(id);
const createEl = (tag, text = '', cls = '') => {
  const el = document.createElement(tag);
  el.textContent = text;
  if (cls) el.className = cls;
  return el;
};

let cash = 1000;
let balances = {};
let prices = {};
let history = [];
const cryptos = ['BTC', 'ETH', 'BNB', 'SOL', 'ADA'];

const populateSelects = () => {
  ['buy-crypto', 'sell-crypto', 'convert-from', 'convert-to'].forEach(id => {
    const select = $(id);
    select.innerHTML = '';
    cryptos.forEach(c => {
      const option = document.createElement('option');
      option.value = c;
      option.textContent = c;
      select.appendChild(option);
    });
  });
};

const updateUI = () => {
  $('cash-balance').textContent = `$${cash.toFixed(2)}`;
  const ul = $('crypto-balances');
  ul.innerHTML = '';
  cryptos.forEach(c => {
    const li = createEl('li', `${c}: ${balances[c] || 0}`);
    ul.appendChild(li);
  });
};

const showToast = (msg) => {
  const toast = createEl('div', msg, 'toast');
  $('toast-container').appendChild(toast);
  setTimeout(() => toast.remove(), 3000);
};

const log = (msg) => {
  const li = createEl('li', msg);
  $('transaction-history').prepend(li);
};

const fetchPrices = async () => {
  try {
    const res = await axios.get('https://api.binance.com/api/v3/ticker/price');
    cryptos.forEach(c => {
      const item = res.data.find(p => p.symbol === c + 'USDT');
      if (item) prices[c] = parseFloat(item.price);
    });
  } catch (e) {
    showToast('ფასების განახლება ვერ მოხერხდა');
  }
};

const updateTradeInfo = () => {
  const buyC = $('buy-crypto').value;
  const buyAmt = parseFloat($('buy-amount').value) || 0;
  const buyCost = buyAmt * (prices[buyC] || 0);
  $('buy-info').textContent = `ჯამი: $${buyCost.toFixed(2)}`;
  $('buy-btn').disabled = buyCost > cash || buyAmt <= 0;

  const sellC = $('sell-crypto').value;
  const sellAmt = parseFloat($('sell-amount').value) || 0;
  const canSell = (balances[sellC] || 0) >= sellAmt;
  const sellVal = sellAmt * (prices[sellC] || 0);
  $('sell-info').textContent = `ჯამი: $${sellVal.toFixed(2)}`;
  $('sell-btn').disabled = !canSell || sellAmt <= 0;

  const from = $('convert-from').value;
  const to = $('convert-to').value;
  const convAmt = parseFloat($('convert-amount').value) || 0;
  const convVal = convAmt * (prices[from] || 0);
  const converted = convVal / (prices[to] || 1);
  const canConvert = (balances[from] || 0) >= convAmt && from !== to;
  $('convert-info').textContent = `მიიღებ: ${converted.toFixed(6)} ${to}`;
  $('convert-btn').disabled = !canConvert || convAmt <= 0;
};

$('buy-btn').onclick = () => {
  const c = $('buy-crypto').value;
  const a = parseFloat($('buy-amount').value);
  const cost = a * prices[c];
  if (cash >= cost) {
    cash -= cost;
    balances[c] = (balances[c] || 0) + a;
    log(`შეძენილი ${a} ${c} ფასად $${cost.toFixed(2)}`);
    updateUI(); showToast('შეძენა შესრულდა');
  }
};

$('sell-btn').onclick = () => {
  const c = $('sell-crypto').value;
  const a = parseFloat($('sell-amount').value);
  const val = a * prices[c];
  if ((balances[c] || 0) >= a) {
    balances[c] -= a;
    cash += val;
    log(`გაყიდული ${a} ${c} მიღებული $${val.toFixed(2)}`);
    updateUI(); showToast('გაყიდვა შესრულდა');
  }
};

$('convert-btn').onclick = () => {
  const from = $('convert-from').value;
  const to = $('convert-to').value;
  const a = parseFloat($('convert-amount').value);
  const val = a * prices[from];
  const newAmt = val / prices[to];
  if ((balances[from] || 0) >= a && from !== to) {
    balances[from] -= a;
    balances[to] = (balances[to] || 0) + newAmt;
    log(`გადაცვლილი ${a} ${from} → ${newAmt.toFixed(6)} ${to}`);
    updateUI(); showToast('კონვერტაცია შესრულდა');
  }
};

Array.from(document.querySelectorAll('.trade-btn')).forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll('.trade-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.trade-panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    $(btn.dataset.target).classList.add('active');
  };
});

$('deposit-btn').onclick = () => {
  const amt = parseFloat($('deposit-amount').value);
  if (amt > 0) {
    cash += amt;
    updateUI(); log(`დეპოზიტი $${amt.toFixed(2)}`); showToast('დეპოზიტი წარმატებით შესრულდა');
  }
};

$('withdraw-btn').onclick = () => {
  const amt = parseFloat($('withdraw-amount').value);
  if (amt > 0 && amt <= cash) {
    cash -= amt;
    updateUI(); log(`გამოტანა $${amt.toFixed(2)}`); showToast('გამოტანა შესრულდა');
  }
};

function loadTradingView() {
  new TradingView.widget({
    container_id: "tradingview-widget",
    autosize: true,
    symbol: "BINANCE:BTCUSDT",
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

window.onload = async () => {
  populateSelects();
  await fetchPrices();
  updateUI();
  updateTradeInfo();
  loadTradingView();
};

['buy-crypto', 'buy-amount', 'sell-crypto', 'sell-amount', 'convert-from', 'convert-to', 'convert-amount']
  .forEach(id => $(id).addEventListener('input', updateTradeInfo));