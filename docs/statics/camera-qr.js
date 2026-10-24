const video = document.getElementById('camera');
const startButton = document.getElementById('start');
const stopButton = document.getElementById('stop');
const switchButton = document.getElementById('switch');
const status = document.getElementById('status');
const resultText = document.getElementById('result-text');
const resultLink = document.getElementById('result-link');

let scanner;
let facing = 'environment';
let busy = false;
let running = false;
let session = 0;

function setStatus(message, isError = false) {
    status.textContent = message;
    status.dataset.error = String(isError);
}

function updateControls() {
    startButton.disabled = busy || running;
    stopButton.disabled = !running;
    switchButton.disabled = busy || !running;
    switchButton.textContent = facing === 'environment' ? 'Use front camera' : 'Use rear camera';
}

function stopCamera() {
    session++;
    scanner?.stop();
    // Release the camera immediately, including during an interrupted start.
    if (video.srcObject) {
        video.srcObject.getTracks().forEach(track => track.stop());
        video.srcObject = null;
    }
    running = false;
    updateControls();
}

function showResult(result) {
    if (!running) return;
    const text = result.data;
    resultText.textContent = text;
    resultLink.hidden = true;
    resultLink.removeAttribute('href');
    resultLink.textContent = '';
    try {
        const url = new URL(text.trim());
        if (url.protocol === 'https:' || url.protocol === 'http:') {
            resultLink.href = url.href;
            resultLink.textContent = `Open link: ${url.href}`;
            resultLink.hidden = false;
        }
    } catch (error) {
        if (!(error instanceof TypeError)) throw error;
        // Most QR payloads are plain text rather than URLs.
    }
    stopCamera();
    startButton.textContent = 'Scan again';
    setStatus('QR code scanned. Camera stopped.');
}

function cameraError(error) {
    if (error === 'Camera not found.') {
        return 'No camera is available. Allow camera access in your browser settings, close other apps using it, or try another device.';
    }
    const name = error?.name;
    if (name === 'NotAllowedError' || name === 'PermissionDeniedError') {
        return 'Camera access was denied. Allow camera access in your browser settings, then try again.';
    }
    if (name === 'NotFoundError' || name === 'DevicesNotFoundError') {
        return 'No camera was found. Connect a camera or try another device.';
    }
    if (name === 'NotReadableError' || name === 'TrackStartError') {
        return 'The camera is unavailable. Close other apps using it, then try again.';
    }
    const detail = error instanceof Error ? error.message : String(error);
    return `Could not start the camera: ${detail}. Check camera permissions and try again.`;
}

startButton.addEventListener('click', async () => {
    if (busy || running) return;
    if (!window.isSecureContext || !navigator.mediaDevices?.getUserMedia) {
        setStatus('Camera access requires HTTPS and a supported browser. Open this page over HTTPS in Safari, Chrome, Firefox, or Edge.', true);
        return;
    }

    busy = true;
    const currentSession = ++session;
    updateControls();
    setStatus('Loading scanner...');
    try {
        if (!scanner) {
            let QrScanner;
            try {
                ({ default: QrScanner } = await import('./qr-scanner-1.4.2/qr-scanner.min.js'));
            } catch (error) {
                throw new Error('The QR scanner library could not load. Reload this page and check your connection', { cause: error });
            }
            if (currentSession !== session) return;
            scanner = new QrScanner(video, showResult, {
                preferredCamera: facing,
                maxScansPerSecond: 10,
                highlightScanRegion: true,
                highlightCodeOutline: true,
                returnDetailedScanResult: true,
                onDecodeError(error) {
                    const message = String(error);
                    if (message === QrScanner.NO_QR_CODE_FOUND
                        || message === `Scanner error: ${QrScanner.NO_QR_CODE_FOUND}`) return;
                    stopCamera();
                    setStatus(`QR scanning failed: ${error}. Please try again.`, true);
                }
            });
        }
        setStatus('Requesting camera access...');
        await scanner.start();
        if (currentSession !== session || document.hidden) {
            stopCamera();
            return;
        }
        running = true;
        setStatus('Scanning... Hold a QR code inside the marked area.');
    } catch (error) {
        stopCamera();
        setStatus(cameraError(error), true);
    } finally {
        busy = false;
        updateControls();
    }
});

stopButton.addEventListener('click', () => {
    stopCamera();
    setStatus('Camera stopped. Press Start camera to resume.');
});

switchButton.addEventListener('click', async () => {
    busy = true;
    const currentSession = session;
    facing = facing === 'environment' ? 'user' : 'environment';
    updateControls();
    setStatus('Switching camera...');
    try {
        await scanner.setCamera(facing);
        if (currentSession === session && running) {
            setStatus('Scanning... Hold a QR code inside the marked area. If this device has only one camera, it will continue to be used.');
        }
    } catch (error) {
        stopCamera();
        setStatus(cameraError(error), true);
    } finally {
        busy = false;
        updateControls();
    }
});

document.addEventListener('visibilitychange', () => {
    if (document.hidden && (running || busy)) {
        stopCamera();
        setStatus('Camera stopped because the page was hidden. Press the start button to resume.');
    }
});

window.addEventListener('pagehide', stopCamera);
