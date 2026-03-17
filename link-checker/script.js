function showResult(risk, warnings, className){

const result = document.getElementById("result")

result.className = className
result.style.display="block"

result.innerHTML = `
<strong>${risk}</strong>

<ul>
${warnings.map(w=>`<li>${w}</li>`).join("")}
</ul>

<p><strong>Recommended Actions:</strong></p>

<ul>
<li>Do NOT click suspicious links</li>
<li>Verify the sender</li>
<li>Check official websites manually</li>
<li>Report to IT or security team</li>
</ul>
`
}

function checkLink(){

const url=document.getElementById("urlInput").value.trim()

let warnings=[]

if(!url){
alert("Enter a link")
return
}

if(url.includes("@"))
warnings.push("Contains '@' symbol which may redirect to another site")

if(url.match(/\d+\.\d+\.\d+\.\d+/))
warnings.push("Uses IP address instead of domain")

if(url.length>75)
warnings.push("Very long URL used to hide malicious content")

if(url.match(/bit\.ly|tinyurl|t\.co/))
warnings.push("Shortened link hiding real destination")

if(!url.startsWith("https://"))
warnings.push("Link is not using HTTPS")

if(url.match(/\.(exe|zip|html)$/))
warnings.push("Suspicious file extension")

analyzeRisk(warnings)

}

function checkEmail(){

const email=document.getElementById("emailInput").value.toLowerCase()

let warnings=[]

if(!email){
alert("Paste the email text")
return
}

if(email.includes("urgent"))
warnings.push("Uses urgency to pressure you")

if(email.includes("verify your account"))
warnings.push("Requests account verification")

if(email.includes("click here"))
warnings.push("Email asks you to click a link")

if(email.includes("password"))
warnings.push("Requests sensitive information")

if(email.includes("bank"))
warnings.push("Mentions financial information")

if(email.includes("gift card"))
warnings.push("Gift card scam indicator")

if(email.includes("wire transfer"))
warnings.push("Possible business email compromise scam")

analyzeRisk(warnings)

}

function analyzeRisk(warnings){

let risk
let className

if(warnings.length===0){

risk="🟢 LOW RISK"

className="safe"

}

else if(warnings.length<=2){

risk="🟡 SUSPICIOUS"

className="warning"

}

else{

risk="🔴 HIGH RISK – Likely phishing"

className="danger"

}

showResult(risk,warnings,className)

}