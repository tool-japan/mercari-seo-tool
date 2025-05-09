document.getElementById("seoForm").addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    try {
        const response = await fetch("http://localhost:5000/api/generate", {
            method: "POST",
            body: formData,
        });
        
        const data = await response.json();
        document.getElementById("results").innerHTML = `<h2>生成されたキーワード:</h2><p>${data.keywords}</p>`;
    } catch (error) {
        document.getElementById("results").innerHTML = `<p style="color: red;">エラーが発生しました: ${error.message}</p>`;
    }
});

