const sandbox = document.querySelector("[data-code-sandbox]");
const isEnglish = document.documentElement.lang === "en";
const copy = isEnglish ? {
    noOutput: "(No stdout)", passed: "Run completed", review: "Review needed",
    truncated: "output truncated", running: "Running code in the FastAPI sandbox…",
    response: "Sandbox returned a result.", responseError: "Sandbox returned a structured error.",
    unavailable: "Could not reach the Django sandbox endpoint. Please try again.",
    disconnected: "Unable to connect to the sandbox.",
} : {
    noOutput: "(Không có stdout)", passed: "Chạy thành công", review: "Cần kiểm tra lại",
    truncated: "output bị cắt", running: "Đang chạy code trong FastAPI sandbox...",
    response: "Sandbox đã trả kết quả.", responseError: "Sandbox trả lỗi có cấu trúc.",
    unavailable: "Không gọi được Django sandbox endpoint. Hãy thử lại sau.",
    disconnected: "Không thể kết nối sandbox.",
};


function getCsrfToken() {
    const tokenInput = document.querySelector("input[name='csrfmiddlewaretoken']");
    return tokenInput ? tokenInput.value : "";
}


function setStatus(statusNode, message) {
    if (statusNode) {
        statusNode.textContent = message;
    }
}


function showResult(resultPanel, payload) {
    const title = resultPanel.querySelector("[data-sandbox-result-title]");
    const meta = resultPanel.querySelector("[data-sandbox-result-meta]");
    const output = resultPanel.querySelector("[data-sandbox-output]");
    const error = resultPanel.querySelector("[data-sandbox-error]");
    const outputText = payload.execution_output || copy.noOutput;

    resultPanel.hidden = false;
    resultPanel.dataset.status = payload.status || "error";
    title.textContent = payload.status === "passed" ? copy.passed : copy.review;
    meta.textContent = [
        payload.exit_code === null || payload.exit_code === undefined
            ? null
            : `exit ${payload.exit_code}`,
        payload.timed_out ? "timeout" : null,
        payload.output_truncated ? copy.truncated : null,
    ].filter(Boolean).join(" · ");
    output.textContent = outputText;

    if (payload.error_message) {
        error.hidden = false;
        error.textContent = payload.error_message;
    } else {
        error.hidden = true;
        error.textContent = "";
    }
}


async function runSandbox() {
    if (!sandbox) {
        return;
    }

    const runButton = sandbox.querySelector("[data-sandbox-run]");
    const codeInput = sandbox.querySelector("[data-sandbox-code]");
    const stdinInput = sandbox.querySelector("[data-sandbox-stdin]");
    const statusNode = sandbox.querySelector("[data-sandbox-status]");
    const resultPanel = sandbox.querySelector("[data-sandbox-result]");
    const runUrl = sandbox.dataset.runUrl;

    if (!runButton || !codeInput || !stdinInput || !runUrl) {
        return;
    }

    runButton.disabled = true;
    setStatus(statusNode, copy.running);

    try {
        const response = await fetch(runUrl, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCsrfToken(),
            },
            body: JSON.stringify({
                code: codeInput.value,
                stdin: stdinInput.value,
                timeout_seconds: Number(sandbox.dataset.timeoutSeconds || 3),
            }),
        });
        const payload = await response.json();
        showResult(resultPanel, payload);
        setStatus(
            statusNode,
            response.ok ? copy.response : copy.responseError,
        );
    } catch (error) {
        showResult(resultPanel, {
            status: "error",
            execution_output: "",
            error_message: copy.unavailable,
            exit_code: null,
            timed_out: false,
            output_truncated: false,
        });
        setStatus(statusNode, copy.disconnected);
    } finally {
        runButton.disabled = false;
    }
}


function setupSandbox() {
    if (!sandbox) {
        return;
    }

    const runButton = sandbox.querySelector("[data-sandbox-run]");
    const resetButton = sandbox.querySelector("[data-sandbox-reset]");
    const codeInput = sandbox.querySelector("[data-sandbox-code]");
    const initialCode = codeInput ? codeInput.value : "";

    if (runButton) {
        runButton.addEventListener("click", runSandbox);
    }
    if (resetButton && codeInput) {
        resetButton.addEventListener("click", () => {
            codeInput.value = initialCode;
            codeInput.focus();
        });
    }
}


setupSandbox();
