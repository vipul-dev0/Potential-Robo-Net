function qs(sel) { return document.querySelector(sel); }

const robotIpInput = qs('#robotIp');
const saveIpBtn = qs('#saveIp');
const distanceEl = qs('#distance');
const speedEl = qs('#speed');

function getStoredIp() {
  return localStorage.getItem('robot_ip') || robotIpInput.value;
}

function setStoredIp(v) {
  localStorage.setItem('robot_ip', v);
}

saveIpBtn.addEventListener('click', () => {
  const v = robotIpInput.value.trim();
  setStoredIp(v);
  alert('Saved IP: ' + v);
});

async function sendCmd(cmd) {
  const robot_ip = getStoredIp();
  if (!robot_ip) { alert('Set robot IP'); return; }
  try {
    const params = new URLSearchParams({state: cmd, robot_ip: robot_ip});
    const resp = await fetch('/control/api/command/?' + params.toString(), {method: 'GET'});
    const data = await resp.json();
    if (data.ok && data.robot) {
      const r = data.robot;
      if (r.distance) distanceEl.textContent = r.distance;
      if (r.speed) speedEl.textContent = r.speed;
      if (r.raw && typeof r.raw === 'string') {
        // try to display numbers if present
        try {
          const parsed = JSON.parse(r.raw);
          if (parsed.distance) distanceEl.textContent = parsed.distance;
          if (parsed.speed) speedEl.textContent = parsed.speed;
        } catch(e){}
      }
    } else if (data.error) {
      console.warn('Robot error', data.error);
    }
  } catch (e) {
    console.error(e);
    alert('Failed to contact robot: ' + e.message);
  }
}

document.querySelectorAll('[data-cmd]').forEach(btn => {
  btn.addEventListener('click', () => sendCmd(btn.getAttribute('data-cmd')));
});

// Poll status every 3s by sending a harmless 'S' (stop) command to read distance/speed
setInterval(() => sendCmd('S'), 3000);
