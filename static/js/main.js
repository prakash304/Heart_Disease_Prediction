// State for toggle buttons
const state = {
  male: '1',
  currentSmoker: '0',
  BPMeds: '0',
  prevalentStroke: '0',
  prevalentHyp: '0',
  diabetes: '0'
};

function setToggle(key, val, btn) {
  state[key] = val;
  const siblings = btn.closest('.toggle-group').querySelectorAll('.toggle');
  siblings.forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}

function getVal(id) {
  return parseFloat(document.getElementById(id).value) || 0;
}

function setGauge(percent) {
  const arc = document.getElementById('gaugeArc');
  const totalLen = 220;
  const filled = (percent / 100) * totalLen;
  arc.style.strokeDashoffset = totalLen - filled;

  if (percent < 10) arc.style.stroke = '#639922';
  else if (percent < 20) arc.style.stroke = '#BA7517';
  else arc.style.stroke = '#E24B4A';
}

async function predict() {
  const btn = document.getElementById('predictBtn');
  const btnText = document.getElementById('btn-text');
  const spinner = document.getElementById('btn-spinner');
  const placeholder = document.getElementById('resultPlaceholder');
  const content = document.getElementById('resultContent');

  btn.disabled = true;
  btnText.textContent = 'Analyzing...';
  spinner.style.display = 'block';

  const payload = {
    male: state.male,
    age: getVal('age'),
    education: getVal('education'),
    currentSmoker: state.currentSmoker,
    cigsPerDay: getVal('cigsPerDay'),
    BPMeds: state.BPMeds,
    prevalentStroke: state.prevalentStroke,
    prevalentHyp: state.prevalentHyp,
    diabetes: state.diabetes,
    totChol: getVal('totChol'),
    sysBP: getVal('sysBP'),
    diaBP: getVal('diaBP'),
    BMI: getVal('BMI'),
    heartRate: getVal('heartRate'),
    glucose: getVal('glucose')
  };

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error || 'Server error');
    }

    const data = await response.json();

    placeholder.style.display = 'none';
    content.style.display = 'block';

    // Update risk percent and label
    document.getElementById('riskPercent').textContent = data.probability.toFixed(1) + '%';
    document.getElementById('riskLabel').textContent = data.risk_level + ' risk';

    // Color theme
    document.body.classList.remove('risk-low', 'risk-moderate', 'risk-high');
    document.body.classList.add('risk-' + data.risk_level.toLowerCase());

    // Animate gauge
    setTimeout(() => setGauge(data.probability), 100);

    // Prediction summary
    const predMsg = data.prediction === 1
      ? `Based on this profile, the model predicts a <strong style="color:#E24B4A;">positive</strong> 10-year CHD risk (${data.probability.toFixed(1)}%).`
      : `Based on this profile, the model predicts a <strong style="color:#639922;">negative</strong> 10-year CHD risk (${data.probability.toFixed(1)}%).`;
    document.getElementById('resultPrediction').innerHTML = predMsg;

    // Risk and protective factors
    const riskDiv = document.getElementById('riskFlags');
    const protDiv = document.getElementById('protFlags');
    const section = document.getElementById('factorsSection');

    riskDiv.innerHTML = (data.risk_flags || [])
      .map(f => `<div class="chip chip-risk">${f}</div>`).join('');
    protDiv.innerHTML = (data.protective_flags || [])
      .map(f => `<div class="chip chip-ok">${f}</div>`).join('');

    if ((data.risk_flags || []).length || (data.protective_flags || []).length) {
      section.style.display = 'grid';
    }

  } catch (err) {
    placeholder.style.display = 'flex';
    content.style.display = 'none';
    placeholder.innerHTML = `<p style="color:#E24B4A;font-size:13px;">Error: ${err.message}</p>`;
  } finally {
    btn.disabled = false;
    btnText.textContent = 'Predict 10-Year CHD Risk';
    spinner.style.display = 'none';
  }
}
