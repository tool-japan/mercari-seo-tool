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
        
        // デバッグログ
        console.log("📄 受信したデータ:", data);

        // キーワードが定義されているか確認
        if (data.keywords) {
            document.getElementById("results").innerHTML = `<h2>生成されたキーワード:</h2><p>${data.keywords}</p>`;
        } else if (data.message) {
            document.getElementById("results").innerHTML = `<h2>メッセージ:</h2><p>${data.message}</p>`;
        } else if (data.error) {
            document.getElementById("results").innerHTML = `<p style="color: red;">エラーが発生しました: ${data.error}</p>`;
        } else {
            document.getElementById("results").innerHTML = `<p style="color: red;">不明なエラーが発生しました</p>`;
        }

    } catch (error) {
        console.error(error);
        document.getElementById("results").innerHTML = `<p style="color: red;">エラーが発生しました: ${error.message}</p>`;
    }
});
