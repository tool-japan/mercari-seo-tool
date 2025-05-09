document.getElementById("seoForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    try {
        // 相対URLに修正（Render用）
        const response = await fetch("/api/generate", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        document.getElementById("results").innerHTML = `<h2>生成されたキーワード:</h2><p>${data.keywords}</p>`;
    } catch (error) {
        console.error(error);
        document.getElementById("results").innerHTML = `<p style="color: red;">エラーが発生しました: ${error.message}</p>`;
    }
});
