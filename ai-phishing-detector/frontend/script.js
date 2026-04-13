/* Comprehensive frontend logic for AI Phishing Detector */
const API_URL = '/api';

// utils ------------------------------------------------------------------
function $(id) { return document.getElementById(id); }
function createEl(tag, props = {}) { const el = document.createElement(tag); Object.assign(el, props); return el; }

// state
let settings = {
    autoSaveHistory: true,
    showConfidence: true,
    detailedBreakdown: false,
    notifyHighRisk: false,
    soundAlerts: false,
    exportFormat: 'pdf'
};
let historyData = [];
let batchData = [];

// initialization ---------------------------------------------------------
window.addEventListener('load', () => {
    loadSettings();
    loadHistory();
    initTabs();
    initCharCounters();
    initFormControls();
    checkBackendStatus();
});

// backend status indicator
async function checkBackendStatus() {
    try {
        const res = await fetch(`${API_URL}/health`);
        const dot = $('backend-status');
        if (res.ok) {
            dot.style.background = 'var(--success-color)';
        } else {
            dot.style.background = 'var(--danger-color)';
        }
    } catch (e) {
        $('backend-status').style.background = 'var(--danger-color)';
    }
}

// tabs
function initTabs() {
    const buttons = document.querySelectorAll('.nav-btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            showTab(btn.dataset.tab);
        });
    });
}
function showTab(name) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.toggle('active', tab.id === `${name}-tab`);
    });
}

// character counters
function initCharCounters() {
    const subj = $('email-subject');
    const body = $('email-body');
    subj.addEventListener('input', () => {
        $('subject-count').textContent = subj.value.length;
    });
    body.addEventListener('input', () => {
        $('body-count').textContent = body.value.length;
    });
}

// form controls
function initFormControls() {
    $('detector-form').addEventListener('submit', async e => {
        e.preventDefault();
        const subject = $('email-subject').value.trim();
        const body = $('email-body').value.trim();
        if (!subject || !body) return showError('Please fill in all fields');
        const start = Date.now();
        const mode = $('analysis-mode').value;
        const sender = $('sender-email').value.trim();
        const result = await analyzeEmail(subject, body);
        if (result) {
            result.analysis_time = ((Date.now() - start) / 1000).toFixed(2) + 's';
            result.sender = sender;
            result.mode = mode;
            saveToHistory(result);
        }
    });

    $('clear-form').addEventListener('click', () => {
        $('detector-form').reset();
        $('subject-count').textContent = '0';
        $('body-count').textContent = '0';
        $('result-section').classList.add('hidden');
        $('error-section').classList.add('hidden');
    });

    $('export-result').addEventListener('click', exportCurrentResult);
    $('share-result').addEventListener('click', shareCurrentResult);
}

async function analyzeEmail(subject, body) {
    const loadingDiv = $('loading');
    const resultSection = $('result-section');
    const errorSection = $('error-section');
    resultSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    loadingDiv.classList.remove('hidden');
    try {
        const res = await fetch(`${API_URL}/detect`, {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email_subject: subject, email_body: body})
        });
        const data = await res.json();
        if (res.ok) { displayResult(data); return data; }
        else showError(data.error || 'An error occurred');
    } catch (err) {
        showError(`Connection failed: ${err.message}`);
    } finally {
        loadingDiv.classList.add('hidden');
    }
}

// display helpers
function displayResult(data) {
    // prediction badge
    $('prediction').textContent = data.prediction.toUpperCase();
    $('prediction').className = `prediction ${data.prediction}`;
    
    // confidence meter
    const confVal = parseFloat(data.confidence) || 0;
    $('confidence').textContent = settings.showConfidence ? `${(confVal*100).toFixed(1)}%` : '';
    const fillEl = $('confidence-fill');
    if(fillEl) fillEl.style.width = `${confVal*100}%`;
    
    // risk level
    const riskEl = $('risk-level');
    riskEl.textContent = data.risk_level.toUpperCase();
    riskEl.className = `risk-badge ${data.risk_level}`;
    
    // metadata
    if($('analysis-time')) $('analysis-time').textContent = data.analysis_time || '';
    if($('threat-score')) $('threat-score').textContent = data.threat_score || '';
    
    // breakdown
    if (settings.detailedBreakdown && $('breakdown-content')) {
        $('breakdown-content').textContent = JSON.stringify(data, null, 2);
    } else if($('breakdown-content')) {
        $('breakdown-content').textContent = '';
    }
    
    // recommendations
    const recList = $('recommendations-list');
    if(recList) {
        recList.innerHTML='';
        (data.recommendations||[]).forEach(r=>{const li=createEl('li',{textContent:r});recList.appendChild(li);});
    }
    
    // show result
    $('result-section').classList.remove('hidden');
}

function showError(msg) {
    $('error-message').textContent = msg;
    $('error-section').classList.remove('hidden');
    $('result-section').classList.add('hidden');
}

// history
function saveToHistory(entry) {
    if (!settings.autoSaveHistory) return;
    historyData.unshift(entry);
    localStorage.setItem('history', JSON.stringify(historyData));
    renderHistory();
}
function loadHistory() {
    const raw = localStorage.getItem('history');
    if (raw) historyData = JSON.parse(raw);
    renderHistory();
}
function renderHistory(filter='all', query='') {
    const list = $('history-list');
    list.innerHTML='';
    historyData.forEach((e,i)=>{
        if(filter!=='all' && e.prediction!==filter) return;
        if(query && !JSON.stringify(e).toLowerCase().includes(query.toLowerCase())) return;
        const item=createEl('div',{className:'history-item'});
        item.textContent = `${e.email_subject} → ${e.prediction.toUpperCase()} (${e.confidence.toFixed(2)})`;
        item.addEventListener('click',()=>displayResult(e));
        list.appendChild(item);
    });
}
$('history-search')?.addEventListener('input',e=>renderHistory($('history-filter').value,e.target.value));
$('history-filter')?.addEventListener('change',e=>renderHistory(e.target.value,$('history-search').value));
$('clear-history')?.addEventListener('click',()=>{historyData=[];localStorage.removeItem('history');renderHistory();});

// settings
function loadSettings() {
    const raw = localStorage.getItem('settings');
    if (raw) settings = JSON.parse(raw);
    // map HTML IDs to settings keys
    const idMap = {
        'auto-save-history': 'autoSaveHistory',
        'show-confidence': 'showConfidence',
        'detailed-breakdown': 'detailedBreakdown',
        'notify-high-risk': 'notifyHighRisk',
        'sound-alerts': 'soundAlerts',
        'export-format': 'exportFormat'
    };
    Object.entries(idMap).forEach(([htmlId, settingKey])=>{
        const el=$(htmlId);
        if(el) {
            if(el.type==='checkbox') el.checked=settings[settingKey];
            else el.value=settings[settingKey];
        }
    });
}
function saveSettings() {
    const idMap = {
        'auto-save-history': 'autoSaveHistory',
        'show-confidence': 'showConfidence',
        'detailed-breakdown': 'detailedBreakdown',
        'notify-high-risk': 'notifyHighRisk',
        'sound-alerts': 'soundAlerts',
        'export-format': 'exportFormat'
    };
    Object.entries(idMap).forEach(([htmlId, settingKey])=>{
        const el=$(htmlId);
        if(el)settings[settingKey]= el.type==='checkbox' ? el.checked : el.value;
    });
    localStorage.setItem('settings', JSON.stringify(settings));
    alert('Settings saved!');
}
$('save-settings')?.addEventListener('click',saveSettings);

// export/share helpers
function exportCurrentResult() {
    const data = historyData[0];
    if (!data) return;
    const blob = new Blob([JSON.stringify(data,null,2)],{type:'application/json'});
    const url = URL.createObjectURL(blob);
    const a = createEl('a',{href:url,download:`analysis.${settings.exportFormat}`});
    a.click();
}
function shareCurrentResult() {
    const data = historyData[0];
    if (!data) return;
    navigator.clipboard.writeText(JSON.stringify(data,null,2));
    alert('Result copied to clipboard');
}

// batch processing (simple CSV parser)
// Browse button trigger
if($('browse-btn')) {
    console.log('Browse button found, adding click handler');
    $('browse-btn').addEventListener('click', () => {
        console.log('Browse button clicked');
        $('batch-file').click();
    });
} else {
    console.log('Browse button not found');
}

// Drag and drop functionality for upload area
const uploadArea = $('upload-area');
if(uploadArea) {
    // Prevent default drag behaviors
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // Highlight drag area
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        uploadArea.classList.add('dragover');
    }

    function unhighlight(e) {
        uploadArea.classList.remove('dragover');
    }

    // Handle drop
    uploadArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        console.log('Files dropped:', files.length);

        if (files.length > 0) {
            const file = files[0];
            console.log('File type:', file.type, 'File name:', file.name);

            if (file.type === 'text/csv' || file.name.toLowerCase().endsWith('.csv')) {
                // Process the file directly
                processCSVFile(file);
                console.log('File processed directly from drop');
            } else {
                alert('Please drop a CSV file only.');
            }
        }
    }
}

$('batch-file')?.addEventListener('change', async e=>{
    console.log('File input change event triggered');
    const file=e.target.files[0];
    console.log('Selected file:', file);
    if(!file) {
        console.log('No file selected');
        return;
    }
    processCSVFile(file);
});

async function processCSVFile(file) {
    const text=await file.text();
    console.log('File content length:', text.length);
    // Simple CSV parser that handles quoted fields
    const rows = [];
    const lines = text.trim().split(/\r?\n/);
    for (const line of lines) {
        // Handle quoted fields with commas
        const fields = [];
        let current = '';
        let inQuotes = false;
        for (let i = 0; i < line.length; i++) {
            const char = line[i];
            if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                fields.push(current.trim());
                current = '';
            } else {
                current += char;
            }
        }
        fields.push(current.trim());
        rows.push(fields);
    }
    batchData = rows.slice(1).map(r=>({subject:(r[0]||'').replace(/^"|"$/g,''),body:(r[1]||'').replace(/^"|"$/g,'')}));
    $('analyze-batch-btn').disabled=false;
    alert(`Loaded ${batchData.length} emails. Click "Analyze Batch" to process.`);
}
$('analyze-batch-btn')?.addEventListener('click',async ()=>{
    const total=batchData.length;
    let completed=0, phishing=0;
    const results=[];
    $('batch-progress').classList.remove('hidden');
    for(const item of batchData){
        const res=await analyzeEmail(item.subject,item.body);
        if(res){
            if(res.prediction==='phishing') phishing++;
            results.push({...item,...res});
        }
        completed++;
        const pct=Math.round((completed/total)*100);
        $('progress-fill').style.width=`${pct}%`;
        $('progress-text').textContent=`${completed} / ${total}`;
    }
    $('batch-progress').classList.add('hidden');
    $('total-emails').textContent=total;
    $('phishing-count').textContent=phishing;
    $('legitimate-count').textContent=total-phishing;
    $('batch-results').classList.remove('hidden');
    $('download-results').onclick=()=>{
        const csv='subject,body,prediction,confidence\n'+
            results.map(r=>`"${r.subject}","${r.body}",${r.prediction},${r.confidence}`).join('\n');
        const blob=new Blob([csv],{type:'text/csv'});
        const url=URL.createObjectURL(blob);
        const a=createEl('a',{href:url,download:'batch_results.csv'});a.click();
    };
});

// retry button
$('retry-analysis')?.addEventListener('click',()=>{
    $('error-section').classList.add('hidden');
    $('detector-form').dispatchEvent(new Event('submit'));
});


